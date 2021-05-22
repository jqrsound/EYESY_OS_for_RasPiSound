# JJD MOD of Dancing Image to scroll through available images
# Combines some features of the original Basic Image sketch with the Dancing Image sketch
# Trigger now scrolls through image (manual, audio or via MIDI)

import os
import pygame
import time
import random
import glob
import math

last_point = [0, 360]
i = 0
images = []
image_index = 0     #JJD SET Start image
waiting = 0         #JJD Set waiting
lx = 0
ly = 0

def setup(screen, etc):
    global images, xr, yr, last_point
    xr = etc.xres
    yr = etc.yres
    last_point = [0, yr/2]
    for filepath in sorted(glob.glob(etc.mode_root + '/Images/*.png')):
        filename = os.path.basename(filepath)
        print 'loading image file: ' + filename
        img = pygame.image.load(filepath).convert_alpha()
        images.append(img)

def draw(screen, etc):
    #JJD Added image_index and waiting
    global last_point, images, image_index, i, lx, ly, xr, yr, waiting
    etc.color_picker_bg(etc.knob5)
    x300 = int((300*xr)/1280)
    x30 = int((30*xr)/1280)
    xoffset = 0
    y1 = int(etc.knob2 * yr) + ((etc.audio_in[i]*0.00003058) *(yr/2))
    x = i * (xr/100)
    color = etc.color_picker(etc.knob4)
    
# START JJD MOD For image selection - copied from Basic Image sketch
    above = False
    
    if waiting == 0 :
        for i in range(0, 100) :
            if abs(etc.audio_in[i]) > 1000 :
                above = True
                waiting = 4
    else :
        waiting -= 1
    
    if etc.audio_trig or etc.midi_note_new :
        image_index += 1
        if image_index == len(images) : image_index = 0
        img = images[image_index]
# END JJD MOD

    R = (etc.knob2*x300)-(x300/2)
    R = R + ((etc.audio_in[i]*0.00003058)*(yr/2))
    x = R * math.cos((i /  100.) * 6.28) + (xr/2)
    y = R * math.sin((i /  100.) * 6.28) + (yr/2)
    
    max_circle = x300
    image_size = 1
    circle_size = 0
    line_width = 0
    if etc.knob3 <=.5 :
        circle_size = int(etc.knob3 * max_circle)
        line_width = 0
    if etc.knob3 >.501 :
        circle_size = abs(max_circle-int(etc.knob3 * max_circle)) 
        line_width =  abs(x30-int(etc.knob3 * x30))
    
    pygame.draw.circle(screen,color,(int(x),int(y)), circle_size, line_width)
    image = images[image_index]  #JJD Change image index based on code above (this replaces original 0)
    image = pygame.transform.scale(image, (int(image.get_width() * etc.knob1), int(image.get_height() * etc.knob1)) )
    screen.blit(image, (x, y))
    
    i = (i + 1) % 100

# Thanks for downloading!
# www.jeremydeprisco.net