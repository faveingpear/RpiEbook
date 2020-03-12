#!/usr/bin/python3

import sys
import os
import textwrap
import glob
import logging

from PyPDF2 import PdfFileReader
from lib.waveshare_epd import epd2in7
from PIL import Image,ImageDraw,ImageFont
import time

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

os.chdir("/home/pi/RpiEbook/")

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

    def addText(self, text, x, y, textformat):
        if textformat == True:
            newText = ""

            newText = self.wrapper.fill(text=text)
        
            self.draw.text((x, y), newText, font = self.font, fill = 0)
        else:
            self.draw.text((x, y), text, font = self.font, fill = 0)

    def addRectangle(self, x, y, widht, height):
        self.draw.rectangle((x,y,widht,height), outline=self.epd.GRAY1)

    def drawScreen(self):
        self.epd.display(self.epd.getbuffer(self.himage))

    def sleep(self):
        self.epd.sleep()

    def clear(self):
        self.epd.Clear(0xFF)

    # Init
    def __init__(self, newEpd, newFontsDir, newFont):
        self.epd = newEpd
        self.epd.init()
        self.font = ImageFont.truetype(os.path.join(newFontsDir, newFont), 12)

        self.wrapper = textwrap.TextWrapper(width=43)

class pageOfBook():

    text = ""
    pagenumber = ""

    def setText(self, newText):
        self.text = newText

    def setPageNumber(self, newPageNumber):
        self.pagenumber = newPageNumber

    def getText(self):
        return self.text

    def __init__(self, newText):
        self.text = newText

class book():

    # Array to hold each page class
    pages = {}

    # Title of the book
    title = ""
    # Total number of pages
    numberOfPages = 0
    # File path to the book
    pathToBook = ""

    # Variable to hold the wrapper object
    wrapper = ""

    currentpage = 0

    def startReading(self, newTitle, newPathToBook):
        self.title = newTitle
        self.pathToBook = newPathToBook

        self.wrapper = textwrap.TextWrapper(width=455)
        
        textForBook = self.wrapper.wrap(text=files.getTextfromPath(self.pathToBook))

        print(textForBook)

        for i in range(len(textForBook)):
            self.pages[i] = pageOfBook(textForBook[i])
        
        self.numberOfPages = len(self.pages)

        self.currentpage = files.updatePageFile(self.pathToBook,self.currentpage)

        self.displayPage()

    def displayPage(self):
        display.newScreen()
        print(self.pages[self.currentpage])
        display.addText(self.pages[self.currentpage], 2, 0, True)
        display.drawScreen()
        #s.updateClock()
        files.updatePageFile(self.pathToBook,self.currentpage)
        #s.addStatusBar()

    def nextPage(self):
        self.currentpage = self.currentpage + 1

        self.displayPage()

        files.updatePageFile(self.pathToBook,self.currentpage)

    def prevPage(self):
        self.currentpage = self.currentpage - 1

        self.displayPage()
        files.updatePageFile(self.pathToBook,self.currentpage)

class fileHandeling():

    def getTextfromPath(self, pathToBook):
        
        filetype = ""
        text = ""

        if ".txt" in pathToBook:
            filetype = ".txt"
        elif ".pdf" in pathToBook:
            filetype = ".pdf"

        if filetype == ".txt":
            file = open(pathToBook, "r")
            text = file.read()
            file.close()
            return text
        elif filetype == ".pdf":
            pdffile = PdfFileReader(open(pathToBook, "rb"))
            numberOfPages = pdffile.getNumPages()

            for i in range(numberOfPages):
                text = text + pdffile.getPage(i).extractText()

            return text

    def updatePageFile(self, pathToBook, currentpage):
        return 0

    def getPage(self, pathToBook):
        print("getting page")

display = inkdisplay(epd2in7.EPD(), "fonts", "UbuntuMono-R.ttf")
currentBook = book()
files = fileHandeling()

currentBook.startReading("Text","Books/Foxy Keith.txt")
time.sleep(5)
currentBook.nextPage()
time.sleep()
display.clear()
display.sleep()