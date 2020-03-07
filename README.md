# RpiEbook

A python program that utilizes the waveshare E-ink displays for reading books.

### What can it do?

So far RpiEbook can allow your to read from multiple text files and automatically saves your place.

### TODO

Add support for Ebook formats such as EPUB, or PDF.
Add a settings menu to change options such as font, fontsize, what the status bar displays, etc
Improve menu navagation speed
Make a menu that used highlighted sections so I can render more than one option on the screen at once
Work on settings menu to change fontsizes, font, words per page, etc..
Work on making the program more stable for example making sure out of bound errors can happen
Figure out how the licences work with the waveshare_epd driver
Use public domain fonts because Im not sure if I am really allowed to use Ubuntu Fonts 
LOGGING
General Optimization
Maybe research if exception based GPIO is a thing so I don't need a mainloop to check for the GPIO every 0.5s 
Design!!
IMPROVE Menu class so it doesn't need specific code for every menu but can be reused.