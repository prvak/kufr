#!/usr/bin/python
import argparse
import pygame
import sys

verbose = False
def log(message):
    if (verbose):
        print(message)

backgroundColor = (0, 0, 0)
fontColor = (255, 255, 255)
foregroundColor = (50, 60, 70)

def fitImageToScreen(img, screen):
    """Returns image rescaled so that it fits the screen."""
    w, h = img.get_size()
    sw, sh = screen.get_size()
    log("%d x %d -> %d x %d" % (w, h, sw, sh))
    if float(sw)/sh > float(w)/h:
        w = w*sh/h
        h = sh
    else:
        h = h*sw/w
        w = sw
    log(" => %d x %d" % (w, h))
    img = pygame.transform.scale(img, (w, h))
    return img

def computeOffset(img, screen):
    """How far from the top left corner the image should be."""
    w, h = img.get_size()
    sw, sh = screen.get_size()
    if float(sw)/w > float(sh)/h:
        x0 = (sw-w)/2
        y0 = 0
    else:
        y0 = (sh-h)/2
        x0 = 0
    return (x0, y0)

def drawGrid(img, screen, font, cols, rows, visible):
    # redraw
    w, h = img.get_size()
    x0, y0 = computeOffset(img, screen)
    cw, ch = w/cols, h/rows
    b = 1
    screen.fill(backgroundColor)
    for x in range(cols):
        for y in range(rows):
            ri = pygame.Rect(x*(cw+b), y*(ch+b), cw-b, ch-b)
            rs = pygame.Rect(x*(cw+b)+x0, y*(ch+b)+y0, cw-b, ch-b)
            if visible[x][y]:
                screen.blit(img, rs, ri)
            else:
                pygame.draw.rect(screen, foregroundColor, rs)
                text = font.render("%d, %d"% (x+1,y+1), 1, fontColor)
                rt = pygame.Rect(x*(cw+b)+x0+5, y*(ch+b)+y0+5, cw-b, ch-b)
                screen.blit(text, rt)

    pygame.display.flip()

def drawImage(img, screen):
    # redraw
    w, h = img.get_size()
    x0, y0 = computeOffset(img, screen)
    screen.fill((0, 0, 0))
    ri = pygame.Rect(0, 0, w, h)
    rs = pygame.Rect(x0, y0, w, h)
    screen.blit(img, rs, ri)
    pygame.display.flip()

def run(img, screen, font, cols, rows):
    visible = [[False]*rows for i in range(cols)]
    wholeVisible = False
    drawGrid(img, screen, font, cols, rows, visible)
    while(True):
        e = pygame.event.wait()
        if e.type == pygame.MOUSEBUTTONDOWN and not wholeVisible:
            x, y = e.pos
            w, h = img.get_size()
            x0, y0 = computeOffset(img, screen)
            if x >= x0 and x < w + x0 and y > y0 and y < h + y0:
                col = (x-x0)*cols/w
                row = (y-y0)*rows/h
                visible[col][row] = not visible[col][row]
                drawGrid(img, screen, font, cols, rows, visible)
        if e.type==pygame.KEYDOWN:
            if e.key == pygame.K_RETURN:
                if wholeVisible:
                    exit()
                else:
                    drawImage(img, screen)
                    wholeVisible = True
            if e.key == pygame.K_ESCAPE:
                exit()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
            description="""Hides given image behind a grid of black squares and
            reveals one square per click.""")
    parser.add_argument("-r", "--rows", type = int, default = 8,
            help = "how many rows should the grid have")
    parser.add_argument("-c", "--cols", type = int, default = 6,
            help="how many columns should the grid have")
    parser.add_argument("-x", "--width", type = int, default = 800,
            help = "width of the window")
    parser.add_argument("-y", "--height", type = int, default = 600,
            help = "height of the window")
    parser.add_argument("-f", "--fullscreen", action = "store_true",
            help = "if true, the window will occupy the entire screen")
    parser.add_argument("-v", "--verbose", action = "store_true",
            help = "if not specified, the program will not output anything")
    parser.add_argument("image", type = str, 
            help = "path to the image")
    args = parser.parse_args()
    
    # Set verbosity level.
    verbose = args.verbose

    # Initialize the pygame.
    log("Initializing display.")
    pygame.init()
    #pygame.display.init()
    pygame.event.set_allowed(pygame.MOUSEBUTTONDOWN)
    pygame.event.set_allowed(pygame.KEYDOWN)
    if args.fullscreen:
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode((args.width, args.height))

    # Load the image.
    img = pygame.image.load(args.image).convert()
    img = fitImageToScreen(img, screen)

    # Load font.
    sw, sh = screen.get_size()
    fontSize = sh/25
    font = pygame.font.SysFont(pygame.font.get_default_font(), fontSize)

    run(img, screen, font, args.cols, args.rows)
    sw, sh = screen.get_size()
    b=2 # border width


