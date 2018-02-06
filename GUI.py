#Graphic User Interface for Belt Sander 16x2 LCD
import RPi_I2C_driver
import time
import pigpio
#import Microstep_Driver as md
import serial
#import RPi.GPIO as gpio
#import threading

class gui:
    def __init__(self, pi):
        scroll = "scroll"
        function = "function"
        dictionary = "dictionary"
        list = "list"

        self.pi = pigpio.pi()
        self.motor1_enable_pin = 26 #enable pin for turning motor on/off
        self.motor2_enable_pin = 19

        self.pi.set_mode(self.motor1_enable_pin, pigpio.OUTPUT)
        self.pi.set_mode(self.motor2_enable_pin, pigpio.OUTPUT)

        self.pi.write(self.motor1_enable_pin, 0)
        self.pi.write(self.motor2_enable_pin, 0)

        self.lcd = RPi_I2C_driver.lcd() #Create lcd object

        self.lcd.lcd_load_custom_chars([[0x1F,0x1F,0x1F,0x1F,0x1F,0x1F,0x1F,0x1F]])

        self.teensy = serial.Serial("/dev/ttyACM0", 115200) #Initialize teensy serial communication

        self.cursor = 0 #Cursor value (relative to the entire screen dictionary)
        self.local_cursor = 0 #Cursor value (relative to the display size -- i.e. self.disp_rows)
        self.start = 0 #Holder remember which item to print first on lcd...

        #INPUT THE SIZE OF THE DISPLAY BELOW:
        self.disp_cols = 20
        self.disp_rows = 4

        if self.pi.read(22):
            self.state = "MANUAL"
        else:
            self.state = "HOME" #Start state is manual or "home" depending on initial switch state
        self.path = [] #Path is used to remember the current "location" in the gui dictionary. Will be a string of values to enter in dictionary

        self.home_screen = [" Sand Speed [%]: ", " Belt Speed [%]: ", " Thickness [\"]:", " Direction: ", " Home Belt"]
        home_screen = [[list, 0, ["OFF", "ON"]], [scroll, 0, 0, 100], [list, 0, self.range(0.125,4,0.125)], [list, 0,["FORWARD", "REVERSE"]], [function, self.home_belt]]
        self.home_dict = self.make_screen_dict(self.home_screen, home_screen)

        self.menu_dict = self.home_dict

    def make_screen_obj(self, screen, list): # method to make a list of objects / functions associated with a dictionary
        output = []
        for i in range(len(screen)):
            if list[i][0] == "scroll":
                obj = scroll_object(list[i][1], list[i][2], list[i][3])
                output.append(obj)
            elif list[i][0] == "list":
                obj = list_object(list[i][1], list[i][2])
                output.append(obj)
            elif list[i][0] == "function":
                output.append(list[i][1])
            elif list[i][0] == "dictionary":
                output.append(list[i][1])
        return output

    def make_screen_dict(self, screen, list): #method to make a dictionary for a screen with objects / functions
        dictionary = {}
        obj = self.make_screen_obj(screen, list)
        for i in range(len(screen)):
            if str(type(self)) == "<type 'instance'>" or callable(obj[i]) or str(type(self)) == "<type 'dict'>": #Check if dictionary item is acceptable and add to dictionary --- NOT DONE YET!!!
                d = {screen[i]:obj[i]}
                dictionary.update(d)
            else:
                pass

        return dictionary

    def range(self, start, stop, incr):
        i = []
        i.append(start)
        j = 0
        while i[j] < stop:
            i.append(i[j]+incr)
            j = j + 1

        return i

    def dict_loc(self): #Returns the dictionary based on current path
        dictionary = self.home_dict
        for i in self.path:
            dictionary = dictionary[i]

        return dictionary

    def prev_dict_loc(self): #Returns the dictionary based on previous path
        dictionary = self.home_dict
        for i in self.path[1:len(self.path)]:
            dictionary = dictionary[i]

    def welcome(self): #print welcome
        self.lcd.lcd_display_string("    BELT SANDER", 2)
        self.lcd.lcd_display_string("    RasPi Zero W", 3)

    def screen_home(self, screen):
        s = screen
        self.start = 0
        if len(s) < self.disp_rows:
            for i in range(len(s)):
                ob_type = str(type(self.menu_dict[s[i]]))
                if i == 0:
                    if ob_type == "<type 'instance'>":
                        val = str(self.menu_dict[s[i]].val())
                        self.lcd.lcd_display_string(">"+s[i][1:]+val, 1)
                    else:
                        self.lcd.lcd_display_string(">" + s[i][1:], 1)
                else:
                    if ob_type == "<type 'instance'>":
                        val = str(self.menu_dict[s[i]].val())
                        self.lcd.lcd_display_string(s[i]+val, 1)
                    else:
                        self.lcd.lcd_display_string(s[i], i + 1)

        else:
            for i in range(self.disp_rows):
                ob_type = str(type(self.menu_dict[s[i]]))
                if i == 0:
                    if ob_type == "<type 'instance'>":
                        val = str(self.menu_dict[s[i]].val())
                        self.lcd.lcd_display_string(">"+s[i][1:]+val, 1)
                    else:
                        self.lcd.lcd_display_string(">" + s[i][1:], 1)
                else:
                    if ob_type == "<type 'instance'>":
                        val = str(self.menu_dict[s[i]].val())
                        self.lcd.lcd_display_string(s[i]+val, i + 1)
                    else:
                        self.lcd.lcd_display_string(s[i], i + 1)

    def scroll(self, screen, command):
        #Get new cursor index and print new screens
        self.state = "HOME"
        s = []

        start = self.start
        local_cursor = self.local_cursor

        if self.cursor == len(screen)-1 and command == -1:
            self.cursor = 0
            self.local_cursor = 0
            self.start = 0
        elif command == -1:
            self.cursor -= command
            if self.local_cursor >= self.disp_rows - 1:
                self.local_cursor = self.disp_rows - 1
                self.start -= command
            else:
                self.local_cursor -= command

        elif self.cursor == 0 and command == 1:
            self.cursor = len(screen)-17
            self.local_cursor = self.disp_rows - 1
            self.start = len(screen) - (self.disp_rows)
        elif command == 1:
            self.cursor -= command
            if self.local_cursor == 0:
                self.start -= command
            else:
                self.local_cursor -= command

        else:
            s = None

        if start == self.start:
            self.lcd.lcd_display_string(" ", local_cursor+1, 0)
            self.lcd.lcd_display_string(">", self.local_cursor+1, 0)

        elif start != self.start and len(screen) < self.disp_rows + 1: #If screen is smaller than display...
            self.lcd.lcd_clear()
            for i in range(len(screen)):
                ob_type = str(type(self.menu_dict[screen[self.start+i]]))
                if i == self.local_cursor:
                    if ob_type == "<type 'instance'>":
                        val = str(self.menu_dict[screen[self.start+i]].val())
                        s.append(">" + screen[self.start+i] + val)
                    else:
                        s.append(">" + screen[self.start+i][1:])
                else:
                    s.append(screen[self.start+i])
            #If there is a new screen, print...
            if not s == None:
                for i in range(len(s)):
                    self.lcd.lcd_display_string(s[i], i+1)
            else:
                pass

        else:
            self.lcd.lcd_clear()
            for i in range(self.disp_rows):
                ob_type = str(type(self.menu_dict[screen[self.start+i]]))
                if i == self.local_cursor:
                    if ob_type == "<type 'instance'>":
                        val = str(self.menu_dict[screen[self.start+i]].val())
                        s.append(">" + screen[self.start+i][1:] + val)
                    else:
                        s.append(">" + screen[self.start+i][1:])
                else:
                    if ob_type == "<type 'instance'>":
                        val = str(self.menu_dict[screen[self.start+i]].val())
                        s.append(screen[self.start+i] + val)
                    else:
                        s.append(screen[self.start+i])

            #If there is a new screen, print...
            if not s == None:
                for i in range(len(s)):
                    self.lcd.lcd_display_string(s[i], i+1)
            else:
                pass

    def enter(self):
        if self.state == "HOME":
            dictionary = self.home_dict
            if str(type(self.home_dict[self.home_screen[self.cursor]])) == "<type 'instance'>":
                self.state = self.home_dict[self.home_screen[self.cursor]].state() #Necessary for object to have self.state() method...
            elif callable(self.home_dict[self.home_screen[self.cursor]]): #Call method if dictionary item is callable
                self.home_dict[self.home_screen[self.cursor]]()
            elif str(type(self.home_dict[self.home_screen[self.cursor]])) == "<type 'dict'>": #For nested dictionary -- How to navigate forwards/backwards?
                dictionary = self.home_dict[self.home_screen[self.cursor]]
        elif self.state == "SCROLLING":
            self.state = "HOME"
        else:
            dictionary = None

    def home_belt(self):
        self.teensy.write("1,2,0\\n") #Send serial message to teensy to home belt...

    def _cbf(self, gpio, level, tick): #, level, tick

        if self.pi.read(22):
            self.state = "MANUAL"
            print self.state
            command = 0
        elif gpio == 20:
            command = -1
        elif gpio == 16:
            command = 1
        elif gpio == 21 or gpio == 25:
            command = 3
        elif gpio == 22:
            if level == 0:
                self.state = "HOME"
                command = 0
            else:
                self.state = "MANUAL"
                command = 0 #Case should never occur but "else" statement ensures "command" will have a value...
        else:
            command = 0

        if self.state == "HOME":
            if command == 1 or command == -1:
                self.scroll(self.home_screen, command)
            elif command == 2 or command == -2:
                pass #Left to go "backwards" in dictionary  if possible. Right to go "forwards" in dictionary if possible.
            elif command == 3:
                self.enter()
                if not callable(self.home_dict[self.home_screen[self.cursor]]):
                    self.lcd.lcd_display_string("#", self.local_cursor+1)
        elif self.state == "SCROLLING":
            if command == 1 or command == -1:
                [self.state, x] = self.home_dict[self.home_screen[self.cursor]].scroll(command)#Scrolling object always has self.value attribute
                disp_string = "#"+self.home_screen[self.cursor][1:]+str(x)

                if len(disp_string) < self.disp_cols: #Depends on the width of the screen being used!!!
                    #flash_string = flash_string + " "*(self.disp_cols-len(disp_string))
                    disp_string = disp_string + " "*(self.disp_cols-len(disp_string))
                #self.lcd.lcd_display_string(flash_string, self.local_cursor + 1)
                self.lcd.lcd_display_string(disp_string, self.local_cursor+1)
                #self.lcd.lcd_display_string(unichr(0))

            elif command == -2:
                self.state = "HOME"

            elif command  == 3:
                self.state = "HOME"
                if self.home_screen[self.cursor] == " Belt Speed [%]: ":
                    if self.home_dict[" Direction: "].val() == "REVERSE":
                        teensy_str = "2,1,"+str(-1*self.home_dict[self.home_screen[self.cursor]].val())+str("\\n")
                    else:
                        teensy_str = "2,1," + str(self.home_dict[self.home_screen[self.cursor]].val()) + str("\\n")
                elif self.home_screen[self.cursor] == " Thickness [\"]:":
                    teensy_str = "1,1,"+str((4-(self.home_dict[self.home_screen[self.cursor]].val()))*1000)+str("\\n")
                elif self.home_screen[self.cursor] == " Direction: ":
                    if self.home_dict[" Direction: "].val() == "REVERSE":
                        teensy_str = "2,1,"+str(-1*self.home_dict[" Belt Speed [%]: "].val())+str("\\n")
                    else:
                        teensy_str = "2,1,"+str(self.home_dict[" Belt Speed [%]: "].val())+str("\\n")
                else:
                    teensy_str = ""
                self.teensy.write(teensy_str)
                self.lcd.lcd_display_string(">", self.local_cursor+1)
        elif self.state == "MANUAL":
            pass
        else:
            print "Invalid state"


class scroll_object: #Class for creating menu items with "scrollable" input -- For actual implementation need to allow user to hold button and scroll value
    def __init__(self, initial, lower, upper):
        self.value = initial
        self.lower = lower
        self.upper = upper

    def scroll(self, command):
        if command == 1: #To add or subtract from the value of scrollable object
            if self.value == self.upper:
                self.value = self.lower
            else:
                self.value += command
            state = "SCROLLING"
        elif command == -1:
            if self.value == self.lower:
                self.value = self.upper
            else:
                self.value += command
            state = "SCROLLING"
        elif command == -2: #To cancel changing the value of scrollable object
            state = "HOME"
        elif command == 3:
            state = "HOME"
        else:
            state = "SCROLLING"

        return [state, self.value]

    def state(self):
        return "SCROLLING"

    def val(self):
        return self.value

class list_object():
    def __init__(self, initial, list):
        self.incr = initial
        self.list = list
        self.value = self.list[initial]

    def scroll(self, command):
        if command == 1: #To add or subtract from the value of scrollable object
            if self.incr == len(self.list)-1:
                self.incr = 0
            else:
                self.incr += command
            state = "SCROLLING"
            self.value = self.list[self.incr]
        elif command == -1:
            if self.incr == 0:
                self.incr = len(self.list) - 1
            else:
                self.incr += command
            state = "SCROLLING"
            self.value = self.list[self.incr]
        elif command == -2: #To cancel changing the value of scrollable object
            state = "HOME"
        elif command == 3:
            state = "HOME"
        else:
            state = "SCROLLING"

        return [state, self.value]

    def state(self):
        return "SCROLLING"

    def val(self):
        return self.value

def run():

    pi = pigpio.pi()
    lcd = gui(pi)
    lcd.welcome()
    time.sleep(2.5)
    lcd.screen_home(lcd.home_screen)

    right = 21
    down = 20
    up = 16
    left = 12
    ok = 25
    man = 22

    #motor = md.stepper(pi, 26, 13, 19, 6)

    '''pi.set_pull_up_down(right, pigpio.PUD_UP)
    pi.set_pull_up_down(down, pigpio.PUD_UP)
    pi.set_pull_up_down(up, pigpio.PUD_UP)
    pi.set_pull_up_down(left, pigpio.PUD_UP)
    pi.set_pull_up_down(ok, pigpio.PUD_UP)'''

    pi.set_mode(right, pigpio.INPUT)
    pi.set_mode(down, pigpio.INPUT)
    pi.set_mode(up, pigpio.INPUT)
    pi.set_mode(left, pigpio.INPUT)
    pi.set_mode(ok, pigpio.INPUT)

    pi.callback(right, pigpio.RISING_EDGE, lcd._cbf)
    pi.callback(down, pigpio.RISING_EDGE, lcd._cbf)
    pi.callback(up, pigpio.RISING_EDGE, lcd._cbf)
    pi.callback(left, pigpio.RISING_EDGE, lcd._cbf)
    pi.callback(ok, pigpio.RISING_EDGE, lcd._cbf)
    pi.callback(man, pigpio.EITHER_EDGE, lcd._cbf)

    lcd.home_belt()

    while True:
        time.sleep(.00001)

if __name__ == "__main__":
    run()