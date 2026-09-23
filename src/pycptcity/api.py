import random as _random
import re as _re

from . import _data
from ._color import color_ramp_palette, rgb_to_hex_round

_N_PALETTES = None


def _n():
    global _N_PALETTES
    if _N_PALETTES is None:
        _N_PALETTES = _data.palette_count()
    return _N_PALETTES


def cpt(pal="mpl_inferno", n=100, colorrampalette=False, rev=False, frgb=(1.0, 1.0, 1.0)):
    """Return a colour gradient as a list of hex strings or a ramp function.

    Parameters
    ----------
    pal : str
        Name of the colour gradient in the cpt-city archive.
    n : int
        Number of colours to return when *colorrampalette* is False.
    colorrampalette : bool
        If True return a callable ``f(n) -> list[str]`` equivalent to R's
        ``colorRampPalette``.  Use this with matplotlib / plotnine.
    rev : bool
        Reverse the gradient before interpolation.
    frgb : tuple of 3 floats
        Per-channel scaling factors for (red, green, blue).
    """
    m = _data.get_palette(pal)
    rows = m
    if rev:
        rows = rows[::-1]

    max_val = max(max(r, g, b) for r, g, b in rows)

    cols = [rgb_to_hex_round(r, g, b, max_val, frgb) for r, g, b in rows]
    ramp = color_ramp_palette(cols)

    if colorrampalette:
        return ramp
    return ramp(n)


def find_cpt(name, ignore_case=True, fixed=False):
    """Search palette names by keyword.  Returns a list of matching names."""
    names = _data.all_names()
    if fixed:
        if ignore_case:
            needle = name.lower()
            return [x for x in names if needle in x.lower()]
        return [x for x in names if name in x]
    flags = _re.IGNORECASE if ignore_case else 0
    pat = _re.compile(name, flags)
    return [x for x in names if pat.search(x)]


def lucky(n=100, colorrampalette=False, rev=False, message=True, nseed=None, frgb=(1.0, 1.0, 1.0)):
    """Pick a random palette -- "I'm Feeling Lucky" for colours."""
    rng = _random.Random(nseed)
    idx = rng.randrange(_n())
    names = _data.all_names()
    pal_name = names[idx]

    if message:
        print(f"Colour gradient: {pal_name}, number: {idx + 1}")

    return cpt(pal_name, n=n, colorrampalette=colorrampalette, rev=rev, frgb=frgb)


def show_cpt(x, label=True):
    """Display one or more palettes as horizontal colour bars (requires matplotlib)."""
    import matplotlib.pyplot as plt

    if isinstance(x, str):
        x = [x]
    nx = len(x)
    if nx <= 2:
        nrow, ncol = 1, max(nx, 1)
    elif nx <= 4:
        nrow, ncol = 2, 2
    elif nx <= 6:
        nrow, ncol = 2, 3
    elif nx <= 9:
        nrow, ncol = 3, 3
    elif nx <= 12:
        nrow, ncol = 3, 4
    elif nx <= 16:
        nrow, ncol = 4, 4
    elif nx <= 20:
        nrow, ncol = 4, 5
    elif nx <= 25:
        nrow, ncol = 5, 5
    elif nx <= 30:
        nrow, ncol = 5, 6
    elif nx <= 36:
        nrow, ncol = 6, 6
    elif nx <= 49:
        nrow, ncol = 7, 7
    elif nx <= 64:
        nrow, ncol = 8, 8
    elif nx <= 100:
        nrow, ncol = 10, 10
    elif nx <= 150:
        nrow, ncol = 10, 15
    elif nx <= 216:
        nrow, ncol = 12, 18
    elif nx <= 304:
        nrow, ncol = 16, 19
    elif nx <= 572:
        nrow, ncol = 22, 26
    else:
        raise ValueError("Please select fewer than 573 palettes at once.")

    fig, axes = plt.subplots(nrow, ncol, figsize=(ncol * 1.2, nrow * 0.6))
    axes = axes.flatten() if nx > 1 else [axes]
    for i, name in enumerate(x):
        cols = cpt(name, n=50)
        ax = axes[i]
        ax.imshow([cols], aspect="auto", interpolation="nearest")
        ax.set_xticks([])
        ax.set_yticks([])
        if label:
            ax.text(0.5, -0.05, str(i + 1), transform=ax.transAxes, ha="center", va="top")
    for j in range(nx, len(axes)):
        axes[j].set_visible(False)
    fig.tight_layout()
    plt.show()
    return x


def cpt_names():
    """Return a list of every palette name bundled in pycptcity."""
    return _data.all_names()
