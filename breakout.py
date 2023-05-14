import time
from pimoroni import Button
from pimoroni import RGBLED
from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY, PEN_P4

display = PicoGraphics(display=DISPLAY_PICO_DISPLAY, pen_type=PEN_P4, rotate=0)

display.set_backlight(0.5)
display.set_font("bitmap8")

WIDTH, HEIGHT = display.get_bounds()

BG = display.create_pen(40, 40, 40)
WHITE = display.create_pen(255, 255, 255)
RED = display.create_pen(255, 0, 0)
BLUE = display.create_pen(0, 0, 255)
GREEN = display.create_pen(0, 255, 0)

btn_a = Button(12)
btn_b = Button(13)
btn_x = Button(14)
btn_y = Button(15)

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
        self.speed = 5

class Block():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 30
        self.height = 15
        self.points = 1
        self.colour = BLUE
        self.destroyed = False

victory = False

# Render functions
def renderBlocks():
    for block in blocks:
        if (not block.destroyed):
            display.set_pen(block.colour)
            display.rectangle(block.x, block.y, block.width, block.height)
        else:
            display.set_pen(BG)
            display.rectangle(block.x, block.y, block.width, block.height)

def renderPaddle(obj):
    display.set_pen(obj.colour)
    display.rectangle(int(obj.x), int(obj.y), obj.width, obj.height)

def renderBall(obj):
    display.set_pen(obj.colour)
    display.circle(int(obj.x), int(obj.y), obj.radius)
    obj.x += obj.x_velocity
    obj.y += obj.y_velocity

def movePaddle():
    if btn_y.read():
        paddle.x += paddle.speed
    
    if btn_b.read():
        paddle.x -= paddle.speed

# Program Loop
while True:
    
    # Main Menu Loop
    while True:
        if not victory:
            display.set_pen(WHITE)
            display.text("Untitled Breakout Game", 5, 5, scale=2)
            display.text("Buttons B and Y to move", 5, 25, scale=2)
            display.text("Button A to start", 5, 45, scale=2)
            display.text("Button X to quit", 5, 65, scale=2)
            display.update()
            if btn_a.read():
                break
        else:
            display.set_pen(GREEN)
            display.text("Congratulations!", 5, 5, scale=2)
            display.update()
            if btn_a.read():
                break

    # Create ball and paddle
    paddle = Paddle()
    ball = Ball(paddle.x + (paddle.width / 2), paddle.y - 15)

    # Create all the blocks
    blocks = []
    blocks.append(Block(15,5))
    blocks.append(Block(50,5))
    blocks.append(Block(85,5))
    blocks.append(Block(120,5))
    blocks.append(Block(155,5))
    blocks.append(Block(190,5))

    blocks.append(Block(15,25))
    blocks.append(Block(50,25))
    blocks.append(Block(85,25))
    blocks.append(Block(120,25))
    blocks.append(Block(155,25))
    blocks.append(Block(190,25))

    blocks.append(Block(15,45))
    blocks.append(Block(50,45))
    blocks.append(Block(85,45))
    blocks.append(Block(120,45))
    blocks.append(Block(155,45))
    blocks.append(Block(190,45))

    # Game loop before the game starts
    while True:
        display.set_pen(BG)
        display.clear()
        
        movePaddle()
        
        ball.x = paddle.x + (paddle.width / 2)
        
        renderPaddle(paddle)
        renderBall(ball)
        renderBlocks()
        
        if btn_a.read():
            ball.y_velocity = -ball.speed
            break
        
        display.update()
        time.sleep(0.01)

    # Game loop when the game starts
    while True:
        display.set_pen(BG)
        display.clear()

        movePaddle()
        
        xmax = WIDTH - ball.radius
        xmin = ball.radius
        ymin = ball.radius

        if ball.x < xmin or ball.x > xmax:
            ball.x_velocity *= -1

        if ball.y < ymin:
            ball.y_velocity *= -1
        
        # Check if the ball is colliding with the paddle
        if (ball.y >= paddle.y-paddle.height) and (paddle.x <= ball.x <= paddle.x + paddle.width):
            #Make the ball go up
            ball.y_velocity *= -1
            
            # If the ball hits the left side of the paddle, make the ball go left
            if (paddle.x <= ball.x <= paddle.x + paddle.width/2):
                ball.x_velocity = -2
                
            # If the ball hits the right side of the paddle, make the ball go right
            if ( (paddle.x + paddle.width/2) <= ball.x <= (paddle.x + paddle.width) ):
                ball.x_velocity = 2
        
        # Check if the ball is colliding with a block
        for block in blocks:
            if (block.x <= ball.x <= block.x+block.width) and (block.y <= ball.y <= block.y+block.height) and (not block.destroyed):
                block.destroyed = True
                ball.y_velocity *= -1
                ball.x_velocity *= -1
                blocks.remove(block)
                
        renderBlocks()
        renderPaddle(paddle)
        renderBall(ball)
        
        # Exit to Main Menu
        if btn_x.read():
            display.set_pen(BG)
            display.clear()
            break
        
        if not blocks:
            display.set_pen(BG)
            display.clear()
            victory = True
            break
        
        display.update()
        time.sleep(0.01)
        