import pygame
import pygame.gfxdraw
import time
import math
from pygame.locals import *

# original code adapted from zach lieberman's talk
# https://www.youtube.com/watch?v=bmztlO9_Wvo
#http://www.mathrecreation.com/2016/10/some-familiar-spirals-in-desmos.html

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
    k=int(((h1 ))+((h1 )) *(math.sin(time.time()*(.1+etc.knob2*2))))
    for i in range(0, (h1 +20), 1):
        i=i*2
        color = (int(127 + 120 * math.sin(i * .01 + time.time())),
                 int(127 + 120 * math.sin(i * (.01 + etc.knob5*.01) + time.time())),
                 int(127 + 120 * math.sin(i * (.01 + etc.knob5*.02)+ time.time())))
                
        r1= (abs(etc.audio_in[i%100]))
        radius2 = int((.4+etc.knob2/3)*(r1/400))

        xpos3= (w1 / 2)
        ypos2 = (h1/2)
        
        xpos4=int(xpos3+(20*etc.knob2+1)*math.sqrt(i)*math.cos(i*((1+math.sqrt(5)*math.pi/(math.pi+12*etc.knob1)))))
        
        ypos3=int(ypos2+(20*etc.knob2+1)*math.sqrt(i)*math.sin(i*((1+math.sqrt(5)*math.pi/(math.pi+12*etc.knob1)))))
        
        radius4=int(radius2+ (math.cos(i * (etc.knob2 * .2) + time.time())))
        if (k-((h1*2)+30)*etc.knob4-5) <= i <= (k+((h1*2)+30)*etc.knob4+5) :
            pygame.gfxdraw.filled_circle(screen, xpos4, ypos3, radius4, color)
    #Trails
    veil = pygame.Surface((1280,720))  
    veil.set_alpha(int(etc.knob3 * 50))
    veil.fill((etc.bg_color[0],etc.bg_color[1],etc.bg_color[2])) 
    screen.blit(veil, (0,0))