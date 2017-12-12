import time

class pgui:
    def __init__(self):
        scroll = "scroll"
        function = "function"
        dictionary = "dictionary"
        list = "list"

        self.cursor = 0
        self.state = "HOME" #Start state will be home screen
        self.path = [] #Path is used to remember the current "location" in the gui dictionary. Will be a string of values to enter in dictionary

        self.some_screen = [" foo: ", " bar: "]
        some_screen = [[scroll, 0, 0, 100], [scroll, 0, 0, 100]]
        self.some_screen = self.make_screen_dict(self.some_screen, some_screen)

        self.home_screen = [" Sand Speed:", " Belt Speed:", " Thickness:", " Direction:", " Home Belt", " Dictionary"]
        home_screen = [[scroll, 0, 0, 100], [scroll, 0, 0, 100], [scroll, 6, 0, 100], [scroll, 0,-1, 1], [function, self.phome_belt], [dictionary, self.some_screen]]
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
            if str(type(self)) == "<type 'instance'>" or callable(obj[i]) or str(type(self )) == "<type 'dict'>": #Check if dictionary item is acceptable and add to dictionary
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

    def pwelcome(self): #print welcome
        print("---- SANDER ----")
        print("RasPi Zero W")

    def pscreen_home(self, screen):
        print(">"+screen[0][1:])
        print(screen[1])

    def pscroll(self, screen, command):
        #Get new cursor index and print new screens
        self.state = "HOME"
        if self.cursor == len(screen)-1 and command == -1:
            self.cursor = 0
            s = [">"+screen[self.cursor][1:], screen[self.cursor+1]]
        elif command == -1:
            self.cursor -= command
            s = [screen[self.cursor-1], ">"+screen[self.cursor][1:]]
        elif self.cursor == 0 and command == 1:
            self.cursor = len(screen)-1
            s = [screen[self.cursor-1], ">"+screen[self.cursor][1:]]
        elif command ==1:
            self.cursor -= command
            s = [">"+screen[self.cursor][1:], screen[self.cursor+1]]
        else:
            s = None
        #If there is a new screen, print...
        if not s == None:
            print s[0]
            print s[1]

    def penter(self):
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

    def phome_belt(self):
        state = self.state #Track previous state when calling method
        self.state = "HOMING"
        print "State: " + self.state
        time.sleep(.5)
        self.state = state #Return to previous state after homing.

    def _cbf(self, command):

        if self.state == "HOME":
            if command == 1 or command == -1:
                self.pscroll(self.home_screen, command)
            elif command == 2 or command == -2:
                print "L/R -- Not programmed" #Left to go "backwards" in dictionary  if possible. Right to go "forwards" in dictionary if possible.
            elif command == 3:
                self.penter()
        elif self.state == "SCROLLING":
            if command == 1 or command == -1:
                [self.state, x] = self.home_dict[self.home_screen[self.cursor]].scroll(command)#Scrolling object always has self.value attribute
                print str(self.home_screen[self.cursor]) + str(x)
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
    gui = pgui()
    gui.pwelcome()
    print "\n"
    time.sleep(.5)
    gui.pscreen_home(gui.home_screen)
    print"\n"
    time.sleep(.5)
    i = None

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

        gui._cbf(i)
        print "State: " +str(gui.state)
        print "\n"

    print "TEST COMPLETE..."
    return gui