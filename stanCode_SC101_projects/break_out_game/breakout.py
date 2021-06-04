"""
stanCode Breakout Project
Adapted from Eric Roberts's Breakout by
Sonja Johnson-Yu, Kylie Jue, Nick Bowman,
and Jerry Liao.

YOUR DESCRIPTION HERE
"""

from campy.gui.events.timer import pause
from breakoutgraphics import BreakoutGraphics

FRAME_RATE = 1000 / 120 # 120 frames per second
NUM_LIVES = 3			# Number of attempts


def main():
    """
    A breakout game, user can click mouse to start,and move the mouse to control the paddle,
    using the paddle to bounce the ball for hitting bricks.
    """
    graphics = BreakoutGraphics()
    life = NUM_LIVES

    # Add animation loop here!
    while life > 0:
        dx = graphics.get_dx()
        dy = graphics.get_dy()
        pause(FRAME_RATE)
        graphics.ball.move(dx, dy)
        graphics.window_check()
        graphics.check_remove()
        life -= graphics.dead()
        if graphics.ball.y >= graphics.window.height:
            graphics.restart()


if __name__ == '__main__':
    main()
