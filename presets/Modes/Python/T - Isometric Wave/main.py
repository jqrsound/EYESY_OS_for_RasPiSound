import os
import pygame
import glob
import random
from pygame.locals import *
 
images = []
patterns = []

    
def setup(screen, etc) :
    global w1, h1, images, patterns
    
    for filepath in sorted(glob.glob(etc.mode_root + '/Images/*.png')):
        filename = os.path.basename(filepath)
        print 'loading image file: ' + filename
        img = pygame.image.load(filepath)
        images.append(img)
        
    patterns = generate_pattern(80, screen, etc)
    
    
def generate_pattern(TILEWIDTH_HALF, screen, etc):
    lines = []
    for  x in range(0, int(600-200*etc.knob1), TILEWIDTH_HALF):
        for y in range(0, int(600-200*etc.knob1), TILEWIDTH_HALF):
            cart_x = x 
            cart_y = y  
            iso_x = (cart_x - cart_y) 
            iso_y = (cart_x + cart_y)/2
            centered_x = screen.get_rect().centerx + iso_x - 60
            centered_y = screen.get_rect().centery/8 + iso_y
            if random.random() > (1*etc.knob3):           
                lines.append([0, centered_x, centered_y])  
            else:
                lines.append([1, centered_x, centered_y])
    return lines

def draw(screen, etc):
    global images, patterns

    etc.color_picker_bg(etc.knob5) 
    
    TileSize=int(160-64*etc.knob1)#+96*etc.knob1
    TILEWIDTH = TileSize  #holds the tile width and height
    TILEWIDTH_HALF = TILEWIDTH /2
    if etc.audio_trig:
        patterns = generate_pattern(TILEWIDTH_HALF, screen, etc)
        for p, pattern in enumerate(patterns):
            p2, p1 = pattern[-2:], pattern[:-2]
            i=p1.pop()
            k = p2.pop()
            j = p2.pop()
            y = k + etc.audio_in[p % 100] * .01 * etc.knob2
            pic=images[i]
            screen.blit(pic, (j, y))
    
    else:
        for p, pattern in enumerate(patterns):
            p2, p1 = pattern[-2:], pattern[:-2]
            i=p1.pop()
            k = p2.pop()
            y = k + etc.audio_in[p % 100] * .01 * etc.knob2
            j = p2.pop()
            pic=images[i]
            screen.blit(pic, (j, y))
            
    #Trails
    veil = pygame.Surface((1280,720))  
    veil.set_alpha(int(etc.knob4 * 50))
    veil.fill((etc.bg_color[0],etc.bg_color[1],etc.bg_color[2])) 
    screen.blit(veil, (0,0))
   