#/usr/bin/env python3

from ddhf_hh_logo import DDHF_HH_Logo

class Logo_GnuPlot():

    def __init__(self, filename, **kwargs):
        logo = DDHF_HH_Logo()
        self.file = open(filename, "w")
        logo.logo_shapes(drawer=self)

    def move_to(self, x, y):
        self.file.write("\n%5.1f %5.1f\n" % (x, 1000 - y))

    def line_to(self, x, y):
        self.file.write("%5.1f %5.1f\n" % (x, 1000 - y))

if __name__ == "__main__":
    Logo_GnuPlot("hh_logo.gnuplot.txt")
