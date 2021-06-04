"""
stanCode Breakout Project
Adapted from Eric Roberts's Breakout by
Sonja Johnson-Yu, Kylie Jue, Nick Bowman, 
and Jerry Liao

YOUR DESCRIPTION HERE
"""
from campy.graphics.gwindow import GWindow
from campy.graphics.gobjects import GOval, GRect, GLabel
from campy.gui.events.mouse import onmouseclicked, onmousemoved
import random

BRICK_SPACING = 5      # Space between bricks (in pixels). This space is used for horizontal and vertical spacing.
BRICK_WIDTH = 40       # Height of a brick (in pixels).
BRICK_HEIGHT = 15      # Height of a brick (in pixels).
BRICK_ROWS = 10        # Number of rows of bricks.
BRICK_COLS = 10        # Number of columns of bricks.
BRICK_OFFSET = 50      # Vertical offset of the topmost brick from the window top (in pixels).
BALL_RADIUS = 10       # Radius of the ball (in pixels).
PADDLE_WIDTH = 75      # Width of the paddle (in pixels).
PADDLE_HEIGHT = 15     # Height of the paddle (in pixels).
PADDLE_OFFSET = 50     # Vertical offset of the paddle from the window bottom (in pixels).

INITIAL_Y_SPEED = 7    # Initial vertical speed for the ball.
MAX_X_SPEED = 5        # Maximum initial horizontal speed for the ball.


class BreakoutGraphics:

    def __init__(self, ball_radius=BALL_RADIUS, paddle_width=PADDLE_WIDTH,
                 paddle_height=PADDLE_HEIGHT, paddle_offset=PADDLE_OFFSET,
                 brick_rows=BRICK_ROWS, brick_cols=BRICK_COLS,
                 brick_width=BRICK_WIDTH, brick_height=BRICK_HEIGHT,
                 brick_offset=BRICK_OFFSET, brick_spacing=BRICK_SPACING,
                 title='Breakout'):

        self.__ball_radius = ball_radius
        self.__paddle_width = paddle_width
        self.__paddle_height = paddle_height
        self.__paddle_offset = paddle_offset

        # Create a graphical window, with some extra space
        self.window_width = brick_cols * (brick_width + brick_spacing) - brick_spacing
        self.window_height = brick_offset + 3 * (brick_rows * (brick_height + brick_spacing) - brick_spacing)
        self.window = GWindow(width=self.window_width, height=self.window_height, title=title)

        # Create a paddle
        self.__paddle = GRect(paddle_width, paddle_height, x=(self.window_width-paddle_width)/2, y=(self.window_height-self.__paddle_offset))
        self.__paddle.filled = True
        self.window.add(self.__paddle)

        # Center a filled ball in the graphical window
        self.ball = GOval(ball_radius*2, ball_radius*2, x=(self.window_width/2)-ball_radius, y=(self.window_height/2)-ball_radius)
        self.ball.filled = True
        self.window.add(self.ball)

        # Default initial velocity for the ball
        self.__dy = 0
        self.__dx = 0

        # Initialize our mouse listeners
        onmousemoved(self.paddle_move)
        self.__click = 1                    # 'click' as a switch,1 means prepare to start,-1 means game playing.
        onmouseclicked(self.ball_start)

        # Draw bricks
        for i in range(brick_rows):
            for j in range(brick_cols):
                self.__brick = GRect(brick_width, brick_height, x=0+j*(brick_width + brick_spacing), y=0+i*(brick_height + brick_spacing))
                self.__brick.filled = True
                if i % 10 < 2:
                    self.__brick.fill_color = 'red'
                elif i % 10 < 4:
                    self.__brick.fill_color = 'orange'
                elif i % 10 < 6:
                    self.__brick.fill_color = 'yellow'
                elif i % 10 < 8:
                    self.__brick.fill_color = 'green'
                elif i % 10 < 10:
                    self.__brick.fill_color = 'blue'
                self.window.add(self.__brick)

    # mouse move
    def paddle_move(self, m):
        x = m.x - self.__paddle_width/2
        if (self.window_width-self.__paddle_width/2) > m.x > self.__paddle_width/2:
            self.window.add(self.__paddle, x=x, y=(self.window_height-self.__paddle_offset))
        elif m.x < self.__paddle_width/2:
            self.window.add(self.__paddle, x=0, y=(self.window_height - self.__paddle_offset))
        else:
            self.window.add(self.__paddle, x=(self.window_width-self.__paddle_width), y=(self.window_height - self.__paddle_offset))

    # mouse clicked,give velocity for the ball
    def ball_start(self, mouse):
        if self.__click == 1:
            self.__click *= -1              # game start,turn 'click' to -1.
            self.__dy = INITIAL_Y_SPEED
            self.__dx = random.randint(1, MAX_X_SPEED)
            if random.random() > 0.5:
                self.__dx = -self.__dx

    def get_dx(self):
        return self.__dx

    def get_dy(self):
        return self.__dy

    # check if the ball hits the window,let the ball bound.
    def window_check(self):
        if self.ball.x <= 0 or self.ball.x + self.ball.width >= self.window.width:
            self.__dx = -self.__dx
        if self.ball.y <= 0:
            self.__dy = -self.__dy

    # check if the ball touch the brick,remove the brick.
    def check_remove(self):
        # ball1 upper left point
        ball1x = self.ball.x
        ball1y = self.ball.y

        # ball2 upper right point
        ball2x = self.ball.x + self.__ball_radius * 2
        ball2y = self.ball.y

        # ball3 lower right point
        ball3x = self.ball.x + self.__ball_radius * 2
        ball3y = self.ball.y + self.__ball_radius * 2

        # ball4 lower left point
        ball4x = self.ball.x
        ball4y = self.ball.y + self.__ball_radius * 2

        if self.window.get_object_at(ball1x, ball1y) is not None:
            if ball1y > self.window_height-self.__paddle_offset and self.__dy < 0:         # 防止球黏在板上
                pass
            else:
                self.__dy = -self.__dy
                box = self.window.get_object_at(ball1x, ball1y)
                if box.y < (self.window_height-self.__paddle_offset-self.__paddle_height):
                    self.window.remove(box)
        elif self.window.get_object_at(ball2x, ball2y) is not None:
            if ball2y > self.window_height-self.__paddle_offset and self.__dy < 0:
                pass
            else:
                self.__dy = -self.__dy
                box = self.window.get_object_at(ball2x, ball2y)
                if box.y < (self.window_height-self.__paddle_offset-self.__paddle_height):
                    self.window.remove(box)
        elif self.window.get_object_at(ball3x, ball3y) is not None:
            if ball3y > self.window_height-self.__paddle_offset and self.__dy < 0:
                pass
            else:
                self.__dy = -self.__dy
                box = self.window.get_object_at(ball3x, ball3y)
                if box.y < (self.window_height-self.__paddle_offset-self.__paddle_height):
                    self.window.remove(box)
        elif self.window.get_object_at(ball4x, ball4y) is not None:
            if ball4y > self.window_height-self.__paddle_offset and self.__dy < 0:
                pass
            else:
                self.__dy = -self.__dy
                box = self.window.get_object_at(ball4x, ball4y)
                if box.y < (self.window_height-self.__paddle_offset-self.__paddle_height):
                    self.window.remove(box)

    # if the ball drop out of the window
    def dead(self):
        if self.ball.y > self.window_height:
            self.__click *= -1                  # game fail ,turn 'click' to 1.
            return 1
        else:
            return 0

    # reset the ball
    def restart(self):
        self.ball.x = (self.window.width - self.ball.width) / 2
        self.ball.y = (self.window.height - self.ball.height) / 2
        self.__dx = 0
        self.__dy = 0