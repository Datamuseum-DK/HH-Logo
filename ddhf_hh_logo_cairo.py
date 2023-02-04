#/usr/bin/env python3

import cairo

from ddhf_hh_logo import DDHF_HH_Logo

TA_COLOR=(0, .3, 1)
TEST_COLOR=(0xff/0xff, 0xd7/0xff, 0x00/0xff)

def Logo_Cairo(ctx, txt=None, txtsz=None, txtcol=None):
    if txt:
        ctx.save()
        ctx.set_source_rgb(*txtcol)
        ctx.set_font_size(txtsz)
        ctx.select_font_face("Arial",
                     cairo.FONT_SLANT_NORMAL,
                     cairo.FONT_WEIGHT_NORMAL)
        xbearing, ybearing, width, height, dx, dy = ctx.text_extents(txt)
        ctx.move_to(500 - width/2, 500 + height/2)
        ctx.show_text(txt)
        ctx.restore()
    ctx.set_line_cap(cairo.LineCap.ROUND)
    ctx.set_line_join(cairo.LineCap.ROUND)
    DDHF_HH_Logo().logo_shapes(drawer=ctx)
    ctx.stroke()

def Logo_TA_Cairo(ctx):
    Logo_Cairo(ctx, txt="TA", txtsz=700, txtcol=TA_COLOR)
    

if __name__ == "__main__":
    # The basic logos
    for test in (True, False):
        for fn, func,size in (
             ("hh_logo_100", Logo_Cairo, 100),
             ("hh_logo_ta_100", Logo_TA_Cairo, 100),
        ):
            if test:
                fn += "_test"
            fn += ".svg"
 
            surface = cairo.SVGSurface(fn, size, size)
            ctx = cairo.Context(surface)
            if test:
                ctx.save()
                ctx.set_source_rgb(*TEST_COLOR)
                ctx.paint()
                ctx.fill()
                ctx.restore()
            ctx.scale(size/1000, size/1000)
            func(ctx)

        # Make a favicon with light gray background
        for fn, func,size in (
             ("favicon", Logo_Cairo, 100),
             ("favicon_ta", Logo_TA_Cairo, 100),
        ):
            if test:
                fn += "_test"
            fn += ".svg"
 
            surface = cairo.SVGSurface(fn, size, size)
            ctx = cairo.Context(surface)
            ctx.save()
            if test:
                ctx.set_source_rgb(*TEST_COLOR)
            else:
                ctx.set_source_rgb(0.9, 0.9, 0.9)
            ctx.paint()
            ctx.fill()
            ctx.restore()
            ctx.scale(size/1000, size/1000)
            func(ctx)
