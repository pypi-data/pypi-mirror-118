# -*- coding: utf8 -*-
"""
Kriging adapted from vacumm's module
https://github.com/VACUMM/vacumm/blob/master/lib/python/vacumm/misc/grid/kriging.py

"""
from __future__ import absolute_import
import gc
from multiprocessing import Pool,  cpu_count
import warnings

import numpy as np
import xarray as xr

from .__init__ import XoaError
from . import misc
from . import geo
from . import cf as xcf
from . import coords as xcoords




#from scipy.optimize import curve_fit
def get_blas_func(name):
    try:
        import scipy.linalg.blas
        func = scipy.linalg.blas.get_blas_funcs(name)
    except:
        import scipy.linalg.fblas
        func = getattr(scipy.linalg.fblas, 'd'+name)
    return func


blas_dgemv = get_blas_func('gemv')


def dgemv(a, x): return blas_dgemv(1., a, x)


dgemm = get_blas_func('gemm')


def symm(a, b): return dgemm(1., a, b)


sytri = np.linalg.pinv


class KrigingError(XoaError):
    pass


def get_xyz(obj):
    """Get lon/lat coordinates and data values from a data array or dataset

    Parameters
    ----------
    obj: xarray.DataArray, xarray.Dataset
        If a data array, it must have valid longitude and latitude coordinates.
        If a dataset, it must have a single variable as in the data array case.

    Return
    ------
    numpy.array
        Longitudes as 1D array
    numpy.array
        Latitudes as 1D array
    numpy.array
        Values as a 1D or 2D. None if `obj` is a dataset.
    """
    # Xarray stuff
    if isinstance(obj, xr.Dataset):
        obj = obj[list(obj)[0]]
    lon = xcoords.get_lon(obj)
    lat = xcoords.get_lat(obj)
    obj = obj.stack({"ssss": set(lon.dims).union(lat.dims)})

    # Numpy
    x = obj.coords[lon.name].values
    y = obj.coords[lat.name].values
    if isinstance(obj, xr.DataArray):
        z = obj.values.reshape(-1, x.size)
    else:
        z = None

    return x, y, z


def empirical_variogram(
        da, nbin=30, nbin0=10, nmax=1500, distmax=None, errfunc=None):
    """Compute the semi-variogram from data

    Parameters
    ----------

    da: xarray.dataArray
        Data array with lon and lat coordinates.
    nmax: optional
        Above this number, size of the sample is reduced by a crude undersampling.
    binned: optional
        If set to a number,
        data are arranged in bins to estimate
        variogram. If set to ``None``, data are
        arranged in bins if the number of pairs
        of points is greater than ``nbindef*nbmin``.
    nbindef: optional
        Default number of bins (not used if ``binned`` is a number).
    nbin0: optional
        If set to a number > 1,
        the first bin is split into nbin0 sub-bins.
        If set to ``None``, it is evaluated with
        ``min(bins[1]/nbmin, nbin)``.
    nbmin: optional
        Minimal number of points in a bin.
    distmax: optional
        Max distance to consider.
    errfunc: optional
        Callable function to compute "errors" like square
        root difference between to z values. It take two arguments and
        defaults to :math:`(z1-z0)^2/2`.

    Return
    ------
    xarray.DataArray
        Values as 1D array with name "semivariogram" and with "dist" as distance coordinate in km

    """
    x, y, z = get_xyz(da)
    npts = x.shape[0]

    # Undepsample?
    if npts > nmax:
        samp = npts/nmax
        x = x[::samp]
        y = y[::samp]
        z = z[..., ::samp]
        npts = x.shape[0]

    # Distances
    dd = geo.pdist(x, y) * 1e-3
    iitriu = np.triu_indices(dd.shape[0], 1)
    d = dd[iitriu]
    del dd

    # Max distance
    if distmax:
        iiclose = d <= distmax
        d = d[iiclose]
        # v = v[valid]
        # del valid
    else:
        iiclose = ...

    # Variogram
    if errfunc is None:
        def errfunc(a0, a1): return 0.5*(a1-a0)**2
    z = np.atleast_2d(z)
    v = np.asarray([errfunc(*np.meshgrid(z[i], z[i]))[iitriu][iiclose] for i in range(z.shape[0])])

    # Unique
    d, iiuni = np.unique(d, return_index=True)
    v = v[:, iiuni]

    # Compute edges
    # - classic bins
    nbin = min(d.size, nbin)
    iiedges = np.linspace(0, d.size-1, nbin+1).astype('l').tolist()
    # - more details in the first bin
    if nbin0 > 1 and nbin0 < iiedges[1]:  # split first bin
        iiedges = np.linspace(0., iiedges[1], nbin0+1).astype('l')[:-1].tolist()+iiedges[1:]
        nbin = nbin - 1 + nbin0  # len(iiedges)-1
        print('BIN0')

    # Compute histogram
    db = np.empty(nbin)
    vb = np.empty(nbin)
    for ib in range(nbin):
        iib = slice(iiedges[ib], iiedges[ib+1]+1)
        db[ib] = d[iib].mean()
        vb[ib] = v[:, iib].mean()

    # Dataarray
    dist = xr.DataArray(db, dims="dist", attrs={'long_name': "Distance", "units": "km"})
    attrs = {}
    if "long_name" in da.attrs:
        attrs = {"long_name": "Semi-variogram of "+da.attrs["long_name"]}
    else:
        attrs = {"long_name": "Semi-variogram"}
    if "units" in da.attrs:  # TODO: pint support
        attrs = {"units": da.attrs["units"]+"^2"}
    return xr.DataArray(
        vb,
        dims="dist",
        coords={"dist": ("dist", dist, {"long_name": "Distance", "units": "km"})},
        attrs=attrs,
        name="semivariogram")



class variogram_model_types(misc.IntEnumChoices, metaclass=misc.DefaultEnumMeta):
    """Supported types of variograms"""
    #: Exponential (default)
    exponential = 1
    #: Linear
    linear = 0
    #: Gausian
    gaussian = 2
    #: Spherical
    spherical = 3


def get_variogram_model_func(mtype, n, s, r, nrelmax=0.2):
    """Get the variogram model function from its name"""

    mtype = variogram_model_types[mtype]

    n = max(n, 0)
    n = min(n, nrelmax*s)
    r = max(r, 0)
    s = max(s, 0)

    if mtype.name == 'linear':
        return lambda h: n + (s-n) * ((h/r)*(h <= r) + 1*(h > r))

    if mtype.name == 'exponential':
        return lambda h: n + (s-n) * (1 - np.exp(-3*h/r))

    if mtype.name == 'gaussian':
        return lambda h: n + (s-n)*(1-np.exp(-3*h**2/r**2))

    if mtype.name == 'spherical':
        return lambda h: n + (s-n)*((1.5*h/r - 0.5*(h/r)**3)*(h <= r) + 1*(h > r))


class VariogramModel(object):
    """Class used when fitting a variogram model to data to better control params"""
    param_names = list(get_variogram_model_func.__code__.co_varnames[1:])
    param_names.remove('nrelmax')

    def __init__(self, mtype, **frozen_params):
        self.mtype = variogram_model_types[mtype]
        self._frozen_params = {}
        self._estimated_params = {}
        self._fit = None
        self._fit_err = None
        self.set_params(**frozen_params)
        self._ev = None

    def __str__(self):
        clsname = self.__class__.__name__
        mtype = self.mtype.name
        sp = []
        for name in self.param_names:
            sp.append("{}={}".format(name, self[name]))
        sp = ', '.join(sp)
        return f"<{clsname}('{mtype}', {sp})>"

    def __repr__(self):
        return str(self)

    @property
    def frozen_params(self):
        return dict((name, self._frozen_params[name]) for name in self.param_names
                    if name in self._frozen_params)

    def get_estimated_params(self):
        return dict((name, self._estimated_params.get(name)) for name in self.param_names
                    if name not in self._frozen_params)

    def set_estimated_params(self, overwrite=True, **params):
        params_update = dict(
            (name, params[name]) for name in self.param_names
            if name not in self._frozen_params and name in params and
            (not overwrite or name not in self._estimated_params))
        self._estimated_params.update(params_update)

    estimated_params = property(get_estimated_params,set_estimated_params, doc='Estimated paramaters')

    def set_params(self, **params):
        """Freeze some parameters"""
        params = dict([(p, v) for (p, v) in params.items()
                      if p in self.param_names and v is not None])
        self._frozen_params.update(params)

    def get_params(self, **params):
        """Get current parameters with optional update

        Parameters
        ----------
        asarray: bool
            If True, return parameters as an array in the right order
            and raise an error if one of them is missing or None
        params:
            Extra parameters to alter currents values

        Return
        ------
        dict, numpy.array
        """
        these_params = dict(**self.frozen_params, **self.estimated_params)
        if params:
            these_params.update(
                dict([(p, v) for (p, v) in params.items()
                      if p in self.param_names and v is not None]))
        return dict((name, these_params[name]) for name in self.param_names)

    def get_param(self, name):
        """Get a single parameter

        Parameter
        ---------
        name: str
            A valid parameter name

        Returns
        -------
        float, None
            Returns None if the parameter is not frozen and has not been estimated yet.
        """
        if name not in self.param_names:
            raise KrigingError(
                f"Invalid param name: {name}. Please use one of: "+", ".join(self.param_names))
        if name in self._frozen_params:
            return self._frozen_params[name]
        return self._estimated_params.get(name)

    __getitem__ = get_param

    def get_params_array(self):
        """Get the :attr:`estimated_param` as an array

        Returns
        -------
        numpy.array
        """
        pp = list(self.estimated_params.values())
        if None in pp:
            raise VariogramModelError(
                "No all parameters are estimated: {}".format(self.estimated_params))
        return np.array(pp)

    def set_params_array(self, pp):
        """Set the :attr:`estimated_param` with an array

        Parameters
        ----------
        pp: numpy.array
            Array of estimated parameters
        """
        for i, name in enumerate(self.estimated_params):
            self._estimated_params[name] = pp[i]
        return self.params

    @property
    def params(self):
        """Current variogram model parameters"""
        return self.get_params()

    def __call__(self, d, pp=None):
        """Call the variogram model function

        Parameters
        ----------
        d: array
            Distances in km
        """
        return self.get_func(pp)(d)

    def get_func(self, pp=None):
        """Get the variogram model function using `pp` variable arguments"""
        if pp is not None:
            params = self.set_params_array(pp)
        else:
            params = self.get_params()
            if None in list(params.values()):
                raise VariogramModelError("No all parameters are estimated: {}".format(self.estimated_params))
        return get_variogram_model_func(self.mtype, **params)

    def fit(self, da, **kwargs):
        """Estimate parameters from data"""
        # Empirical variogram
        if da.name == "semivariogram" or da.name == "variogram":
            ev = da
        else:
            ev = empirical_variogram(da, **kwargs)
        dist = ev.dist.values * 1e3
        values = ev.values
        self._ev = ev

        # First guess of paramaters
        imax = np.ma.argmax(values)
        self.set_estimated_params(n=0., s=values[imax], r=dist[imax], overwrite=False)
        pp0 = self.get_params_array()

        # Fitting
        from scipy.optimize import minimize
        def func(pp): return ((values-self(dist, pp))**2).sum()
        with warnings.catch_warnings():
            warnings.filterwarnings('ignore', 'divide by zero encountered in divide')
            self._fit = minimize(
                func, pp0, bounds=[(np.finfo('d').eps, None)]*len(pp0), method='L-BFGS-B')
            pp = self._fit['x']
            self._fit_err = np.sqrt(func(pp))/values.size

        self.set_params_array(pp)

    def plot(self, rmax=None, nr=100, show_params=True, **kwargs):
        """Plot the semivariogram

        Parameters
        ----------
        rmax: float
            Max range in meters
        nr: int
            Number of points to plot the curve
        show_params: bool, dict
            Show a text box that contains the variogram paramters in the lower right corner.
        kwargs: dict
            Extra keyword are passed to the `xarray.DataArray.plot` callable accessor
        """
        # Distances
        if rmax is None and self._ev is not None:
            rmax = self._ev.dist.max() * 1e3
        else:
            rmax =self["r"]*1.2
        dist = np.linspace(0, rmax, nr)

        # Array and plot
        mv = xr.DataArray(
            self.get_func()(dist),
            dims='dist',
            coords=[("dist", dist*1e-3, {"long_name": "Distance", "units": "km"})],
            attrs={"long_name": self.mtype.name.title()+" fit"})
        kwargs.setdefault("label", mv.long_name)
        p = mv.plot(**kwargs)

        # Text box for params
        if show_params:
            params = self.params.copy()
            text = ["r = {:<g} km".format(params["r"]*1e-3),
                    "n = {:<g}".format(params["n"]),
                    "r = {:<g}".format(params["s"])]
            maxlen = max([len(t) for t in text])
            text = "\n".join(t.ljust(maxlen) for t in text)
            axes = p[0].axes
            axes.text(0.98, 0.04, text, transform=axes.transAxes, family="monospace",
                      bbox=dict(facecolor=(1, 1, 1, .5)), ha="right")


class VariogramModelError(KrigingError):
    pass


# def variogram_fit(da, mtype=None, getall=False, getp=False, geterr=False,
#                   errfunc=None, **kwargs):
#     """Fit a variogram model to data and return a VariogramModel

#     Example
#     -------

#         >>> vm, errs = variogram_fit(x, y, z, 'linear', n=0, distmax=30e3, geterr=True)

#     Parameters
#     ----------

#     da: xarray.dataArray
#         Data array with lon and lat coordinates.
#     mtype:
#         Variogram model type (see ::`variogram_model_type`).
#     getall:
#         Get verything in a dictionary whose keys are

#             - ``"func"``: model function,
#             - ``"err"``: fitting error,
#             - ``"params"``: all parameters has a dictionary,
#             - ``"popt"``: parameters than where optimised,
#             - ``vm"``: :class:`VariogramModel` instance,
#             - ``"mtype"``: variogram model type.

#     getp: optional
#         Only return model parameters. Return them as
#         a `class:`dict` if equal to ``2``.
#     variogram_<param>: optional
#         ``param`` is passed to :func:`variogram`.
#     distfunc:
#     errfunc: optional
#         Callable function to compute "errors" like square
#         root difference between to z values. It take two arguments and
#         defaults to :math:`\sqrt(z1^2-z0^2)/2`.

#         .. warning:: use "haversine" if input coordinates are in degrees.

#         - Extra keywords are those of :func:`variogram_model`.
#           They can be used to freeze some of the parameters.

#           >>> variogram_fit(x, y, z, mtype, n=0) # fix the nugget

#     Return
#     ------
#     VariogramModel
#     """
#     kwv = misc.kwfilter(kwargs, 'variogram_')
#     kwv.setdefault("errfunc", errfunc)

#     # Variogram model
#     vm = VariogramModel(mtype, **kwargs)

#     # Empirical variogram
#     d, v = empirical_variogram(da, **kwv)

#     # First guess of paramaters
#     imax = np.ma.argmax(v)
#     p0 = vm.get_var_args(n=0., s=v[imax], r=d[imax])

#     # Fitting
# #    p, e = curve_fit(vm, d, v, p0=p0) # old way: no constraint
#     from scipy.optimize import minimize

#     def func(pp): return ((v-vm.get_func(pp)(d))**2).sum()
#     warnings.filterwarnings('ignore', 'divide by zero encountered in divide')
#     p = minimize(func, p0, bounds=[(np.finfo('d').eps, None)]*len(p0),
#                  method='L-BFGS-B')['x']
#     del warnings.filters[0]

#     # Output
#     if getall:
#         return dict(
#             func=vm.get_func(p),
#             err=(vm.get_func(p)(d)-v).std(),
#             params=vm.get_all_kwargs(p),
#             popt=p)
#     if int(getp) == 2:
#         res = vm.get_all_kwargs(p)
#     elif getp:
#         res = p
#     else:
#         res = vm.get_func(p)
#     if not geterr:
#         return res
#     return res,  (vm.get_func(p)(d)-v).std()


# def variogram_multifit(xx, yy, zz, mtype=None, getall=False, getp=False, **kwargs):
#     """Same as :func:`variogram_fit` but with several samples"""
#     vm = VariogramModel(mtype, **kwargs)
#     pp = []
#     for i, (x, y, z) in enumerate(zip(xx, yy, zz)):
#         x, y, z = _get_xyz_(x, y, z, check=False)
#         if len(x) == 0:
#             continue
#         p = variogram_fit(x, y, z, mtype, getp=True, **kwargs)
#         pp.append(p)
#     pp = np.asarray(pp)
#     if pp.shape[0] == 0:
#         raise KrigingError('All data are masked')
#     mp = np.median(pp, axis=0)
#     if getall:
#         return dict(
#             func=vm.get_func(mp),
#             err=None,
#             params=vm.get_all_kwargs(mp),
#             popt=mp)
#     if int(getp) == 2:
#         return vm.get_all_kwargs(mp)
#     if getp:
#         return mp
#     return vm.get_func(mp)


def clusterize(obj, npmax=1000):
    """Split data into clouds of points of max size npmax

    Parameters
    ----------
    obj: xarray.DataArray, xarray.Dataset
        If a data array, it must have valid longitude and latitude coordinates.

    Returns
    -------
    ``None`` if ``len(x)<=npmax``

        Else ``indices``
        or ``(indices, global_distorsion, distortions)``.

    """
    # Positions
    x, y = get_xyz(obj)[:2]

    from scipy.cluster.vq import kmeans, vq

    # Nothing to do
    csize = len(x)
    if npmax < 2 or csize <= npmax:
        return

    # Loop on the number of clusters
    nclust = 2
    points = np.vstack((x, y)).T
    ii = np.arange(csize)
    while csize > npmax:
        centroids, global_distorsion = kmeans(points, nclust)
        indices, distorsions = vq(points, centroids)
        sindices = [ii[indices == nc] for nc in range(nclust)]
        csizes = [sii.shape[0] for sii in sindices]
        order = np.argsort(csizes)[::-1]
        csize = csizes[order[0]]
        sdistorsions = [distorsions[sii] for sii in sindices]
        nclust += 1

    #  Reorder
    sindices = [sindices[i] for i in order]
    sdistorsions = [sdistorsions[i] for i in order]
    dists = global_distorsion,  sdistorsions
    centroids = centroids[order]

    # Output
    if not getdist and not getcent:
        return indices
    ret = sindices,
    if getcent:
        ret += centroids,
    if getdist:
        ret += dists,
    return ret


# def syminv(A):
#     """Invert a symetric matrix

#     Parameters
#     ----------

#     A:
#         (np+1,np+1) for variogram matrix

#     Return
#     ------
#     ``Ainv(np+1,np+1)``

#     :Raise: :exc:`KrigingError`

#     """
#     res = sytri(A.astype('d'))
#     if isinstance(res, tuple):
#         info = res[1]
#         if info:
#             raise KrigingError(
#                 'Error during call to Lapack DSYTRI (info=%i)' % info)
#         return res[0]
#     else:
#         return res


# class CloudKriger(object):
#     """Ordinary kriger using mutliclouds of points

#     Big input cloud of points (size > ``npmax``)
#     are split into smaller
#     clouds using cluster analysis of distance with
#     function :func:`cloud_split`.

#     The problem is solved in this way:

#         #. Input points are split in clouds if necessary.
#         #. The input variogram matrix is inverted
#            for each cloud, possibly using
#            :mod:`multiprocessing` if ``nproc>1``.
#         #. Value are computed at output positions
#            using each the inverted matrix of cloud.
#         #. Final value is a weighted average of
#            the values estimated using each cloud.
#            Weights are inversely proportional to the inverse
#            of the squared error.

#     Parameters
#     ----------

#     x/y/z:
#         Input positions and data (masked array).
#     mtype: optional
#         Variogram model type (defaults to 'exp').
#         See :func:`variogram_model_type` and :func:`variogram_model_type`.
#     vgf: optional
#         Variogram function. If not set,
#         it is estimated using :meth:`variogram_fit`.
#     npmax: optional
#         Maxima size of cloud.
#     nproc: optional
#         Number of processes to use
#         to invert matrices. Set it to a number <2 to switch off
#         parallelisation.
#     exact: optional
#         If True, variogram is exactly zero when distance is zero.
#     distfunc:
#         Function to compute distances, or a mode argument to
#           :func:`~vacumm.misc.grid.misc.get_distances`.
#     errfunc: optional
#         Callable function to compute "errors" like square
#         root difference between to z values. It take two arguments and
#         defaults to :math:`\sqrt(z1^2-z0^2)/2`.
#         - Extra keywords are  parameters to the :func:`variogram_model` that must not be
#           optimized by :func:`variogram_model`. For instance ``n=0`` fix the
#         - Extra keywords are the parameters to the :func:`variogram_model` that must not be
#           optimized by :func:`variogram_model`. For instance ``n=0`` fixes the
#           nugget to zero.
#           This is used only if ``vfg`` is not passed as an argument.


#     Attributes
#     ----------
#     :attr:`x`, :attr:`y`, :attr:`z`, :attr:`np`,
#         :attr:`xc`, :attr:`yc`, :attr:`zc`,  :attr:`npc`,
#         :attr:`variogram_function`, :attr:`Ainv`, :attr:`npmax`, :attr:`nproc`.

#         .. attribute:: x

#             List of all input x positions.

#         .. attribute:: y

#             List of all input y positions.

#         .. attribute:: z

#             List of all input data.

#         .. attribute:: xc

#             List of input x positions of each cloud.

#         .. attribute:: yc

#             List input of y positions of each cloud.

#         .. attribute:: zc

#             List of input data of each cloud.
#     """

#     def __init__(self, x, y, z, krigtype, mtype=None, vgf=None, npmax=1000,
#                  nproc=None, exact=False, distfunc='simple', errfunc=None,
#                  mean=None, farvalue=None, **kwargs):
#         if krigtype is None:
#             krigtype = 'ordinary'
#         krigtype = str(krigtype).lower()
#         assert krigtype in ['simple', 'ordinary'], ('krigtype must be either '
#                                                     '"simple" or "ordinary"')
#         self.x, self.y, self.z, self.mask = _get_xyz_(
#             x, y, z, noextra=False, getmask=True)
#         self.np = self.x.shape[0]
#         self.nt = 0 if self.z.ndim == 1 else z.shape[0]
#         self.mtype = variogram_model_type(mtype)
#         self.npmax = npmax
#         if nproc is None:
#             nproc = cpu_count()
#         else:
#             nproc = max(1, min(cpu_count(), nproc))
#         self._setup_clouds_()
#         self.nproc = min(nproc, self.ncloud)
#         if callable(vgf):
#             self.variogram_func = vgf
#         self._kwargs = kwargs
#         self.variogram_fitting_results = None
#         self.exact = exact
#         self.distfunc = distfunc
#         self.errfunc = errfunc
#         self.krigtype = krigtype
#         self._simple = self.krigtype == 'simple'
#         if not self._simple:
#             mean = 0.
#         elif mean is None:
#             mean = self.z.mean()
#         self.mean = mean
#         self.farvalue = farvalue

#     def __len__(self):
#         return self.x.shape[0]

#     def _get_xyz_(self, x=None, y=None, z=None):
#         if x is None:
#             x = self.x
#         if y is None:
#             y = self.y
#         if z is None:
#             z = self.z
#         return _get_xyz_(x, y, z, noextra=False)

#     def _setup_clouds_(self):
#         """Setup cloud spliting

#         Estimate:

#             #. The number of procs to use (sef.nproc).
#             #. Cloud positions and data (self.xc/yc/zc[ic]).
#             #. Weight function for each cloud (self.wc[ic](x,y)).
#         """

#         # Split?
#         self.npc = []
#         if self.npmax > 2 and self.x.shape[0] > self.npmax:

#             # Split in clouds
#             indices, centroids, (gdist, dists) = cloud_split(self.x, self.y,
#                                                              npmax=self.npmax, getdist=True, getcent=True)
#             self.ncloud = len(indices)

#             # Loop on clouds
#             self.xc = []
#             self.yc = []
#             self.zc = []
#             for ic in range(self.ncloud):

#                 # Positions and data
#                 for xyz in 'x', 'y', 'z':
#                     getattr(self, xyz+'c').append(getattr(self, xyz)
#                                                   [..., indices[ic]].T)

#                 # Size
#                 self.npc.append(len(indices[ic]))

#         else:  # Single cloud

#             self.xc = [self.x]
#             self.yc = [self.y]
#             self.zc = [self.z.T]
#             self.ncloud = 1
#             self.npc = [self.np]
#             self.cwfunc = [lambda x, y: 1.]

#     def plot_clouds(self, marker='o', **kwargs):
#         """Quickly Plot inputs points splitted in clouds"""
#         P.figure()
#         for x, y in zip(self.xc, self.yc):
#             P.plot(x, y, marker, **kwargs)
#         P.show()

#     def variogram_fit(self, x=None, y=None, z=None, **kwargs):
#         """Estimate the variogram function by using :func:`variogram_fit`"""
#         kw = self._kwargs.copy()
#         kw.update(kwargs)
#         kw['distfunc'] = self.distfunc
#         kw['errfunc'] = self.errfunc
#         x, y, z = self._get_xyz_(x, y, z)
#         if z.ndim == 2:
#             ne = z.shape[0]
#             res = variogram_multifit(
#                 [x]*ne, [y]*ne, z, self.mtype, getall=True, **kw)
#         else:
#             res = variogram_fit(x, y, z, self.mtype, getall=True, **kw)
#         self.variogram_func = res['func']
#         self.variogram_fitting_results = res
#         return self.variogram_func

#     def get_sill(self):
#         vgf = self.variogram_func
#         if self.variogram_fitting_results is not None:
#             return self.variogram_fitting_results['params']['s']
#         return vgf(1e60)

#     sill = property(fget=get_sill, doc="Sill")

#     def set_variogram_func(self, vgf):
#         """Set the variogram function"""
#         if not callable(vgf):
#             raise KrigingError("Your variogram function must be callable")
#         reset = getattr(self, '_vgf', None) is not vgf
#         self._vgf = vgf
#         if reset:
#             del self.Ainv

#     def get_variogram_func(self):
#         """Get the variogram function"""
#         if not hasattr(self, '_vgf'):
#             self.variogram_fit()
#         return self._vgf

#     def del_variogram_func(self):
#         """Delete the variogram function"""
#         if hasattr(self, '_vgf'):
#             del self._vgf
#     variogram_func = property(get_variogram_func, set_variogram_func,
#                               del_variogram_func, "Variogram function")

#     def get_Ainv(self):
#         """Get the inverse of A"""

#         # Already computed
#         if hasattr(self, '_Ainv'):
#             return self._Ainv

#         # Variogram function
#         vgf = self.variogram_func

#         # Loop on clouds
#         if not hasattr(self, '_dd'):
#             self._dd = []
#         Ainv = []
#         AA = []
#         next = int(not self._simple)
#         for ic in range(self.ncloud):

#             # Get distance between input points
#             if len(self._dd) < ic+1:
#                 dd = get_distances(self.xc[ic], self.yc[ic],
#                                    self.xc[ic], self.yc[ic], mode=self.distfunc)
#                 self._dd.append(dd)
#             else:
#                 dd = self._dd[ic]

#             # Form A
#             np = self.npc[ic]
#             A = np.empty((np+next, np+next))
#             A[:np, :np] = vgf(dd)
#             if self.exact:
#                 np.fill_diagonal(A, 0)
#                 A[:np, :np][isclose(A[:np, :np], 0.)] = 0.
#             if not self._simple:
#                 A[-1] = 1
#                 A[:, -1] = 1
#                 A[-1, -1] = 0

#             # Invert for single cloud
#             if self.nproc == 1:
#                 Ainv.append(syminv(A))
#             else:
#                 AA.append(A)

#         # Multiprocessing inversion
#         if self.nproc > 1:
#             pool = Pool(self.nproc)
#             Ainv = pool.map(syminv, AA, chunksize=1)
#             pool.close()

#         # Fortran arrays
#         Ainv = [np.asfortranarray(ainv, 'd') for ainv in Ainv]
#         self.Ainv = Ainv
#         return Ainv

#     def set_Ainv(self, Ainv):
#         """Set the invert of A"""
#         self._Ainv = Ainv

#     def del_Ainv(self):
#         """Delete the invert of A"""
#         if hasattr(self, '_Ainv'):
#             del self._Ainv

#     Ainv = property(get_Ainv, set_Ainv, del_Ainv, doc='Invert of A')

#     def interp(self, xo, yo, geterr=False, blockr=None):
#         """Interpolate to positions xo,yo

#         Parameters
#         ----------

#         xo/yo:
#             Output positions.
#         geterr: optional
#             Also return errors.

#         Return
#         ------
#         ``zo`` or ``zo,eo``
#         """

#         # Inits
#         xo = np.asarray(xo, 'd')
#         yo = np.asarray(yo, 'd')
#         npo = xo.shape[0]
#         vgf = self.variogram_func
#         so = (self.nt, npo) if self.nt else npo
#         zo = np.zeros(so, 'd')
#         if geterr:
#             eo = np.zeros(npo, 'd')
#         if self.ncloud > 1 or geterr:
#             wo = np.zeros(npo, 'd')

#         # Loop on clouds
#         Ainv = self.Ainv
#         next = int(not self._simple)
#         for ic in range(self.ncloud):  # TODO: multiproc here?

#             # Distances to output points
#             # dd = cdist(np.transpose([xi,yi]),np.transpose([xo,yo])) # TODO: test cdist
#             dd = get_distances(
#                 xo, yo, self.xc[ic], self.yc[ic], mode=self.distfunc)

#             # Form B
#             np = self.npc[ic]
#             B = np.empty((np+next, npo))
#             B[:self.npc[ic]] = vgf(dd)
#             if not self._simple:
#                 B[-1] = 1
#             if self.exact:
#                 B[:np][isclose(B[:np], 0.)] = 0.
#             del dd

#             # Block kriging
#             if blockr:
#                 from scipy.spatial import cKDTree
#                 tree = cKDTree(np.transpose([xo, yo]))
#                 Bb = B.copy()
#                 for i, iineigh in enumerate(tree.query_ball_tree(tree, blockr)):
#                     Bb[:, i] = B[:, iineigh].mean()
#                 B = Bb

#             # Compute weights
#             W = np.ascontiguousarray(symm(Ainv[ic], np.asfortranarray(B, 'd')))

#             # Simple kriging with adjusted mean for long distance values
#             if self._simple and self.farvalue is not None:
#                 Ais = self.get_sill() * Ainv[ic].sum(axis=0)
#                 mean = self.farvalue - (self.zc[ic] * Ais).sum()
#                 mean /= (1 - Ais.sum())
#             else:
#                 mean = self.mean

#             # Interpolate
#             z = np.ascontiguousarray(dgemv(np.asfortranarray(W[:np].T, 'd'),
#                                           np.asfortranarray(self.zc[ic]-mean, 'd')))
#             if self._simple:
#                 z += mean

#             # Simplest case
#             if not geterr and self.ncloud < 2:
#                 zo[:] = z.T
#                 continue

#             # Get error
# #            e = (W[:-1]*B[:-1]).sum(axis=0)
#             e = (W*B).sum(axis=0)
#             del W, B

#             # Weigthed contribution based on errors
#             w = 1/e**2
#             if self.ncloud > 1:
#                 z[:] *= w
#             wo += w
#             del w
#             zo[:] += z.T
#             del z

#         # Error
#         if geterr:
#             eo = 1/np.sqrt(wo)

#         # Normalization
#         if self.ncloud > 1:
#             zo[:] /= wo

#         gc.collect()
#         if geterr:
#             return zo, eo
#         return zo

#     __call__ = interp


# class OrdinaryCloudKriger(CloudKriger):
#     """Ordinary kriger using cloud splitting"""

#     def __init__(self, x, y, z, mtype=None, vgf=None, npmax=1000,
#                  nproc=None, exact=False, distfunc='simple', errfunc=None,
#                  **kwargs):
#         CloudKriger.__init__(self, x, y, z, 'ordinary', mtype=mtype, vgf=vgf, npmax=npmax,
#                              nproc=nproc, exact=False, distfunc=distfunc, errfunc=errfunc,
#                              **kwargs)


# OrdinaryKriger = OrdinaryCloudKriger


# class SimpleCloudKriger(CloudKriger):
#     """Simple kriger using cloud splitting"""

#     def __init__(self, x, y, z, mtype=None, vgf=None, npmax=1000,
#                  nproc=None, exact=False, distfunc='simple', errfunc=None,
#                  mean=None, farvalue=None, **kwargs):
#         CloudKriger.__init__(self, x, y, z, 'simple', mtype=mtype, vgf=vgf, npmax=npmax,
#                              nproc=nproc, exact=False, distfunc=distfunc, errfunc=errfunc,
#                              mean=mean, farvalue=farvalue, **kwargs)


# def krig(xi, yi, zi, xo, yo, vgf=None, geterr=False, **kwargs):
#     """Quickly krig data"""
#     return OrdinaryKriger(xi, yi, zi, vgf=vgf, **kwargs)(xo, yo, geterr=geterr)


# def gauss3(x, y,
#            x0=-1, y0=0.5, dx0=1, dy0=1, f0=1.,
#            x1=1, y1=1, dx1=2, dy1=0.5, f1=-1,
#            x2=0, y2=-1.5, dx2=.5, dy2=.5, f2=-.3,
#            **kwargs):
#     """Create data sample as function position and 3-gaussian function"""
#     g = P.bivariate_normal(x, y, dx0, dy0, x0, y0)*f0
#     g += P.bivariate_normal(x, y, dx1, dy1, x1, y1)*f1
#     g += P.bivariate_normal(x, y, dx2, dy2, x2, y2)*f2
#     g *= 10.
#     return g


# def gridded_gauss3(nx=100, ny=100, xmin=-3, xmax=3, ymin=-3, ymax=3, mesh=False, **kwargs):
#     """Create a data sample on a grid using :func:`gauss3`"""
#     x = np.linspace(xmin, xmax, nx)
#     y = np.linspace(ymin, ymax, ny)
#     xx, yy = np.meshgrid(x, y)
#     zz = gauss3(xx, yy, **kwargs)
#     if mesh:
#         return xx, yy, zz
#     return x, y, zz


# def random_gauss3(**kwargs):
#     """Create a data sample of random points using :func:`gauss3`"""
#     x, y = random_points(**kwargs)
#     z = gauss3(x, y, **kwargs)
#     return x, y, z


# def random_points(np=200, xmin=-3, xmax=3, ymin=-3, ymax=3, **kwargs):
#     """Generate random coordinates of points"""
#     x = P.rand(np)*(xmax-xmin)+xmin
#     y = P.rand(np)*(ymax-ymin)+ymin
#     return x, y
