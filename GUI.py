#Graphic User Interface for Belt Sander 16x2 LCD
import RPi_I2C_driver
#import time
#import pigpio

import time

class gui:
    def __init__(self):
        scroll = "scroll"
        function = "function"
        dictionary = "dictionary"
        list = "list"

        self.lcd = RPi_I2C_driver.lcd()

        self.cursor = 0 #cursor value (relative to the entire screen dictionary)
        self.local_cursor = 0 #cursor value (relative to the display size -- i.e. self.disp_rows)
        self.start = 0 #remember which item to print first on lcd...
        self.disp_rows = 4

        self.state = "HOME" #Start state will be home screen
        self.path = [] #Path is used to remember the current "location" in the gui dictionary. Will be a string of values to enter in dictionary

        #self.some_screen = [" foo: ", " bar: "]
        #some_screen = [[scroll, 0, 0, 100], [scroll, 0, 0, 100]]
        #self.some_screen = self.make_screen_dict(self.some_screen, some_screen)

        self.home_screen = [" Sand Speed [%]: ", " Belt Speed [%]: ", " Thickness [\"]: ", " Direction: ", " Home Belt"]
        home_screen = [[scroll, 0, 0, 100], [scroll, 0, 0, 100], [scroll, 6, 0, 100], [scroll, 0,-1, 1], [function, self.home_belt]]
        self.home_dict = self.make_screen_dict(self.home_screen, home_screen)

        self.menu_dict = self.home_dict

    def make_screen_obj(self, screen, list): #method to make a list of objects / functions associated with a dictionary
        output = []
        for i in range(len(screen)):
            if list[i][0] == "scroll" or list[i][0] == "list":
                obj = scroll_object(list[i][1], list[i][2], list[i][3])
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
        while i[j] <= stop:
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
        self.lcd.lcd_display_string("    BELT SANDER", 1)
        self.lcd.lcd_display_string("    RasPi Zero W", 2)
        time.sleep(1)
        self.lcd.lcd_clear()

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
        self.lcd.lcd_clear()

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
            self.cursor = len(screen)-1
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

        if len(screen) < self.disp_rows + 1: #If screen is smaller than display...
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
        else:
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
        state = self.state #Track previous state when calling method
        self.state = "HOMING"
        print "State: " + self.state
        time.sleep(.5)
        self.state = state #Return to previous state after homing.

    def _cbf(self, command):

        if self.state == "HOME":
            if command == 1 or command == -1:
                self.scroll(self.home_screen, command)
            elif command == 2 or command == -2:
                print "L/R -- Not programmed" #Left to go "backwards" in dictionary  if possible. Right to go "forwards" in dictionary if possible.
            elif command == 3:
                self.enter()
        elif self.state == "SCROLLING":
            if command == 1 or command == -1:
                [self.state, x] = self.home_dict[self.home_screen[self.cursor]].scroll(command)#Scrolling object always has self.value attribute
                print str(self.home_screen[self.cursor]) + str(x)
                disp_string = ">"+self.home_screen[self.cursor][1:]+str(x)
                if len(disp_string) < 20: #Depends on the width of the screen being used!!!
                    disp_string = disp_string + " "*(20-len(disp_string))
                self.lcd.lcd_display_string(disp_string, self.local_cursor+1)
            elif command == -2:
                self.state = "HOME"
            elif command  == 3:
                self.state = "HOME"
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
            if self.incr == self.list[len(self.list)-1]:
                self.incr = self.list[0]
            else:
                self.incr += command
                self.value = self.list[self.incr]
            state = "SCROLLING"
        elif command == -1:
            if self.incr == self.list[0]:
                self.incr = self.list[len(self.list)-1]
            else:
                self.incr += command
                self.value = self.list[self.incr]
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

def test():
    lcd = gui()
    lcd.welcome()
    lcd.screen_home(lcd.home_screen)

    print "Local Cursor: " + str(lcd.local_cursor)
    print "Global Cursor: " + str(lcd.cursor)
    print "Start Point: " + str(lcd.start)
    print "\n"

    #while not i == "exit":
    while True:
        i = raw_input("Command: ")
        if i == "w":
            i = 1
        elif i == "s":
            i = -1
        elif i == "e":
            i = 3
        elif i == "a":
            i = -2
        elif i == "d":
            i = 2
        elif i == "exit":
            break

        lcd._cbf(i)
        print "\n"

    lcd.lcd.lcd_clear()
    print "TEST COMPLETE..."

if __name__ == "__main__":
    pass