import time

class pgui:
    def __init__(self):
        scroll = "scroll"
        function = "function"

        self.cursor = 0

        self.home_screen = [" Sand Speed:", " Belt Speed:", " Thickness:", " Direction:", " Home Belt"]
        home_screen = [[scroll, 0, 0, 100], [scroll, 0, 0, 100], [scroll, 6, 0, 100], [scroll, 0,-1, 1], [function, self.phome_belt]]
        self.home_dict = self.make_screen_dict(self.home_screen, home_screen)

    def make_screen_obj(self, screen, list): #method to make a list of objects / functions associated with a dictionary
        output = []
        for i in range(len(screen)):
            if list[i][0] == "scroll":
                obj = scroll_object(screen[i], list[i][1], list[i][2], list[i][3])
                output.append(obj)
            elif list[i][0] == "function":
                output.append(list[i][1])
        return output

    def make_screen_dict(self, screen, list): #method to make a dictionary for a screen with objects / functions
        dictionary = {}
        obj = self.make_screen_obj(screen, list)
        for i in range(len(screen)):
            if type(self) == type(obj[i]): #Dictionary item is an object
                d = {screen[i]:obj[i].value}
                dictionary.update(d)
            elif callable(obj[i]): #Dictionary item is a method
                d = {screen[i]:obj[i]}
                obj[i]()
                d[screen[i]]
                print d
                dictionary.update(d)
            else:
                print type(obj[i])
                print obj[i]

        print dictionary
        return dictionary

    def pwelcome(self): #print welcome
        print("---- SANDER ----")
        print("RasPi Zero W")

    def pscreen_home(self, screen):
        print(">"+screen[0][1:])
        print(screen[1])

    def pscroll(self, screen, dir):
        #Get new cursor index and print new screens
        if self.cursor == len(screen)-1 and dir == -1:
            self.cursor = 0
            s = [">"+screen[self.cursor][1:], screen[self.cursor+1]]
        elif dir == -1:
            self.cursor -= dir
            s = [screen[self.cursor-1], ">"+screen[self.cursor][1:]]
        elif self.cursor == 0 and dir == 1:
            self.cursor = len(screen)-1
            s = [screen[self.cursor-1], ">"+screen[self.cursor][1:]]
        elif dir ==1:
            self.cursor -= dir
            s = [">"+screen[self.cursor][1:], screen[self.cursor+1]]
        else:
            s = None
        #If there is a new screen, print...
        if not s == None:
            print s[0]
            print s[1]

    def penter(self, state):
        if state == "HOME":
            dictionary = self.home_dict
            screen = self.home_screen
        else:
            dictionary = None
            screen = None

        if not dictionary == None:
            pass
        else:
            pass

    def phome_belt(self):
        print "Homing Belt"

    def _cbf(self, state, command):
        if state == "HOME":
            screen = self.home_screen
        else:
            screen = None
            print "Invalid state"

        if command == 1 or command == -1:
            self.pscroll(screen, command)
        elif command == 2 or command == -2:
            print "L/R -- Not programmed"
        elif command == 3:
            self.penter(state)

class scroll_object:
    def __init__(self, name, initial, lower, upper):
        self.name = name
        self.value = initial
        self.lower = lower
        self.upper = upper

    def scroll(self, dictionary, command):
        current = dictionary[self.name]
        flag = True
        while flag:
            if command == 1 or command == -1:
                dictionary[self.name] += command
            elif command == -2:
                dictionary[self.name] = current
            elif command == 3:
                flag = False

    def val(self):
        return self.value

def test():
    gui = pgui()
    gui.pwelcome()
    print "\n"
    time.sleep(.5)
    state = "HOME"
    gui.pscreen_home(gui.home_screen)
    print"\n"
    time.sleep(.5)
    i = None

    while not i == "exit":
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

        gui._cbf(state, i)
        print "\n"

    print "TEST COMPLETE..."