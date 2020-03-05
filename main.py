import sys
import os
import textwrap

from lib.waveshare_epd import epd2in7
from PIL import Image,ImageDraw,ImageFont
import time

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

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

class page():

    # TODO Define this more!

    text = ""
    pageNumber = ""
    
    def getText(self):
        return self.text

    def __init__(self, newText, newPageNumber):
        self.text = newText
        self.pageNumber = newPageNumber

d = inkdisplay(epd2in7.EPD(), "fonts", "Ubuntu-R.ttf")

pages = {}

for i in range(2):
    pages[i] = page("This is a test of a very long string of text to see if the display will loop the text or just clip the end of this line." + str(i), i)

pageNumber = 0

key1 = 5
key2 = 6
key3 = 13
key4 = 19

GPIO.setup(key1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(key2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(key3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(key4, GPIO.IN, pull_up_down=GPIO.PUD_UP)

while True:
        key1state = GPIO.input(key1)
        key2state = GPIO.input(key2)
        key3state = GPIO.input(key3)
        key4state = GPIO.input(key4)

        if key1state == False:
            page = page + 1
            d.clear()
            d.newScreen()
            d.addText(pages[pageNumber].getText(), 10, 0)
            d.drawScreen()
            time.sleep(0.2)
        if key2state == False:
            d.clear()
            time.sleep(0.2)
        if key3state == False:
            d.clear()
            time.sleep(0.2)
        if key4state == False:
            d.clear()
            time.sleep(0.2)

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