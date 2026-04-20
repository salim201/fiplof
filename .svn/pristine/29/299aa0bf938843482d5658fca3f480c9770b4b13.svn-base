import pdfkit
import os
import re

class Html2Pdf:
    def __init__(self):
        self.orientation="Portrait"
        self.format = "A4"
        self.margin_left = 10
        self.margin_right = 10

    def setMarginLeft(self, margin):
        self.margin_left = margin

    def setMarginRight(self, margin):
        self.margin_right = margin

    def setOrientation(self, orientation):
        self.orientation = orientation

    def setFormat(self, format):
        self.format = format

    def generate(self, html, pdf, dictionnary={}):
        tmp = html + ".tmp.html"
        try:
            finput = open(html)
        except Exception as err:
            print (err)

        foutput = open(tmp, "w")
        try:
            s = finput.read()
        except Exception as err:
            print (err)
        for i in dictionnary:
            if isinstance(dictionnary[i], str):
                s = s.replace(i, dictionnary[i])
            if isinstance(dictionnary[i], list):
                s = self.replace_list(s, i, dictionnary[i])
        foutput.write(s)
        finput.close()
        foutput.close()
        config = pdfkit.configuration(wkhtmltopdf=os.path.dirname(__file__) + '/pdfkit/wkhtmltopdf/bin/wkhtmltopdf.exe')
        options = {'orientation': self.orientation, 'page-size': self.format, 'margin-left': self.margin_left , 'margin-right': self.margin_right }
        pdfkit.from_file(tmp, pdf, configuration=config, options=options)
        os.remove(tmp)

    def replace_list(self, string, key, values):
        regex = re.compile("\{REPEAT \\" + key + ":|\}|\{ENDREPEAT \\" + key + "\}")
        parts = regex.split(string)
        if len(parts) < 3:
            return
        variable = parts[1]
        subject = parts[2]
        all_replaced = ""
        for row in values:
            replaced = subject
            for i in row:
                try:
                    if row[i] is None:
                        r = " - "
                    else:
                        r = str(row[i]).encode('utf-8')
                except Exception as e:
                    r = ""
                replaced = replaced.replace(variable + "." + i, r)
            all_replaced += replaced

        pattern = re.compile("\{REPEAT \\" + key + ":\$.+\}.+\{ENDREPEAT \\" + key + "\}", re.DOTALL)
        s = pattern.search(string)
        if s is None:
            return string
        return (string[:s.start()] + all_replaced + string[s.end():])
