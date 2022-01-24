#/usr/bin/env python3

# Fig 10 fra https://datamuseum.dk/bits/30002303

import itertools

# py38-beziers https://github.com/simoncozens/beziers.py
from beziers.point import Point
from beziers.path import BezierPath
from beziers.cubicbezier import CubicBezier

import math

class DDHF_HH_Logo():

    MARGIN = 2000

    # Matrix X-coords
    X0 = 65
    X1 = X0 + 189
    DX = 234
    X2 = X1 + DX
    X3 = X2 + DX
    X4 = X3 + 160

    # Matrix Y-coords
    Y0 = 82
    Y1 = Y0 + 180
    DY = 229
    Y2 = Y1 + DY
    Y3 = Y2 + DY
    Y4 = Y3 + 182

    # Core {Width, Height}
    CORE_WIDTH = 87
    CORE_HEIGHT = 37

    # Ground symbol top center
    GND_X = X4 + 76
    GND_Y = Y4 + 20

    # Slope lengths from (X1,Y3)...(X3,Y1) center line
    S0 = -150
    S1 =  338
    S2 = -485
    S3 =  425
    S4 = -312
    S5 =  None              # Match GND.x

    # Bend bezier control lines: angle and length
    BZ_ANGLE = math.radians(5)
    BZ_LENGTH = 93

    PEN_WIDTH1 = 9
    PEN_WIDTH2 = 6
    PEN_WIDTH3 = 12

    def __init__(self):
        ''' ... '''
        self.items = []
        self.lwidth = "1"

    def logo_shapes(self, drawer=None):
        if drawer is None:
            drawer = self
        self.drawer = drawer
        self.items = []

        if hasattr(self.drawer, "set_line_width"):
            self.drawer.set_line_width(self.PEN_WIDTH1)

        # Effective angle, cos, sin, distance
        self.core_angle = math.atan2(self.DX, self.DY)
        self.cosine = math.cos(self.core_angle)
        self.sine = math.sin(self.core_angle)
        dist = .5 * math.sqrt(self.DX * self.DX + self.DY * self.DY)

        s5 = self.S5
        if s5 is None:
            s5 = (self.GND_X - self.X3 ) / self.sine

        # Bend compensation distance (not param)
        compensation = .5 * dist * math.cos(math.pi - 2 * self.core_angle)

        # Bezier control lines in cartesian format
        bz_ax = self.BZ_LENGTH * math.sin(self.core_angle + self.BZ_ANGLE)
        bz_ay = self.BZ_LENGTH * math.cos(self.core_angle + self.BZ_ANGLE)
        bz_bx = self.BZ_LENGTH * math.sin(self.core_angle - self.BZ_ANGLE)
        bz_by = self.BZ_LENGTH * math.cos(self.core_angle - self.BZ_ANGLE)

        for x, y in (
            (self.X1, self.Y1),
            (self.X2, self.Y1),
            (self.X3, self.Y1),
            (self.X3, self.Y2),
            (self.X3, self.Y3),
            (self.X2, self.Y3),
            (self.X2, self.Y2),
            (self.X1, self.Y2),
            (self.X1, self.Y3),
        ):
            self.logo_core(x, y)

        # Y lines
        self.yline_up(self.X1)
        self.yline_down(self.X2)
        self.yline_up(self.X3)

        # X lines
        self.xline_right(self.Y1)
        self.xline_left(self.Y2)
        self.xline_right(self.Y3)

        # Sense line
        self.drawer.move_to(self.X0, self.Y3 + self.S0 * self.cosine)
        self.drawer.line_to(self.X1 + self.S0 * self.sine, self.Y3 + self.S0 * self.cosine)
        self.drawer.line_to(self.X1 - self.core_sdx, self.Y3 - self.core_sdy)
        self.drawer.move_to(self.X1 + self.core_sdx, self.Y3 + self.core_sdy)

        x = self.X1 + (self.S1 + compensation) * self.sine
        y = self.Y3 + (self.S1 + compensation) * self.cosine

        mx = .5 * (self.X1 + self.X2)
        my = .5 * (self.Y2 + self.Y3)
        x1 = mx + (self.S1 - compensation) * self.sine
        y1 = my + (self.S1 - compensation) * self.cosine
        self.drawer.line_to(x, y)
        self.bezier(
           (x, y),
           (x + bz_ax, y + bz_ay),
           (x1 + bz_bx, y1 + bz_by),
           (x1, y1),
        )

        self.drawer.line_to(self.X2 + self.core_sdx, self.Y3 + self.core_sdy)
        self.drawer.move_to(self.X2 - self.core_sdx, self.Y3 - self.core_sdy)

        self.drawer.line_to(self.X1 + self.core_sdx, self.Y2 + self.core_sdy)
        self.drawer.move_to(self.X1 - self.core_sdx, self.Y2 - self.core_sdy)

        x = mx + (self.S2 + compensation) * self.sine
        y = my + (self.S2 + compensation) * self.cosine

        x1 = self.X2 + (self.S2 - compensation) * self.sine
        y1 = self.Y2 + (self.S2 - compensation) * self.cosine
        self.bezier(
           (x, y),
           (x - bz_bx, y - bz_by),
           (x1 - bz_ax, y1 - bz_ay),
           (x1, y1),
        )

        self.drawer.line_to(self.X1 - self.core_sdx, self.Y1 - self.core_sdy)
        self.drawer.move_to(self.X1 + self.core_sdx, self.Y1 + self.core_sdy)

        self.drawer.line_to(self.X2 - self.core_sdx, self.Y2 - self.core_sdy)
        self.drawer.move_to(self.X2 + self.core_sdx, self.Y2 + self.core_sdy)

        self.drawer.line_to(self.X3 - self.core_sdx, self.Y3 - self.core_sdy)
        self.drawer.move_to(self.X3 + self.core_sdx, self.Y3 + self.core_sdy)

        x = self.X2 + (self.S3 + compensation) * self.sine
        y = self.Y2 + (self.S3 + compensation) * self.cosine

        mx = .5 * (self.X2 + self.X3)
        my = .5 * (self.Y1 + self.Y2)
        x1 = mx + (self.S3 - compensation) * self.sine
        y1 = my + (self.S3 - compensation) * self.cosine
        self.bezier(
            (x, y),
            (x + bz_ax, y + bz_ay),
            (x1 + bz_bx, y1 + bz_by),
            (x1, y1),
        )

        self.drawer.line_to(self.X3 + self.core_sdx, self.Y2 + self.core_sdy)
        self.drawer.move_to(self.X3 - self.core_sdx, self.Y2 - self.core_sdy)

        self.drawer.line_to(self.X2 + self.core_sdx, self.Y1 + self.core_sdy)
        self.drawer.move_to(self.X2 - self.core_sdx, self.Y1 - self.core_sdy)

        x = mx + (self.S4 + compensation) * self.sine
        y = my + (self.S4 + compensation) * self.cosine

        x1 = self.X3 + (self.S4 - compensation)  * self.sine
        y1 = self.Y1 + (self.S4 - compensation) * self.cosine
        self.bezier(
            (x, y),
            (x - bz_bx, y - bz_by),
            (x1 - bz_ax, y1 - bz_ay),
            (x1, y1),
        )

        self.drawer.line_to(self.X3 - self.core_sdx, self.Y1 - self.core_sdy)
        self.drawer.move_to(self.X3 + self.core_sdx, self.Y1 + self.core_sdy)

        x = self.X3 + s5 * self.sine
        y = self.Y1 + s5 * self.cosine
        self.drawer.line_to(x, y)
        self.drawer.line_to(self.GND_X, self.GND_Y)

        self.gnd()
        if self.drawer == self:
            return self.items

    def logo_core(self, x, y):

        def rot(dx, dy):
            return (
                x + dx * self.cosine + dy * self.sine,
                y + dy * self.cosine - dx * self.sine,
            )

        w = self.CORE_WIDTH / 2
        h = self.CORE_HEIGHT / 2
        w += self.PEN_WIDTH1 / 2
        h += self.PEN_WIDTH1 / 2
        self.c0 = rot(-w, -h)
        self.c1 = rot(-w,  h)
        self.c2 = rot( w,  h)
        self.c3 = rot( w, -h)

        # Calculate intersection with sense line
        self.core_sdx = h * self.sine
        self.core_sdy = h  * self.cosine

        # Calculate intersection with X and Y lines
        dx = x - self.c0[0]
        dy = self.c0[1] - y
        c = dy / self.sine
        self.core_dx = dx - c * self.cosine
        c = dx / self.cosine
        self.core_dy = c * self.sine - dy

        w = self.CORE_WIDTH / 2 - self.PEN_WIDTH2 / 2
        h = self.CORE_HEIGHT / 2 - self.PEN_WIDTH2 / 2
        self.d0 = rot(-w, -h)
        self.d1 = rot(-w,  h)
        self.d2 = rot( w,  h)
        self.d3 = rot( w, -h)

        self.drawer.move_to(*self.c0)
        for i in (self.c1, self.c2, self.c3, self.c0):
            self.drawer.line_to(*i)
        for i in (self.d0, self.d1, self.d2, self.d3, self.d0):
            self.drawer.line_to(*i)

    def move_to(self, x, y):
        self.items.append(("M", (x, y)))

    def line_to(self, x, y):
        self.items.append(("L", (x, y)))

    def bezier(self, coord1, coord2, coord3, coord4):
        i = getattr(self.drawer, "curve_to", None)
        if i:
            self.drawer.line_to(*coord1)
            i(*coord2, *coord3, *coord4)
        else:
            b = CubicBezier(*(Point(*j) for j in (coord1, coord2, coord3, coord4)))
            for i in range(1000):
                p = b.pointAtTime(i * .001)
                self.drawer.line_to(p.x, p.y)

    def xline_left(self, y):
        for x0, x1 in self.xline():
            self.drawer.move_to(x0, y)
            self.drawer.line_to(x1, y)

    def xline_right(self, y):
        for x0, x1 in reversed(list(self.xline())):
            self.drawer.move_to(x1, y)
            self.drawer.line_to(x0, y)

    def xline(self):
        yield self.X0, self.X1 - self.core_dx
        yield self.X1 + self.core_dx, self.X2 - self.core_dx
        yield self.X2 + self.core_dx, self.X3 - self.core_dx
        yield self.X3 + self.core_dx, self.X4

    def yline_down(self, x):
        for y0, y1 in self.yline():
            self.drawer.move_to(x, y0)
            self.drawer.line_to(x, y1)

    def yline_up(self, x):
        for y0, y1 in reversed(list(self.yline())):
            self.drawer.move_to(x, y1)
            self.drawer.line_to(x, y0)

    def yline(self):
        yield self.Y0, self.Y1 - self.core_dy
        yield self.Y1 + self.core_dy, self.Y2 - self.core_dy
        yield self.Y2 + self.core_dy, self.Y3 - self.core_dy
        yield self.Y3 + self.core_dy, self.Y4

    def gnd(self):
        ''' actual ground symbol '''
        for (dx, dy) in (
             (35, 0),
             (21, 25),
             (6, 49),
        ):
            self.drawer.move_to(self.GND_X - dx, self.GND_Y + dy)
            self.drawer.line_to(self.GND_X + dx, self.GND_Y + dy)
            dy += (self.PEN_WIDTH3 - self.PEN_WIDTH1)
            self.drawer.line_to(self.GND_X + dx, self.GND_Y + dy)
            self.drawer.line_to(self.GND_X - dx, self.GND_Y + dy)
            dy -= (self.PEN_WIDTH3 - self.PEN_WIDTH1)
            self.drawer.line_to(self.GND_X - dx, self.GND_Y + dy)

    def bbox(self):
        xlo = 9e9
        ylo = 9e9
        xhi = -9e9
        yhi = -9e9
        for i in self.logo_shapes():
            x, y = i[1]
            xlo = min(xlo, x)
            ylo = min(ylo, y)
            xhi = max(xhi, x)
            yhi = max(yhi, y)
        return xlo, ylo, xhi, yhi

if __name__ == "__main__":
    print("BBOX", DDHF_HH_Logo().bbox())
