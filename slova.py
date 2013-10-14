#coding=UTF-8
import codecs
import reportlab.rl_config
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.units import cm, mm
from reportlab.lib import pagesizes
import sys

reportlab.rl_config.TTFSearchpath = './'
pdfmetrics.registerFont(TTFont('DejaVuSans-Bold','DejaVuSans-Bold.ttf'))

def readTexts(filename):
    file = codecs.open(filename, encoding='utf-8')
    lines = file.readlines()
    file.close()
    return lines

def fitText(pdf, text, page, fontName, encoding):
    fontSize = 10
    w = pdf.stringWidth(text, fontName, fontSize)
    while (w < page[0]*0.9 and fontSize < page[1]*0.9):
        fontSize = fontSize + 1
        w = pdf.stringWidth(text, fontName, fontSize)
    fontSize = fontSize - 1
    return fontSize

def centerString(pdf, page, text):
    fontName = "DejaVuSans-Bold"
    encoding = "utf-8"
    texts = text.split(" ")
    fontSize = page[1]
    for t in texts:
        fontSize = min(fitText(pdf, t, (page[0],page[1]/len(texts)), fontName, encoding), fontSize)
    pdf.setFont(fontName, fontSize)
    i = 0
    for t in texts:
       pdf.drawCentredString(page[0]/2, page[1]/(len(texts)+1)*(len(texts)-i) -fontSize/3, t.strip())
       i = i+1
    

def createPDF(pdf, texts):
    page = pagesizes.landscape(pagesizes.A4)
    pdf.setFillColorRGB(0.0, 0.0, 0.0)
    pdf.setPageSize(page)
    for text in texts:
        centerString(pdf, page, text)
        pdf.showPage()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "usage: kufr.py filename [filenames...]"
    else:
        for arg in sys.argv[1:]:
            try:
                # read the file
                texts = readTexts(arg)
                filename = arg + ".pdf"
                print "Creating file '"+filename+"'...",
            
                try:
                    pdf = canvas.Canvas(filename)
                    createPDF(pdf, texts)
                    pdf.save()
                    print "done."
                except Exception, e:
                    print "failed."
                    print e

            except IOError, e:
                print "Can not read file '" + arg + "'"
                print e
            

