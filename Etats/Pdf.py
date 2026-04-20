from fpdf import fpdf
import webbrowser
import tempfile
import os
from random import randint


class PlofPdf(fpdf.FPDF):
    def __init__(self, **args):
        super(PlofPdf, self).__init__(**args)
        self.rect_height = 12
        self.line_height = 7.5
        self.xm1 = (self.w / 2) - (self.l_margin * 2)
        self.xm2 = (self.w / 2) - self.l_margin
        self.column = 1

    def split(self):
        x1 = self.w / 2
        y1 = 0
        x2 = x1
        y2 = self.h
        self.dashed_line(x1, y1, x2, y2, dash_length=1, space_length=2)

    def set_column(self, column):
        self.column = column
        self.xm2 = (self.w / 2) - self.l_margin
        if self.column == 2:
            self.xm2 = self.w - self.r_margin

    def get_x_column(self):
        if self.column == 1:
            return self.l_margin
        if self.column == 2:
            return (self.w / 2) + self.l_margin

    def fullwidthrect(self, txt, y, border=1):
        x = self.get_x_column()
        self.set_font("Arial", size=12, style="B")
        self.rect(x, y, self.xm1, self.rect_height) if border == 1 else None
        self.set_y(y)
        self.set_x(x)
        self.multi_cell(w=self.xm1, h=self.rect_height / 2, txt=txt, border=0, align="C")

    def label(self, txt1, txt2, txt3, dots=True, big=False):
        x = self.get_x_column()
        self.set_font("Arial", size=12) if not big else self.set_font("Arial", size=14, style="B")
        self.set_x(x)
        self.write(self.line_height, txt1)
        if big:
            self.line_break()
            self.set_x(x)
        self.set_font("Arial", size=9, style="I") if not big else self.set_font("Arial", size=12, style="BI")
        self.write(self.line_height, txt2)
        if dots:
            x1 = self.get_x() + 1.5
            y1 = 2 + self.get_y() + self.line_height / 2
            self.dashed_line(x1, y1, self.xm2, y1, dash_length=0.2, space_length=2)

        self.write(self.line_height, txt3)
        self.write(self.line_height, "\n")

    def line_break(self, nb=1):
        for i in range(0, nb):
            self.write(self.line_height, "\n")

    def mcell(self, w, h, s, b=0, o='C'):
        x = self.get_x()
        y = self.get_y()
        self.multi_cell(w, h, s, b, o)
        self.set_xy(x + w, y)

    def show(self, filename, usetemp=True):
        if usetemp:
            #f = os.path.join(tempfile.gettempdir(), str(randint(10000, 99999)) + "-" + filename)
            f = os.path.join(tempfile.gettempdir(), filename)
        else:
            f = os.path.dirname(__file__) + "/" + filename
        self.output(f)
        webbrowser.open(f)
