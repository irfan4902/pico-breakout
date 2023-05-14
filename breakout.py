import time
from pimoroni import Button
from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY, PEN_P4

display = PicoGraphics(display=DISPLAY_PICO_DISPLAY, pen_type=PEN_P4, rotate=0)

display.set_backlight(0.5)
display.set_font("bitmap8")

WHITE = display.create_pen(255, 255, 255)
BLACK = display.create_pen(0, 0, 0)

btn_a = Button(12)
btn_b = Button(13)
btn_x = Button(14)
btn_y = Button(15)

WIDTH, HEIGHT = display.get_bounds()

cols = 6
rows = 6

BG = display.create_pen(40, 40, 40)

class Paddle():
    def __init__(self):
        self.x = int(WIDTH/2)
        self.y = HEIGHT-10
        self.width = 50
        self.height = 5
        self.speed = 10
        self.colour = WHITE

lol = Paddle()

display.set_pen(lol.colour)
display.rectangle(lol.x, lol.y, lol.width, lol.height)
display.update()

while True:
    display.set_pen(BG)
    display.clear()

    if btn_y.read():
        lol.x += lol.speed
    
    if btn_b.read():
        lol.x -= lol.speed
    
    display.set_pen(lol.colour)
    display.rectangle(lol.x, lol.y, lol.width, lol.height)
    display.update()
    time.sleep(0.01)
    
    
    
    
    
    
    
    
    