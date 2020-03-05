import sys

from lib.waveshare_epd import epd2in7
import time

try:
    epd = epd2in7.EPD()

    epd.init()
    epd.Clear(0xFF)

    draw.text((10, 0), 'hello world', font = font24, fill = 0)

    epd.display(epd.getbuffer(Himage))

    epd.Clear(0xFF)

except:
    print("error")