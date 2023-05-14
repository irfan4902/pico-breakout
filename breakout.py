import time
from pimoroni import Button
from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY, PEN_P4

display = PicoGraphics(display=DISPLAY_PICO_DISPLAY, pen_type=PEN_P4, rotate=0)

display.set_backlight(0.5)
display.set_font("bitmap8")

WIDTH, HEIGHT = display.get_bounds()

BG = display.create_pen(40, 40, 40)
WHITE = display.create_pen(255, 255, 255)
RED = display.create_pen(255, 0, 0)
BLUE = display.create_pen(255, 0, 0)

btn_a = Button(12)
btn_b = Button(13)
btn_x = Button(14)
btn_y = Button(15)

cols = 6
rows = 6

class Paddle():
    def __init__(self):
        self.width = 60
        self.height = 5
        self.x = WIDTH/2 - (self.width / 2)
        self.y = HEIGHT-10
        self.speed = 25
        self.colour = WHITE

class Ball():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 5
        self.x_velocity = 0
        self.y_velocity = 0
        self.colour = RED  

class Block():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 60
        self.height = 30
        self.points = 1
        self.colour = BLUE

def renderPaddle(obj):
    display.set_pen(obj.colour)
    display.rectangle(int(obj.x), int(obj.y), obj.width, obj.height)

def renderBall(obj):
    display.set_pen(obj.colour)
    display.circle(int(obj.x), int(obj.y), obj.radius)
    obj.x += obj.x_velocity
    obj.y += obj.y_velocity

lol = Paddle()
ball = Ball(lol.x + (lol.width / 2), lol.y - 15)

blocks = []
blocks.append(Block(5,0))
blocks.append(Block(70,0))
blocks.append(Block(135,0))

for block in blocks:
    display.rectangle(block.x, block.y, block.width, block.height)

while True:
    renderPaddle(lol)
    display.update()
    renderBall(ball)
    if btn_a.read():
        ball.y_velocity = -2
        ball.x_velocity = 0.5
        break

# Game Loop
while True:
    display.set_pen(BG)
    display.clear()

    if btn_y.read():
        lol.x += lol.speed
    
    if btn_b.read():
        lol.x -= lol.speed
    
    xmax = WIDTH - ball.radius
    xmin = ball.radius
    ymax = HEIGHT - ball.radius
    ymin = ball.radius

    if ball.x < xmin or ball.x > xmax:
        ball.x_velocity *= -1

    if ball.y < ymin:
        ball.y_velocity *= -1
    
    if (ball.y >= lol.y-lol.height) and (lol.x <= ball.x <= lol.x + lol.width):
        ball.y_velocity *= -1
    
    renderPaddle(lol)
    renderBall(ball)
    display.update()
    time.sleep(0.01)
    
    
    
    
    
    
    
    
    