import sys

from lib.waveshare_epd import epd2in7
from PIL import Image,ImageDraw,ImageFont
import time

epd = epd2in7.EPD()

epd.init()
epd.Clear(0xFF)

Himage = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame
draw = ImageDraw.Draw(Himage)

draw.text((10, 0), 'hello world', fill = 0)

epd.display(epd.getbuffer(Himage))

epd.Clear(0xFF)