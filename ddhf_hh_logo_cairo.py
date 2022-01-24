#/usr/bin/env python3

import cairo

from ddhf_hh_logo import DDHF_HH_Logo

def Logo_Cairo(ctx):
    ctx.set_line_cap(cairo.LineCap.ROUND)
    ctx.set_line_join(cairo.LineCap.ROUND)
    DDHF_HH_Logo().logo_shapes(drawer=ctx)
    ctx.stroke()

if __name__ == "__main__":
    for size in (100, 1000,):
        surface = cairo.SVGSurface(
            "hh_logo_%d.svg" % size,
            size,
            size,
        )
        ctx = cairo.Context(surface)
        ctx.scale(size/1000, size/1000)
        Logo_Cairo(ctx)
