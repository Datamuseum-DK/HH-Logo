#/usr/bin/env python3

import math

from ddhf_hh_logo import DDHF_HH_Logo

class Logo_AxiDraw():

    LIFT = 100

    SPEED = .4

    def __init__(self, filename, scale=10):
        self.file = open(filename, "w")
        self.cur_x = 0
        self.cur_y = 0
        self.pen = 0
        self.scale = scale
        self.file.write("EM,1,1\n")
        self.file.write("SP,0,200\n")
        DDHF_HH_Logo().logo_shapes(drawer=self)
        self.move_to(0,0)

    def move_to(self, x, y):
        if self.pen:
            self.file.write("SP,0,%d\n" % self.LIFT)
            self.file.write("XM,%d,0,0\n" % self.LIFT)
            self.pen = False
        self.goto(x, y)

    def line_to(self, x, y):
        if not self.pen:
            self.file.write("SP,1,%d\n" % self.LIFT)
            self.file.write("XM,%d,0,0\n" % self.LIFT)
            self.pen = True
        self.goto(x, y)

    def goto(self, x, y):
        x = int(x * self.scale)
        y = int(y * self.scale)
        if x != self.cur_x or y != self.cur_y:
            l = math.hypot(x - self.cur_x, y - self.cur_y)
            e = self.SPEED * l
            self.file.write("XM,%d,%d,%d\n" % (1 + e, x - self.cur_x, y - self.cur_y))
            self.cur_x = x
            self.cur_y = y

if __name__ == "__main__":
    Logo_AxiDraw("hh_logo_axidraw.txt")
