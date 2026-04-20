# coding: utf-8
import os
import webbrowser
import tempfile
from random import randint
from .Html2Pdf import Html2Pdf
class PageOperationsSubsequenteRun():
    def __init__(self, template = None):
        self.template = template
        self.doPrint()

    def doPrint(self):
        converter = Html2Pdf()
        print "After Html2Pdf"
        dic = {
                "$numCF": "AA"
            }
        converter.setOrientation(orientation="Landscape")
        converter.setMarginLeft(margin=20)
        converter.setMarginRight(margin=5)
        src = os.path.dirname(__file__) + "/" + self.template
        print src
        dst = os.path.join(tempfile.gettempdir(), str(randint(10000, 99999)) + "-" + self.template + ".pdf")
        converter.generate(html=src, pdf=dst, dictionnary=dic)
        webbrowser.open(dst)
        self.merger.append(dst)

        #dstFinal = os.path.join(tempfile.gettempdir(), str(randint(10000, 99999)) + "-" + "Registre.pdf")
        #self.merger.write(dst)
        #webbrowser.open(dstFinal)
