#Graphic User Interface for Belt Sander 16x2 LCD
import RPi_I2C_driver
import time
import pigpio

class gui:
    def __init__(self, pi, left, right, up, down, select):
        self.pi = pi
        self.run_display = [" Sand Speed:", " Belt Speed:", " Thickness:", " Direction:", " Home Belt"]
        self.left = left
        self.right = right
        self.up = up
        self.down = down
        self.select = select
        self.cursor = 0
        self.state = ""
        self.lcd = RPi_I2C_driver.lcd()

    def welcome(self):
        self.lcd.lcd_display_string("---- SANDER ----", 1)
        self.lcd.lcd_display_string("RasPi Zero W", 2)
        time.sleep(.5)
        self.lcd.lcd_clear()

    def screen_home(self, screen):
        self.cursor = 0
        self.lcd.lcd_display_string(screen[0], 1)
        self.lcd.lcd_display_string(screen[1], 2)

    def scroll(self, screen, dir):
        # Get new cursor index and print new screens
        if self.cursor == len(screen) - 1 and dir == -1:
            self.cursor = 0
            s = [">" + screen[self.cursor][1:], screen[self.cursor + 1]]
        elif dir == -1:
            self.cursor -= dir
            s = [screen[self.cursor - 1], ">" + screen[self.cursor][1:]]
        elif self.cursor == 0 and dir == 1:
            self.cursor = len(screen) - 1
            s = [screen[self.cursor - 1], ">" + screen[self.cursor][1:]]
        elif dir == 1:
            self.cursor -= dir
            s = [">" + screen[self.cursor][1:], screen[self.cursor + 1]]
        else:
            s = None

        if not s == None:
            self.lcd.lcd_display_string(s[0], 1)
            self.lcd.lcd_display_string(s[0], 2)

    def arrow_cursor(self, screen, i):
        pass

    def _cbf(self):
        pass

    def run(self):
        self.welcome()
        self.screen_home(self.run_display)
        self.cb_left = self.pi.callback(self.left, pigpio.RISING_EDGE, self._cbf)
        self.cb_right = self.pi.callback(self.right, pigpio.RISING_EDGE, self._cbf)
        self.cb_up = self.pi.callback(self.up, pigpio.RISING_EDGE, self._cbf)
        self.cb_down = self.pi.callback(self.down, pigpio.RISING_EDGE, self._cbf)
        self.cb_select = self.pi.callback(self.select, pigpio.RISING_EDGE, self._cbf)

def test():
    pi = pigpio.pi()
    left = 1
    right = 2
    up = 3
    down = 4
    select = 5
    g = gui(pi, left, right, up, down, select)
    g.welcome()
