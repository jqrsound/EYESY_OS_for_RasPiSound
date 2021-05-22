import pygame
import pygame.gfxdraw
import random
import time
import math
from pygame.locals import *

# original code adapted from zach lieberman's talk
# https://www.youtube.com/watch?v=bmztlO9_Wvo
    
white=(255,255,255)
w1 = 0
h1 = 0

def setup(screen, etc) :
    global w1,h1
    w1 = screen.get_width()
    h1 = screen.get_height()
    pass

def draw(screen, etc):
    global w1,h1
    etc.color_picker_bg(etc.knob5)
    #for i in range(320):
    k=int(((h1 / 2)-10)+((h1 / 2)-10) *(math.sin(time.time()*(.4+1-etc.knob1))))
    j=int(((h1 / 2)-10)+((h1 / 2)-10) *(math.cos(time.time()*(.4+1-etc.knob1))))
    l=int((h1 )-25)-k
    for i in range(0, (h1 / 2) - 10, 1):#+int(etc.knob1*15)):
        i=i*2
        color = (int(127 + 120 * math.sin(i * .01 + time.time())),
                 int(127 + 120 * math.sin(i * (.01 + etc.knob5*.01) + time.time())),
                 int(127 + 120 * math.sin(i * (.01 + etc.knob5*.02)+ time.time())))
                
        r1= (abs(etc.audio_in[i/50]))#300
        radius_2 = int( 50  - 20 * math.sin(i * (etc.knob2 * .2)+.0001 + time.time()))
        radius2 = int(etc.knob3 * radius_2+int(r1/400))
        xoffset1 = i
        xpos1 = int(((w1 / 2)-i) * math.sin(i * .01 + (time.time()*0.3)) + (w1 / 2-i) + xoffset1)
        xpos2 = xpos1 + (h1 / 2) 
        xpos3= xpos1 - (h1 / 2)
        
        rect2 = Rect(xpos1, i, radius2*1.5, radius2*1.5)
        radius3=int(radius2+30*etc.knob1+etc.knob1*30 *(math.sin(i * (etc.knob2 * .2) + time.time())))
        radius4=int(radius2+30*etc.knob1+etc.knob1*30 *(math.cos(i * (etc.knob2 * .2) + time.time())))
        if (j-int(((h1)-10)*etc.knob4)-1) <= i <= (j+int(((h1)-10)*etc.knob4)+1) :
            pygame.gfxdraw.rectangle(screen, rect2, color)
        if (l-((h1)-10)*etc.knob4-1) <= i <= (l+((h1)-10)*etc.knob4+1) :
            pygame.gfxdraw.ellipse(screen, xpos2, i, radius3, radius4, color)
        if (k-((h1)-10)*etc.knob4-1) <= i <= (k+((h1)-10)*etc.knob4+1) :
            pygame.gfxdraw.ellipse(screen, xpos3, i, radius4, radius3, color)
