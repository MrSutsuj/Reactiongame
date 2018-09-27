import random
import time
from enum import Enum

LED_COUNT = 40  # Number of LED pixels.
LED_PIN = 18  # GPIO pin connected to the pixels
LED_FREQ_HZ = 800000  # LED signal frequency in hertz
LED_DMA = 5  # DMA channel to use for generating signal
LED_BRIGHTNESS = 155  # Set to 0 for darkest and 255 for brightest
LED_INVERT = False  # True to invert the signal (when using NPN transistor level shift)

class Status(Enum):
    START = 0
    INLEVEL = 1
    BETWEENLEVELS = 2
    AFTER = 3

    def pred(self):
        if self is Status.AFTER:
            return Status.START
        else:
            return Status(self.value + 1)

    def succ(self):
        if self is Status.START:
            return Status.AFTER
        else:
            return Status(self.value - 1)

class ButtonPress(Enum):
    STARTGAME = 0
    REACT = 1

class Game:
    def __init__(self):
        self.current_position = [0]
        self.current_pointer_pos = random.randint(23,38)
        print(self.current_pointer_pos)
        self.current_level = 0
        self.status = Status.START
        self.score = 0
    
    def compare(self, current_pointer_pos, current_position):
        if current_position == current_pointer_pos - 20:
            self.score = self.score + 20
            print(self.score)
        else:
            self.score = self.score + (abs((current_pointer_pos - 20) - current_position [-1]))
            print(self.score)

    def button_input(self, button_pressed, status):
        if button_pressed is ButtonPress.START and status is Status.START:
            self.status = self.status.pred()
        elif button_pressed is ButtonPress.REACT and status is Status.INLEVEL:
            self.compare()
        else:
            pass

    def set_speed(self, current_level):
        # "speed" is actually a delay
        speed = (100 / 400 - 1 / 400 * current_level)
        return speed
    
    def level_move(self):
        for i in range(20):            
            head_pos = self.current_position[-1] 
            head_pos += 1
            move_position = head_pos
            self.current_position.append(move_position)
            print(self.current_position)
            #light_strip.setPixelColorRGB(move_position, x, x, x)
            speed = self.set_speed(current_level)
            time.sleep(speed)
            if button_pressed is ButtonPress.REACT:
                self.compare(self.current_pointer_pos, self.current_position)
                break
                
game = Game()
button_pressed = 0
current_level = 50
keyboard_input = input()
if keyboard_input is "r":
    button_pressed = ButtonPress.REACT
game.level_move()