import time

class pgui:
    def __init__(self):
        self.cursor = 0
        self.loc = 0  # variable to track index of top LCD line
        self.home = {"Sand Speed":0, "Belt Speed":0, "Thickness":0, "Direction":1, "Home Belt":False}
        self.run_display = [" Sand Speed:", " Belt Speed:", " Thickness:", " Direction:", " Home Belt"]

    def pwelcome(self): #print welcome
        print("---- SANDER ----")
        print("RasPi Zero W")

    def pscreen_home(self, screen):
        self.loc = 0
        print(">"+screen[self.loc][1:])
        print(screen[self.loc+1])

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

    def _cbf(self, screen, command):
        if command == 1:
            pass

def test():
    gui = pgui()
    gui.pwelcome()
    print "\n"
    time.sleep(.5)
    print"HOME"
    gui.pscreen_home(gui.run_display)
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

        gui.pscroll(gui.run_display, i)
        print "\n"

    print "TEST COMPLETE..."