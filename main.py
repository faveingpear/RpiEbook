import sys
import os

from lib.waveshare_epd import epd2in7
from PIL import Image,ImageDraw,ImageFont
import time

epd = epd2in7.EPD()

epd.init()
epd.Clear(0xFF)

fontsdir = os.path.join('fonts')

font24 = ImageFont.truetype(os.path.join(fontsdir, 'Ubuntu-R.ttf'), 24)

Himage = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame
draw = ImageDraw.Draw(Himage)

draw.text((10, 0), 'hello world', font = font24, fill = 0)

epd.display(epd.getbuffer(Himage))

epd.Clear(0xFF)