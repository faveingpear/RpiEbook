import sys

sys.path.insert(1, 'e-Paper/RaspberryPi&JetsonNano/python')

from e-Paper.RaspberryPi&JetsonNano.python.waveshare_epd import epd2in7
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