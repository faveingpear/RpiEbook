#!/usr/bin/python3

# So I made way too much progress today. Right now it's functional, there is not much to it but it does what my goal was to do and I used OOP. 
# TODO  book, etc. Add settings menu so that stuff like font and font size can be changed.
# It's too late but day 1 was a hell of a lot of fun!

# TODO Make a menu that used highlighted sections so I can render more than one option on the screen at once
# TODO Work on settings menu to change fontsizes, font, words per page, etc..
# TODO Work on making the program more stable for example making sure out of bound errors can happen
# TODO Figure out how the licences work with the waveshare_epd driver
# TODO Use public domain fonts because Im not sure if I am really allowed to use Ubuntu Fonts 
# TODO LOGGING
# TODO Working on maybe removie some class ex: reading Im not sure if it is really needed most of what It does can just be put into book
# TODO General Optimization
# TODO Maybe research if exception based GPIO is a thing so I don't need a mainloop to check for the GPIO every 0.5s 
# TODO 

import sys
import os
import textwrap
import glob
import logging

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

class page():

    # TODO Define this more!

    text = ""
    pageNumber = ""
    
    def getText(self):
        return self.text

    def __init__(self, newText, newPageNumber):
        self.text = newText
        self.pageNumber = newPageNumber

class book():

    pages = {}

    title = ""
    numberOfPages = ""
    wrapper = ""
    filePath = ""

    currentpage = 0

    def newBook(self, newTitle, newPath):
        self.currentpage = 0
        self.changeBook(page, newTitle, newPath)
        d.newScreen()
        d.addText(self.getTextOfPage(self.currentpage), 2, 0, True)
        d.drawScreen()

    def nextPage(self):
        try:
            self.currentpage = self.currentpage + 1
            f.saveCurrentPage(self.getCurrentPage(),self.getFilePath())
            d.newScreen()
            d.addText(self.getTextOfPage(self.currentpage), 2, 0, True)
            s.updateClock()
            s.updatePage(self.currentpage)
            s.addStatusBar()
            d.drawScreen()
        except:
            self.currentPage = self.currentPage - 1
            print("Can't go foward!")

    def prevPage(self):
        try:
            self.currentpage = self.currentpage - 1
            f.saveCurrentPage(self.getCurrentPage(),self.getFilePath())
            d.newScreen()
            d.addText(self.getTextOfPage(self.currentpage), 2, 0, True)
            s.updateClock()
            s.updatePage(self.currentpage)
            s.addStatusBar()
            d.drawScreen()
        except:
            self.currentPage = self.currentPage + 1
            print("Can't go back!")

    def getCurrentPage(self):
        return self.currentpage

    def startreading(self, title, pathToBook):
        self.currentpage = f.loadCurrentPage(pathToBook)
        self.changeBook(page, title, pathToBook)
        d.newScreen()
        d.addText(self.getTextOfPage(self.currentpage), 2, 0, True)
        s.updateClock()
        s.updatePage(self.currentpage)
        s.addStatusBar()
        d.drawScreen()

    def getFilePath(self):
        return self.filePath

    def getTextOfPage(self, page):
        return self.pages[page].getText()

    def changeBook(self, pagesClass, title, pathToBook):
        self.title = title
        self.wrapper = textwrap.TextWrapper(width=455)

        self.filePath = pathToBook

        file = open(pathToBook)

        self.createPages(pagesClass, file.read())

        file.close()

    def createPages(self, pagesClass, text):

        newText = self.wrapper.wrap(text=text)

        for i in range(len(newText)):
            self.pages[i] = pagesClass(newText[i], i)

# class reading():

#     currentpage = 0

#     def newBook(self, newTitle, newPath):
#         self.currentpage = 0
#         b.changeBook(page, newTitle, newPath)
#         d.newScreen()
#         d.addText(b.getTextOfPage(self.currentpage), 2, 0, True)
#         d.drawScreen()

#     def nextPage(self):
#         try:
#             self.currentpage = self.currentpage + 1
#             f.saveCurrentPage(r.getCurrentPage(),b.getFilePath())
#             d.newScreen()
#             d.addText(b.getTextOfPage(self.currentpage), 2, 0, True)
#             s.updateClock()
#             s.updatePage(self.currentpage)
#             s.addStatusBar()
#             d.drawScreen()
#         except:
#             self.currentPage = self.currentPage - 1
#             print("Can't go foward!")

#     def prevPage(self):
#         try:
#             self.currentpage = self.currentpage - 1
#             f.saveCurrentPage(r.getCurrentPage(),b.getFilePath())
#             d.newScreen()
#             d.addText(b.getTextOfPage(self.currentpage), 2, 0, True)
#             s.updateClock()
#             s.updatePage(self.currentpage)
#             s.addStatusBar()
#             d.drawScreen()
#         except:
#             self.currentPage = self.currentPage + 1
#             print("Can't go back!")

#     def getCurrentPage(self):
#         return self.currentpage

#     def startreading(self, title, pathToBook):
#         self.currentpage = f.loadCurrentPage(pathToBook)
#         b.changeBook(page, title, pathToBook)
#         d.newScreen()
#         d.addText(b.getTextOfPage(self.currentpage), 2, 0, True)
#         s.updateClock()
#         s.updatePage(self.currentpage)
#         s.addStatusBar()
#         d.drawScreen()

class statusbar():

    elements = {}

    def updateClock(self):
        self.elements[0] = time.asctime( time.localtime(time.time()) )
    
    def updatePage(self, newPage):
        self.elements[1] = newPage

    def addStatusBar(self):
        statusString = ""

        for i in range(len(self.elements)):
            statusString = statusString + str(self.elements[i]) + " "

        d.addText(statusString, 2, 165, False)

class files():

    bookPath = ""
    fontsPath = ""

    def loadCurrentPage(self, pathToBook):
        
        page = 0
        
        try:
            file = open(pathToBook + ".page", "r")
            page = int(file.read())
            file.close()

            return page

        except:
            return 0

    def saveCurrentPage(self, currentpage, pathToBook):
        print("Saveing" + pathToBook + ".page " + str(currentpage))
        file = open(pathToBook+".page", "w")

        file.write(str(currentpage))

        file.close()

    def getStringOfBooks(self):
        stringOfBooks = ""
        for filepath in glob.glob(self.bookPath + "*.txt"):
            stringOfBooks = stringOfBooks + filepath + "\n"

        return stringOfBooks

    def getListOfBook(self):

        txtfiles = []
        for file in glob.glob(self.bookPath + "*.txt"):
            txtfiles.append(file)

        return txtfiles
    
    def getListOfFonts(self):

        fontfiles = []
        for file in glob.glob(self.fontsPath + "/*.ttf"):
            fontfiles.append(file)

        return fontfiles

    def __init__(self, newBookPath, newFontsPath):
        self.bookPath = newBookPath
        self.fontsPath = newFontsPath

class menu():

    mode = 0

    fileSelectOptions = {}
    currentDisplay = {}
    currentPage = 0

    def setModeToFileSelection(self):
        self.mode = 2
    
        self.fileSelectOptions = f.getListOfBook()

        self.currentDisplay[0] = "UP"
        
        self.currentDisplay[1] = self.fileSelectOptions[self.currentPage]

        self.currentDisplay[2] = "DOWN"

        self.displayOptions()

    def setModeToReading(self):
        self.mode = 1

    def fileSelectScreenUp(self):
        try:
            self.currentPage = self.currentPage + 1

            self.currentDisplay[1] = self.fileSelectOptions[self.currentPage]

            m.displayOptions()
        except:
            self.currentPage = self.currentPage - 1
            print("Can't go down")

    def fileSelectScreenDown(self):
        try:
            self.currentPage = self.currentPage - 1

            self.currentDisplay[1] = self.fileSelectOptions[self.currentPage]

            m.displayOptions()
        except:
            self.currentPage = self.currentPage + 1
            print("Can't go foward")

    def currentDisplayToString(self):

        newString = ""

        for i in range(len(self.currentDisplay)):
            newString = newString + str(i) + ":" + self.currentDisplay[i] + "\n"

        return newString

    def executeOption(self, number):
        if self.mode == 0:
            self.setModeToFileSelection()
        elif self.mode == 1:
            if number == 0:
                b.prevPage()
            elif number == 1:
                m.setModeToFileSelection()
            elif number == 2:
                b.nextPage()
            elif number == 3:
                f.saveCurrentPage(b.getCurrentPage(),b.getFilePath())
                d.clear()
                d.sleep()
                os.system("sudo shutdown -h now")
        elif self.mode == 2:
            if number == 0:
                self.fileSelectScreenUp()
            elif number == 1:
                b.startreading("Spice and wolf", self.currentDisplay[1])
                m.setModeToReading()
            elif number == 2:
                self.fileSelectScreenDown()
            elif number == 3:
                d.clear()
                d.sleep()
                os.system("sudo shutdown -h now")

    def displayOptions(self):
        if self.mode == 0:
            d.newScreen()
            d.addText("1) Read A book! 2) Settings!", 2, 0, False)
            d.drawScreen()
        elif self.mode == 2:
            d.newScreen()
            d.addText(self.currentDisplayToString(), 2,0, False)
            d.drawScreen()

# Why did I name the all the object letters? I ask myself this questiong a lot.
d = inkdisplay(epd2in7.EPD(), "fonts", "UbuntuMono-R.ttf") # TODO USER Defined Font
f = files("Books/", "Fonts/")
b = book()
r = reading()
s = statusbar()
m = menu()
m.displayOptions()

fmtstr = " Name: %(user_name)s : %(asctime)s: (%(filename)s): %(levelname)s: %(funcName)s Line: %(lineno)d - %(message)s"
datestr = "%m/%d/%Y %I:%M:%S %p "

logging.basicConfig(
    filename="output.log",
    level=logging.DEBUG,
    filemode="w",
    format=fmtstr,
    datefmt=datestr,
)

logging.info("Init Finished")

def mainloop():
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
                logging.info("Button 1 Pressed")
                m.executeOption(0)
                time.sleep(0.2)
            if key2state == False:
                logging.info("Button 2 Pressed")
                m.executeOption(1)
                time.sleep(0.2)
            if key3state == False:
                logging.info("Button 2 Pressed")
                m.executeOption(2)
                time.sleep(0.2)
            if key4state == False:
                logging.info("Button 2 Pressed")
                m.executeOption(3)
                time.sleep(0.2)
            
            time.sleep(0.5)
try:
    mainloop()
except:
    logging.critical("Whopps something happended here is some info")
    d.clear()
    d.sleep()
    os.system("sudo shutdown -h now") 