"""pycptcity: cpt-city colour gradients for Python / plotnine.

Quick start::

    from pycptcity import cpt, find_cpt, lucky, show_cpt

    cols = cpt("mpl_inferno", n = 100)
    find_cpt("temperature")
    lucky(nseed = 42)

plotnine::

    from plotnine import scale_colour_gradientn, scale_fill_gradientn
    + scale_fill_gradientn(colours = cpt("mpl_inferno", n = 256))
"""

from .api import cpt, cpt_names, find_cpt, lucky, show_cpt

__version__ = "2.3.0"
__all__ = ["cpt", "find_cpt", "lucky", "show_cpt", "cpt_names", "__version__"]
