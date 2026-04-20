
import tempfile
from Etats.codegenerator.ICodeImageGenerator import ICodeImageGenerator
from lib import qrcode

class QrCodeGenerator(ICodeImageGenerator):
    def generateImage(self, code):
        img = qrcode.make(code)
        type(img)
        filename = tempfile.mktemp('.png')
        img.save(filename)
        return filename
