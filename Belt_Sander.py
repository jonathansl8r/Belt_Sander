import Queue
import pigpio
import threading
import RPi_I2C_driver
import time
from Microstep_Driver import stepper
from Sonar import ranger

#i2c Driver: https://gist.github.com/DenisFromHR/cc863375a6e19dce359d

class belt_sander(threading.Thread):
    def __init__(self, sonar, sonar_queue):
        self.sonar = sonar
        threading.Thread.__init__(self)
        self.sonar_threads = []
        self.sonar_queue = sonar_queue

    def sonar_read(self, sonar): #Method for creating sonar thread and taking a distance reading
        started = False
        reading = True
        while reading:
            if not started:
                started = True
                th_sonar = threading.Thread(target=sonar.read)
                th_sonar.setDaemon(False)
                th_sonar.start()
                self.sonar_threads += [th_sonar] #Make a list of all sonar threads created

            elif reading and not self.sonar_queue.empty():
                reading = False #Need to revise so value not removed from queue

    def sonar_cleanup(self):
        for i in self.sonar_threads:
            if not i.isAlive():
                i.join()
            else:
                pass

    def sonar_thread_cleanup(self, threads):
        for i in threads:
            if not i.isAlive():
                i.join()
            else:
                pass

if __name__ == "__main__":
    pi = pigpio.pi()
    sonar_queue = Queue.Queue()
    sonar = ranger(pi=pi, trigger=22, echo=5, queue=sonar_queue)

    lcd = RPi_I2C_driver.lcd()
    lcd.lcd_display_string("Belt Sander ON", 1)
    time.sleep(.5)
    lcd.lcd_clear()