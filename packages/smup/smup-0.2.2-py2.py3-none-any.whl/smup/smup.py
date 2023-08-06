import numpy as np
from numba import njit
from matplotlib import pyplot as plt
import logging
from pathlib import Path


def isfloat(value):
    """
    Parameters
    ----------
    value: :class:`object`

    Returns
    -------
    :class:`bool`
        Can the object be converted to float?

    Examples
    --------

    >>> isfloat(3)
    True
    >>> isfloat("3.145")
    True
    >>> isfloat("Hello")
    False
    >>> isfloat("1+1")
    False
    """
    try:
        float(value)
        return True
    except (ValueError, TypeError):
        return False


@njit
def dist_2(center, points):
    """
    Parameters
    ----------
    center: :class:`~numpy.ndarray`
        2-D coordinate of the center.
    points: :class:`~numpy.ndarray`
        2-D coordinates of the points

    Returns
    -------
    :class:`~numpy.ndarray`
        Square of Euclidian distances between center and points.

    Examples
    --------

    Square distances between the origin and the points (0.3, 0.4), (1, 0), and (2, 1):

    >>> center = np.array([0, 0])
    >>> points = np.array([ [0.3, 1, 2], [0.4, 0, 1] ])
    >>> dist_2(center, points)
    array([0.25, 1.  , 5.  ])
    """
    return (points[0, :] - center[0]) ** 2 + (points[1, :] - center[1]) ** 2


def make_dist_p(p=2.0):
    """
    Parameters
    ----------
        p: :class:`float`
            Power to apply.

    Returns
    -------
    callable
        A jitted function that computes the sum of individual coordinate distances to the power of p.
        Correspond to a norm (up to re-scaling by 1/p) if p greater or equal to 1.

    Examples
    --------

    Let us fix a center and some points.

    >>> center = np.array([0, 0])
    >>> points = np.array([ [0.3, 1, 2], [0.4, 0, 1] ])

    Square distances between the origin and the points (0.3, 0.4), (1, 0), and (2, 1)
    (equivalent to :meth:`~smup.smup.dist_2`)

    >>> my_dist = make_dist_p(p=2)
    >>> my_dist(center, points)
    array([0.25, 1.  , 5.  ])

    Power of 1 (equivalent to :meth:`~smup.smup.dist_1`):

    >>> my_dist = make_dist_p(p=1)
    >>> my_dist(center, points)
    array([0.7, 1. , 3. ])

    Power of 3:

    >>> my_dist = make_dist_p(p=3)
    >>> my_dist(center, points)
    array([0.091, 1.   , 9.   ])

    Power of .5 (not a norm; convexity is lost):

    >>> my_dist = make_dist_p(p=.5)
    >>> my_dist(center, points)
    array([1.18017809, 1.        , 2.41421356])
    """
    def dist_p(center, points):
        return np.abs(points[0, :] - center[0]) ** p + np.abs(points[1, :] - center[1]) ** p
    return njit(dist_p)


@njit
def dist_1(center, points):
    """
    Parameters
    ----------
    center: :class:`~numpy.ndarray`
        2-D coordinate of the center.
    points: :class:`~numpy.ndarray`
        2-D coordinates of the points

    Returns
    -------
    :class:`~numpy.ndarray`
        Manhattan distances between center and points.

    Examples
    --------

    Manhattan distances between the origin and the points (0.3, 0.4), (1, 0), and (2, 1):

    >>> center = np.array([0, 0])
    >>> points = np.array([ [0.3, 1, 2], [0.4, 0, 1] ])
    >>> dist_1(center, points)
    array([0.7, 1. , 3. ])
    """
    return np.abs(points[0, :] - center[0]) + np.abs(points[1, :] - center[1])


@njit
def dist_inf(center, points):
    """
    Parameters
    ----------
    center: :class:`~numpy.ndarray`
        2-D coordinate of the center.
    points: :class:`~numpy.ndarray`
        2-D coordinates of the points

    Returns
    -------
    :class:`~numpy.ndarray`
        Inf-norm distances between center and points.

    Examples
    --------

    Inf-norm distances between the origin and the points (0.3, 0.4), (1, 0), and (2, 1):

    >>> center = np.array([0, 0])
    >>> points = np.array([ [0.3, 1, 2], [0.4, 0, 1] ])
    >>> dist_inf(center, points)
    array([0.4, 1. , 2. ])
    """
    return np.maximum(np.abs(points[0, :] - center[0]), np.abs(points[1, :] - center[1]))


def ascii_display(picture, centers):
    """
    Parameters
    ----------
    picture: :class:`~numpy.ndarray`
        A xXy array populated with integers 0, ..., s-1 that indicate the area of each pixel.
        Non covered pixels, if any, are represented by s.
    centers: :class:`~numpy.ndarray`
        Coordinates of the area centers

    Returns
    -------
    :class:`str`
        ASCII display of the matching.
    """
    _, s = centers.shape
    center_set = {(int(centers[0, i]), int(centers[1, i])) for i in range(s)}

    def pixel_to_txt(x, y):
        if (x, y) in center_set:
            return "X"
        else:
            return str(picture[y, x])

    h, w = picture.shape
    return "\n".join(" ".join(pixel_to_txt(x, y) for x in range(w)) for y in range(h))


@njit
def compute(x, y, s, distance_function, provisioning=1.0, heterogeneous_areas=False, seed=None):
    """
    Main function of the package. Computes the pictures.

    Parameters
    ----------
    x: :py:class:`int`
        Width of the picture (in pixels)
    y: :py:class:`int`
        Height of the picture (in pixels)
    s: :py:class:`int`
        Number of areas to display in the picture
    distance_function: callable
        Functions that computes distances between a center and points
    provisioning: :class:`float`
        Quota under/over provisioning. Values < 1 will make holes in the covering,
        while large values will make a Voronoi diagram.
    heterogeneous_areas: :class:`bool`
        Tells if the surfaces of site try to have same area or not.
    seed: :py:class:`int`, optional
        Random seed

    Returns
    -------
    picture: :class:`~numpy.ndarray`
        A xXy array populated with integers 0, ..., s-1 that indicate the area of each pixel.
        Non covered pixels, if any, are represented by s.
    centers: :class:`~numpy.ndarray`
        Coordinates of the area centers
    """
    xy = x * y
    # total pixel quota
    total_b = round(xy * provisioning)
    # Draw s centers
    if seed is not None:
        np.random.seed(seed)
    centers = np.random.rand(2, s)  # np.random.rand(2,s) #% Coordonnées des sites, penser à la déformation
    centers[0, :] *= x
    centers[1, :] *= y
    # Compute coordinates of all pixels
    points = np.zeros((2, xy))
    for xi in range(x):
        points[0, (xi * y):((xi + 1) * (y))] = xi + 0.5
    for yi in range(y):
        points[1, yi:xy:y] = yi + 0.5
    # Compute distances between all centers and all pixels
    dist = np.zeros(s * xy)
    for si in range(s):
        dist[si * xy:(si + 1) * xy] = distance_function(centers[:, si], points)
    # Sort the indexes by increasing distance
    edges = np.argsort(dist)
    # Prepare main loop
    if heterogeneous_areas:
        quotas = [0]+sorted([np.random.randint(total_b) for _ in range(s-1)])+[total_b]
        quotas = np.array([quotas[i+1]-quotas[i] for i in range(s)])
    else:
        bb = round(total_b / s)
        quotas = bb * np.ones(s, dtype=np.int32)
    results = s * np.ones((y, x), dtype=np.int32)
    pixels = xy
    # Main allocation loop
    for e in edges:
        # edge center
        si = e // xy
        # Check center needs to expand
        if quotas[si] != 0:
            # Pixel
            xyi = e % xy
            xi = xyi // y
            yi = xyi % y
            # Check pixel is free
            if results[yi, xi] == s:
                results[yi, xi] = si
                quotas[si] -= 1
                pixels -= 1
                if pixels == 0:
                    break
    return results, centers


class Smup:
    """
    Main interface with two main methods:
    :py:meth:`~smup.smup.Smup.compute`
    and
    :py:meth:`~smup.smup.Smup.display`.
    """

    def __init__(self):
        self.s = None
        self.picture = None
        self.centers = None

    def compute(self, x=1024, y=720, s=20, norm=2, provisioning=1.0, heterogeneous_areas=False, seed=None):
        """
        Parameters
        ----------
        x: :py:class:`int`
            Width of the picture (in pixels)
        y: :py:class:`int`
            Height of the picture (in pixels)
        s: :py:class:`int`
            Number of areas to display in the picture
        norm: :py:class:`int` or :py:class:`str` or :py:class:`float` or callable.
            Distance function to use.
            If norm is a positive float p (or string representation of), the p-norm will (which is not a norm if p<1).
            Optimized for 1, 2, or 'inf' but arbitrary positive float can be used
            If norm is a callable (must be jittable with proper signature), it will be used as such
            (not need to be an actual norm or even distance).
        provisioning: :class:`float`
            Quotas slack. Values < 1 will make holes in the covering, while large values will make a Voronoi diagram.
        heterogeneous_areas: :class:`bool`
            Tells if the surfaces of site try to have same area or not.
            If False, each area will have the same size up to roundings (about x*y/s).
            If True, (s-1) integers between 0 and x*y are draw uniformly independently. The sizes are given by the s
            intervals generated on [0, x*y].
        seed: :py:class:`int`, optional
            Random seed

        Returns
        -------
        None

        Examples
        --------

        We will use ASCII display for these examples. With the chosen seen, the site `0` should be a `ball`.

        With Euclidian distance, the ball is a disk.

        >>> my_smup = Smup()
        >>> my_smup.compute(x=30, y=20, s=3, norm=2, seed=42)
        >>> txt = ascii_display(my_smup.picture, my_smup.centers)
        >>> print(txt) # doctest: +SKIP
        1 1 1 1 1 1 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 1 1 1 1 1
        1 1 1 1 1 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 1 1 1 1 1
        1 1 1 1 1 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 1 1 1 1 1
        1 1 1 1 1 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 X 2 2 2 1 1 1 X 1
        1 1 1 1 1 2 2 2 0 0 0 0 0 0 2 2 2 2 2 2 2 2 2 2 2 1 1 1 1 1
        1 1 1 1 1 1 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 2 2 2 2 1 1 1 1 1
        1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 2 2 2 1 1 1 1 1
        1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 2 2 1 1 1 1 1
        1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 2 2 1 1 1 1 1
        1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 2 1 1 1 1 1
        1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 1 1 1 1 1
        1 1 1 0 0 0 0 0 0 0 0 X 0 0 0 0 0 0 0 2 2 2 2 2 2 1 1 1 1 1
        1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 1 1 1 1 1
        1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 1 1 1 1 1
        1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 1 1 1 1 1
        1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 1 1 1 1 1
        1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 2 1 1 1 1 1
        1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 2 2 1 1 1 1 1
        1 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 2 2 2 1 1 1 1 1
        1 1 1 1 1 1 1 1 0 0 0 0 0 0 1 1 1 1 1 2 2 2 2 2 1 1 1 1 1 1

        With Manhattan distance, the ball is a diamond.

        >>> my_smup.compute(x=30, y=20, s=3, norm=1, seed=42)
        >>> txt = ascii_display(my_smup.picture, my_smup.centers)
        >>> print(txt) # doctest: +SKIP
        1 1 1 1 1 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 1 1 1 1 1
        1 1 1 1 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 1 1 1 1 1
        1 1 1 2 2 2 2 2 2 2 2 0 2 2 2 2 2 2 2 2 2 2 2 2 2 1 1 1 1 1
        1 1 1 2 2 2 2 2 2 0 0 0 0 2 2 2 2 2 2 2 2 X 2 2 2 1 1 1 X 1
        1 1 1 2 2 2 2 2 2 0 0 0 0 0 2 2 2 2 2 2 2 2 2 2 2 1 1 1 1 1
        1 1 1 1 1 2 2 2 0 0 0 0 0 0 0 2 2 2 2 2 2 2 2 2 2 1 1 1 1 1
        1 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 2 2 2 1 1 1 1 1
        1 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 2 2 1 1 1 1 1
        1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 2 1 1 1 1 1
        1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 1 1 1 1 1
        1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 1 1 1 1 1
        1 0 0 0 0 0 0 0 0 0 0 X 0 0 0 0 0 0 0 0 0 2 2 2 2 1 1 1 1 1
        1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 1 1 1 1 1
        1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 1 1 1 1 1
        1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 1 1 1 1 1
        1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 2 1 1 1 1 1
        1 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 2 2 1 1 1 1 1
        1 1 1 1 1 1 1 0 0 0 0 0 0 0 0 0 1 2 2 2 2 2 2 2 2 1 1 1 1 1
        1 1 1 1 1 1 1 1 0 0 0 0 0 0 0 1 1 1 2 2 2 2 2 2 2 1 1 1 1 1
        1 1 1 1 1 1 1 1 1 0 0 0 0 0 1 1 1 1 1 2 2 2 2 2 2 1 1 1 1 1

        With Inf-norm distance, the ball is a (partial) square.

        >>> my_smup.compute(x=30, y=20, s=3, norm="inf", seed=42)
        >>> txt = ascii_display(my_smup.picture, my_smup.centers)
        >>> print(txt) # doctest: +SKIP
        1 1 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 1 1 1 1 1
        1 1 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 1 1 1 1 1
        1 1 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 1 1 1 1 1
        1 1 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 X 2 2 2 1 1 1 X 1
        1 1 2 2 2 2 0 2 2 0 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 1 1 1 1 1
        1 1 2 2 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 2 2 2 2 1 1 1 1 1
        1 1 2 2 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 2 2 2 1 1 1 1 1
        1 1 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 2 1 1 1 1 1 1
        1 1 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 1 1 1 1 1 1 1
        1 1 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 1 1 1 1 1 1 1 1
        1 2 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2 1 1 1 1 1 1 1 1 1
        1 2 2 2 0 0 0 0 0 0 0 X 0 0 0 0 0 0 0 2 1 1 1 1 1 1 1 1 1 1
        1 2 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 1 1 1 1
        1 2 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 1 1 1 1
        1 2 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 1 1 1 1
        1 2 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 1 1 1 1
        1 2 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 1 1 1 1
        1 2 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 1 1 1 1
        1 2 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 1 1 1 1
        1 2 2 2 2 2 2 2 2 2 2 2 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1

        Arbitrary power can be used for the norm (which may not be a norm in the end).

        >>> my_smup.compute(x=30, y=20, s=3, norm=.5, seed=42)
        >>> txt = ascii_display(my_smup.picture, my_smup.centers)
        >>> print(txt) # doctest: +SKIP
        1 1 1 1 1 1 2 2 2 2 0 0 2 2 2 2 2 2 2 2 2 2 2 2 2 1 1 1 1 1
        1 1 1 2 2 2 2 2 2 2 0 0 2 2 2 2 2 2 2 2 2 2 2 2 2 1 1 1 1 1
        2 2 2 2 2 2 2 2 2 2 0 0 2 2 2 2 2 2 2 2 2 2 2 2 2 1 1 1 1 1
        2 2 2 2 2 2 2 2 2 2 0 0 2 2 2 2 2 2 2 2 2 X 2 2 2 1 1 1 X 1
        1 1 2 2 2 2 2 2 2 0 0 0 0 2 2 2 2 2 2 2 2 2 2 2 2 1 1 1 1 1
        1 1 1 1 1 2 2 2 0 0 0 0 0 0 2 2 2 2 2 2 2 2 2 2 2 1 1 1 1 1
        1 1 1 1 1 1 1 0 0 0 0 0 0 0 0 2 2 2 2 2 2 2 2 2 2 1 1 1 1 1
        1 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 2 2 2 1 1 1 1 1
        1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 2 2 1 1 1 1 1
        1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 1 1 1 1 1
        1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 1 1 1 1 1
        0 0 0 0 0 0 0 0 0 0 0 X 0 0 0 0 0 0 0 0 0 2 2 2 0 1 1 1 1 1
        0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2 0 2 1 1 1 1 1
        1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 1 1 1 1 1
        1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 1 1 1 1 1
        1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 1 2 2 2 2 2 2 2 1 1 1 1 1
        1 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 1 1 2 2 2 2 2 2 2 1 1 1 1 1
        1 1 1 1 1 1 1 0 0 0 0 0 0 0 0 1 1 1 1 2 2 2 2 2 2 1 1 1 1 1
        1 1 1 1 1 1 1 1 0 0 0 0 0 0 1 1 1 1 1 2 2 2 2 2 2 1 1 1 1 1
        1 1 1 1 1 1 1 1 1 0 0 0 0 0 1 1 1 1 1 1 2 2 2 2 1 1 1 1 1 1

        You can also specify a custom function and use it. The function, which may not be a norm of even a distance,
        must be numba compatible with a signature (2,), (2, X) -> (X,). Example:

        >>> def diagonal_polarization(center, points):
        ...     return (points[0, :] - center[0] + points[1, :] - center[1])**2
        >>> my_smup.compute(x=30, y=20, s=3, norm=diagonal_polarization, seed=42)
        >>> txt = ascii_display(my_smup.picture, my_smup.centers)
        >>> print(txt) # doctest: +SKIP
        2 2 2 2 2 2 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 1 1
        2 2 2 2 2 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 1 1 1
        2 2 2 2 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 1 1 1 1
        2 2 2 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0 0 0 0 X 2 2 2 1 1 1 X 1
        2 2 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 1 1 1 1 1 1
        2 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 1 1 1 1 1 1 1
        2 2 2 2 2 2 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 1 1 1 1 1 1 1 1
        2 2 2 2 2 2 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 1 1 1 1 1 1 1 1 1
        2 2 2 2 2 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 1 1 1 1 1 1 1 1 1 1
        2 2 2 2 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 1 1 1 1 1 1 1 1 1 1 1
        2 2 2 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 1 1 1 1 1 1 1 1 1 1 1 1
        2 2 0 0 0 0 0 0 0 0 0 X 0 2 2 2 2 1 1 1 1 1 1 1 1 1 1 1 1 1
        2 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 1 1 1 1 1 1 1 1 1 1 1 1 1 2
        0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 1 1 1 1 1 1 1 1 1 1 1 1 1 1 2
        0 0 0 0 0 0 0 0 0 0 2 2 2 2 1 1 1 1 1 1 1 1 1 1 1 1 1 1 2 2
        0 0 0 0 0 0 0 0 0 2 2 2 2 1 1 1 1 1 1 1 1 1 1 1 1 1 1 2 2 2
        0 0 0 0 0 0 0 0 2 2 2 2 1 1 1 1 1 1 1 1 1 1 1 1 1 1 2 2 2 2
        0 0 0 0 0 0 0 2 2 2 2 1 1 1 1 1 1 1 1 1 1 1 1 1 2 2 2 2 2 2
        0 0 0 0 0 0 2 2 2 2 1 1 1 1 1 1 1 1 1 1 1 1 1 1 2 2 2 2 2 2
        0 0 0 0 0 2 2 2 2 1 1 1 1 1 1 1 1 1 1 1 1 1 1 2 2 2 2 2 2 2

        Unclear norm defaults to Euclidian norm (and a warning is issued).

        >>> my_smup.compute(x=30, y=20, s=3, norm="??", seed=42)
        >>> txt = ascii_display(my_smup.picture, my_smup.centers)
        >>> print(txt) # doctest: +SKIP
        1 1 1 1 1 1 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 1 1 1 1 1
        1 1 1 1 1 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 1 1 1 1 1
        1 1 1 1 1 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 1 1 1 1 1
        1 1 1 1 1 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 X 2 2 2 1 1 1 X 1
        1 1 1 1 1 2 2 2 0 0 0 0 0 0 2 2 2 2 2 2 2 2 2 2 2 1 1 1 1 1
        1 1 1 1 1 1 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 2 2 2 2 1 1 1 1 1
        1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 2 2 2 1 1 1 1 1
        1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 2 2 1 1 1 1 1
        1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 2 2 1 1 1 1 1
        1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 2 1 1 1 1 1
        1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 1 1 1 1 1
        1 1 1 0 0 0 0 0 0 0 0 X 0 0 0 0 0 0 0 2 2 2 2 2 2 1 1 1 1 1
        1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 1 1 1 1 1
        1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 1 1 1 1 1
        1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 1 1 1 1 1
        1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 1 1 1 1 1
        1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 2 1 1 1 1 1
        1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 2 2 1 1 1 1 1
        1 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 2 2 2 1 1 1 1 1
        1 1 1 1 1 1 1 1 0 0 0 0 0 0 1 1 1 1 1 2 2 2 2 2 1 1 1 1 1 1

        Heterogeneous areas make site quotas uneven.

        >>> my_smup.compute(x=30, y=20, s=3, heterogeneous_areas=True, seed=42)
        >>> txt = ascii_display(my_smup.picture, my_smup.centers)
        >>> print(txt)
        1 1 1 1 1 1 2 2 0 0 0 2 2 2 2 2 2 2 2 2 2 2 2 2 2 1 1 1 1 1
        1 1 1 1 1 0 0 0 0 0 0 0 2 2 2 2 2 2 2 2 2 2 2 2 2 1 1 1 1 1
        1 1 1 1 0 0 0 0 0 0 0 0 2 2 2 2 2 2 2 2 2 2 2 2 2 1 1 1 1 1
        1 1 1 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 2 2 X 2 2 2 1 1 1 X 1
        1 1 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 2 2 2 2 2 1 1 1 1 1
        1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 2 2 2 2 1 1 1 1 1
        1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 2 2 2 1 1 1 1 1
        0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 2 2 1 1 1 1 1
        0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 2 2 1 1 1 1 1
        0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 2 1 1 1 1 1
        0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 1 1 1 1 1
        0 0 0 0 0 0 0 0 0 0 0 X 0 0 0 0 0 0 0 0 2 2 2 2 2 1 1 1 1 1
        0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 1 1 1 1 1
        0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 1 1 1 1 1
        0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 1 1 1 1 1
        0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2 1 1 1 1 1
        0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 1 1 1 1 1
        1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 1 1 1 1 1
        1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 1 1 1 1 1
        1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2 1 1 1 1 1 1 1

        Underprovisioned quotas will create *holes*.

        >>> my_smup.compute(x=30, y=20, s=3, provisioning=.4, seed=42)
        >>> txt = ascii_display(my_smup.picture, my_smup.centers)
        >>> print(txt)
        3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 2 2 2 2 2 2 2 2 2 1 1 1 1 1
        3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 2 2 2 2 2 2 2 2 2 1 1 1 1 1
        3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 2 2 2 2 2 2 2 2 2 1 1 1 1 1
        3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 2 2 2 2 2 X 2 2 2 1 1 1 X 1
        3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 2 2 2 2 2 2 2 2 2 1 1 1 1 1
        3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 2 2 2 2 2 2 2 2 2 1 1 1 1 1
        3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 2 2 2 2 2 2 2 2 2 1 1 1 1 1
        3 3 3 3 3 3 3 3 3 0 0 0 0 3 3 3 3 2 2 2 2 2 2 2 2 1 1 1 1 1
        3 3 3 3 3 3 3 3 0 0 0 0 0 0 0 3 3 3 2 2 2 2 2 2 2 1 1 1 1 1
        3 3 3 3 3 3 3 0 0 0 0 0 0 0 0 0 3 3 3 3 1 2 2 1 1 1 1 1 1 1
        3 3 3 3 3 3 0 0 0 0 0 0 0 0 0 0 3 3 3 3 3 1 1 1 1 1 1 1 1 1
        3 3 3 3 3 3 0 0 0 0 0 X 0 0 0 0 3 3 3 3 3 3 1 1 1 1 1 1 1 1
        3 3 3 3 3 3 0 0 0 0 0 0 0 0 0 0 3 3 3 3 3 3 3 3 1 1 1 1 1 1
        3 3 3 3 3 3 0 0 0 0 0 0 0 0 0 0 3 3 3 3 3 3 3 3 3 3 1 1 1 1
        3 3 3 3 3 3 3 0 0 0 0 0 0 0 0 0 3 3 3 3 3 3 3 3 3 3 3 3 3 3
        3 3 3 3 3 3 3 3 0 0 0 0 0 0 0 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3
        3 3 3 3 3 3 3 3 3 0 0 0 0 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3
        3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3
        3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3
        3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3

        Overprovisioned quotas will create a Voronoi diagram.

        >>> my_smup.compute(x=30, y=20, s=3, provisioning=4, seed=42)
        >>> txt = ascii_display(my_smup.picture, my_smup.centers)
        >>> print(txt)
        0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 2 2 2 2 2 2 2 2 1 1 1 1 1
        0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 2 2 2 2 2 2 2 1 1 1 1 1
        0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 2 2 2 2 2 2 2 1 1 1 1 1
        0 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 2 2 X 2 2 2 1 1 1 X 1
        0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 2 2 2 2 2 1 1 1 1 1
        0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 2 2 2 2 1 1 1 1 1
        0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 2 2 2 1 1 1 1 1
        0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 2 2 1 1 1 1 1
        0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 2 2 1 1 1 1 1
        0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 2 1 1 1 1 1
        0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 1 1 1 1 1
        0 0 0 0 0 0 0 0 0 0 0 X 0 0 0 0 0 0 0 0 2 2 2 2 2 1 1 1 1 1
        0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 1 1 1 1 1
        0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 1 1 1 1 1
        0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 1 1 1 1 1
        0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2 1 1 1 1 1
        0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 1 1 1 1 1
        0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 1 1
        0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 1 1
        0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 1
        """
        self.s = s
        if str(norm) == 'inf':
            dist = dist_inf
        elif str(norm) == '1':
            dist = dist_1
        elif str(norm) == '2':
            dist = dist_2
        elif isfloat(norm):
            dist = make_dist_p(float(norm))
        elif callable(norm):
            dist = njit(norm)
        else:
            logging.warning(f"Norm {norm} unknown, defaulting to 2-norm.")
            dist = dist_2
        self.picture, self.centers = compute(x, y, s, dist, provisioning, heterogeneous_areas, seed)

    def display(self, cmap='jet', draw_centers=False, center_size=20, save=None):
        """

        Parameters
        ----------
        cmap: :class:`str`
            Matplotlib colormap to use. Defaults to 'jet'
        draw_centers: :class:`bool`
            Draw centers of areas. Defaults to False.
        center_size: :class:`int`
            Size of centers, if drawn. Defaults to 20.
        save: :class:`str` ot :class:`~pathlib.Path`, optional
            Filename for saving picture.

        Returns
        -------
        None

        Examples
        --------

        See :doc:`/use` for graphical examples. Here we just show the file saving feature.

        >>> from pathlib import Path
        >>> import tempfile
        >>> my_smup = Smup()
        >>> my_smup.compute(x=30, y=20, s=3, norm=2, seed=42)
        >>> with tempfile.TemporaryDirectory() as tmpdirname:
        ...     fn = tmpdirname/Path("picture.png")
        ...     my_smup.display(draw_centers=True, save=fn)
        ...     size=fn.stat().st_size
        >>> size
        55984
        """
        plt.figure(figsize=(40, 30))
        img = plt.imshow(self.picture / self.s)
        plt.contour(self.picture, levels=2 * self.s, colors='black')
        img.set_cmap(cmap)
        if draw_centers:
            plt.plot(self.centers[0, :], self.centers[1, :], 'k.', markersize=center_size)
        plt.xticks([], [])
        plt.yticks([], [])
        if save and (isinstance(save, str) or isinstance(save, Path)):
            plt.savefig(save, bbox_inches='tight')
