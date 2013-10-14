import pygame
import sys

rows=4; cols=10
sw=1024; sh=768 # screen size
b=2 # border width

pygame.init()
pygame.display.init()
scr = pygame.display.set_mode((sw,sh), pygame.FULLSCREEN)
sw, sh = scr.get_size()
pygame.event.set_allowed(pygame.MOUSEBUTTONDOWN)
pygame.event.set_allowed(pygame.KEYDOWN)
font = pygame.font.SysFont(pygame.font.get_default_font(), 20)

img = pygame.image.load(sys.argv[1]).convert()
w,h = img.get_size()
print "%dx%d -> %dx%d"%(w,h,sw,sh)
if float(sw)/w > float(sh)/h:
    h = sh
    w = w*sh/h
    x0 = (sw-w)/2
    y0 = 0
else:
    w = sw
    h = h*sw/w
    y0 = (sh-h)/2
    x0 = 0
print " => %dx%d"%(w,h)
img = pygame.transform.scale(img, (w,h))

vis = [[False]*rows for i in range(cols)] 

while(1):
    # redraw
    scr.fill((0,0,0))
    for x in range(cols):
        for y in range(rows):
            ri = pygame.Rect(x*w/cols+b, y*h/rows+b, w/cols-b, h/rows-b)
            rs = pygame.Rect(x*w/cols+b+x0, y*h/rows+b+y0, w/cols-b, h/rows-b)
            if vis[x][y]:
                col=(200,200,200)
                scr.blit(img, ri, rs)
            else:
                col=(100,100,100)
                pygame.draw.rect(scr, col, rs)
                t = font.render("%d, %d"%(x+1,y+1), 1, (255,255,255))
                scr.blit(t, rs)
    pygame.display.flip()
    # event
    e=pygame.event.wait()
    if e.type==pygame.MOUSEBUTTONDOWN:
        x,y = e.pos
        x=x*cols/w
        y=y*rows/h
        print "Click: %d,%d: %s(pretoggle)"%(x,y,vis[x][y])
        vis[x][y]=not vis[x][y]
    if e.type==pygame.KEYDOWN:
        exit()

