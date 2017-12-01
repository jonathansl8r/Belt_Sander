#Graphic User Interface for Belt Sander 16x2 LCD
import RPi_I2C_driver
import time
import pigpio

class gui:
    def __init__(self, pi, left, right, up, down, select):
        self.pi = pi
        self.run_display = [" Sand Speed: ", " Belt Speed: ", " Thickness: ", " Direction: ", " Home Belt"]
        self.left = left
        self.right = right
        self.up = up
        self.down = down
        self.select = select
        self.cursor = [0, 0]
        self.state = ""
        self.triggered = False

    def welcome(self, lcd):
        lcd.lcd_display_string("---- SANDER ----", 1)
        lcd.lcd_display_string("RasPi Zero W", 2)
        time.sleep(.2)
        lcd.lcd_clear()

    def disp_run_display(self, lcd, i):
        lcd.lcd_display_string(self.run_display[i], 1)
        lcd.lcd_display_string(self.run_display[i + 1], 2)
        self.cursor = i

    def scroll(self, screen, dir):
        if  self.cursor[0] == 0 and dir == -1:
            self.cursor[0] = 1
        elif self.cursor[0] == 1 and dir == -1:
            if len(screen) < self.cursor[0]+1:
                self.cursor[0] = 0
            else:
                self.cursor[0] += 1

    def arrow_cursor(self, screen, i):
        pass

    def _cbf(self):
        pass

    def run(self):
        lcd = RPi_I2C_driver.lcd()
        self.welcome(lcd)
        self.disp_run_display(lcd, 0)
        self.cb_left = self.pi.callback(self.left, pigpio.RISING_EDGE, self._cbf)
        self.cb_right = self.pi.callback(self.right, pigpio.RISING_EDGE, self._cbf)
        self.cb_up = self.pi.callback(self.up, pigpio.RISING_EDGE, self._cbf)
        self.cb_down = self.pi.callback(self.down, pigpio.RISING_EDGE, self._cbf)
        self.cb_select = self.pi.callback(self.select, pigpio.RISING_EDGE, self._cbf)