"""Colour conversion matching R's grDevices::rgb and grDevices::colorRampPalette.

R's rgb() rounding depends on maxColorValue:
  * maxColorValue == 255  -> truncate toward zero   (C cast to int)
  * otherwise             -> round half away from zero  (floor(x + 0.5))
"""


def _hex_char(v):
    return f"{v:02X}"


def _to_int_round(scaled):
    return int(scaled + 0.5)


def _to_int_trunc(scaled):
    return int(scaled)


def rgb_to_hex_round(r, g, b, max_val, frgb=(1.0, 1.0, 1.0)):
    """Convert r,g,b to hex using R's rgb(..., maxColorValue = max_val) with rounding.

    Used for the initial raw-palette -> hex conversion in cpt() where max_val <= 1.
    """
    rr = r * frgb[0] / max_val * 255.0
    gg = g * frgb[1] / max_val * 255.0
    bb = b * frgb[2] / max_val * 255.0
    ir = min(max(_to_int_round(rr), 0), 255)
    ig = min(max(_to_int_round(gg), 0), 255)
    ib = min(max(_to_int_round(bb), 0), 255)
    return f"#{_hex_char(ir)}{_hex_char(ig)}{_hex_char(ib)}"


def _hex_to_rgb01(h):
    h = h.lstrip("#")
    return (int(h[0:2], 16) / 255.0, int(h[2:4], 16) / 255.0, int(h[4:6], 16) / 255.0)


def _lerp(a, b, t):
    return a + (b - a) * t


def _approxfun_eval(ctrl_x, ctrl_y, xout):
    """Linear interpolation matching R's stats::approxfun (method = 'linear')."""
    n = len(ctrl_x)
    if xout <= ctrl_x[0]:
        return ctrl_y[0]
    if xout >= ctrl_x[-1]:
        return ctrl_y[-1]
    lo = 0
    hi = n - 1
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if ctrl_x[mid] <= xout:
            lo = mid
        else:
            hi = mid
    x0, x1 = ctrl_x[lo], ctrl_x[hi]
    y0, y1 = ctrl_y[lo], ctrl_y[hi]
    return y0 + (y1 - y0) * (xout - x0) / (x1 - x0)


def _seq01(length):
    """Match R's seq.int(0, 1, length.out = length)."""
    if length == 1:
        return [0.0]
    step = 1.0 / (length - 1)
    return [i * step for i in range(length)]


def color_ramp_palette(colors):
    """Return a function(n) -> list of hex colours, matching grDevices::colorRampPalette.

    *colors* is a list of hex strings (the control points).
    """
    rgb01 = [_hex_to_rgb01(c) for c in colors]
    nc = len(rgb01)
    if nc == 1:
        rgb01 = rgb01 * 2
        nc = 2
    ctrl_x = _seq01(nc)

    def ramp(n):
        if n <= 0:
            return []
        xs = _seq01(n)
        out = []
        for x in xs:
            r = _approxfun_eval(ctrl_x, [p[0] for p in rgb01], x)
            g = _approxfun_eval(ctrl_x, [p[1] for p in rgb01], x)
            b = _approxfun_eval(ctrl_x, [p[2] for p in rgb01], x)
            # clamp to [0, 1] then scale to 0-255 (colorRamp's roundcolor * 255)
            r = min(max(r, 0.0), 1.0) * 255.0
            g = min(max(g, 0.0), 1.0) * 255.0
            b = min(max(b, 0.0), 1.0) * 255.0
            # rgb(..., maxColorValue = 255) TRUNCATES
            ir = _to_int_trunc(r)
            ig = _to_int_trunc(g)
            ib = _to_int_trunc(b)
            ir = min(max(ir, 0), 255)
            ig = min(max(ig, 0), 255)
            ib = min(max(ib, 0), 255)
            out.append(f"#{_hex_char(ir)}{_hex_char(ig)}{_hex_char(ib)}")
        return out

    return ramp
