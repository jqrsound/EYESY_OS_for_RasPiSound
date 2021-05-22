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
    for i in range((h1 / 2) - 10):
        i=i*2
        color = (int(127 + 120 * math.sin(i * .01 + time.time())),
                 int(127 + 120 * math.sin(i * (.01 + etc.knob4*.01) + time.time())),
                 int(127 + 120 * math.sin(i * (.01 + etc.knob4*.02)+ time.time())))
                
        r1= (abs(etc.audio_in[i/50]/900))
        radius_1 = int(100 + r1+40 * math.sin(i * (etc.knob1 * .05)+.0001 + time.time()))
        radius1 = int(etc.knob3 * radius_1)
        radius_2 = int( 70 + r1 - 20 * math.sin(i * (etc.knob2 * .2)+.0001 + time.time()))
        radius2 = int(etc.knob3 * radius_2)
        xoffset1 = i
        xpos1 = int(((w1 / 2)-i) * math.sin(i * .01 + (time.time()*0.3)) + (w1 / 2-i) + xoffset1)+ int(r1*1.5)
        xpos2 = int(((w1 / 2)-i) * math.sin(i * .01 + (time.time()*0.3)) + (w1 / 2-i) + xoffset1+(h1 / 2))+ int(r1*1.5)#int(w1 // 2 + 100 * math.sin(i * .02 + time.time())*1.3)+(h1 / 2)+ int(r1*1.5)#-int(etc.knob1*(720-i)) 
        xpos3 = int(((w1 / 2)-i) * math.sin(i * .01 + (time.time()*0.3)) + (w1 / 2-i) + xoffset1-+(h1 / 2))+ int(r1*1.5)#int(w1 // 2 + 100 * math.sin(i * .02 + time.time())*1.2)-(h1 / 2)+ int(r1*1.5)#-int(etc.knob1*(720-i))
        rect2 = Rect(xpos2, i, radius2*1.5, radius2*1.5)
        radius3=int(radius2+10+10 *(math.sin(i * (etc.knob2 * .2) + time.time())))
        radius4=int(radius2+10+10 *(math.cos(i * (etc.knob1 * .2) + time.time())))
        pygame.gfxdraw.circle(screen, xpos1, i, radius1, color)
        pygame.gfxdraw.rectangle(screen, rect2, color)
        pygame.gfxdraw.ellipse(screen, xpos3, i, radius3, radius4, color)
        #pygame.gfxdraw.circle(screen, xpos3, i, radius2, color)
        #pygame.gfxdraw.filled_circle(screen, xpos1, i, radius1, color)
        #pygame.gfxdraw.filled_circle(screen, xpos2, i, radius2, color)
        #pygame.gfxdraw.filled_circle(screen, xpos3, i, radius2, color)
    #pygame.gfxdraw.circle(screen, xpos1, i, radius1, white )
    #pygame.gfxdraw.circle(screen, xpos2, i, radius2, white )
    #pygame.gfxdraw.circle(screen, xpos3, i, radius2, white )
