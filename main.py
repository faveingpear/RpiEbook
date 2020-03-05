import sys
import os
import textwrap

from lib.waveshare_epd import epd2in7
from PIL import Image,ImageDraw,ImageFont
import time

class inkdisplay():

    fontsdir = ""
    font = "Ubuntu-R.ttf"
    epd = ""
    himage = ""
    draw = ""
    wrapper = ""

    # Ya set bois
    def setFont(self,newFont):
        self.font = newFont

    def setEpd(self, newEpd): #No reason to ever run this but it's here I guess 大丈夫
        self.epd = newEpd        

    def setFontsDir(self, newFontDir):
        self.fontsdir = newFontDir

    # The do some cool stuffers
    def newScreen(self):
        self.himage = Image.new('1', (self.epd.height, self.epd.width), 255)
        self.draw = ImageDraw.Draw(self.himage)

    def addText(self, text, x, y):

        newText = ""

        newText = self.wrapper.fill(text=text)

        print(newText)

        self.draw.text((x, y), newText, font = self.font, fill = 0)

    def drawScreen(self):
        self.epd.display(self.epd.getbuffer(self.himage))

    def clear(self):
        self.epd.Clear(0xFF)

    # Init
    def __init__(self, newEpd, newFontsDir, newFont):
        self.epd = newEpd
        self.epd.init()
        self.epd.Clear(0xFF)
        self.font = ImageFont.truetype(os.path.join(newFontsDir, newFont), 12)

        self.wrapper = textwrap.TextWrapper(width=45)

d = inkdisplay(epd2in7.EPD(), "fonts", "Ubuntu-R.ttf")

d.newScreen()
d.addText("This is a test of a very long string of text to see if the display will loop the text or just clip the end of this line.", 10, 0)
d.drawScreen()
d.clear()

# epd = epd2in7.EPD()

# epd.init()
# epd.Clear(0xFF)

# fontsdir = os.path.join('fonts')

# font24 = ImageFont.truetype(os.path.join(fontsdir, 'Ubuntu-R.ttf'), 24)

# Himage = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame
# draw = ImageDraw.Draw(Himage)

# draw.text((10, 0), 'hello worlddsdsdsaaaaaaaaaaaaaaaaaaaaaaaaaaaadsadsadadsadsadasdasdas', font = font24, fill = 0)

# epd.display(epd.getbuffer(Himage))

# epd.Clear(0xFF)