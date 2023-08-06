# test program for Fl_JPEG_Image from memory buffer
# cat image from https://commons.wikimedia.org/wiki/File:Arthur,_the_cat.jpg

from fltk import *
from PIL import Image
import io

def img_resize(fname,width):
    '''resizes any image type using high quality PIL library'''
    img = Image.open(fname) #opens all image formats supported by PIL
    w,h = img.size
    height = int(width*h/w)  #correct aspect ratio
    img = img.resize((width, height), Image.BICUBIC) #high quality resizing
    mem = io.BytesIO()  #byte stream memory object
    img.save(mem, format="JPEG") #converts image type to JPEG byte stream
    return Fl_JPEG_Image(None, mem.getbuffer())

pic = img_resize('cat.jpg', 300) #resizes to 300 pixels width
win = Fl_Window(pic.w(), pic.h(), 'PIL resizing')
win.begin()
box = Fl_Box(0, 0, pic.w(), pic.h())
win.end()

box.image(pic)

win.show()
Fl.run()


