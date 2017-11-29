import pigpio
import time

#Microstep Driver Class
#ENA must be ahead of DIR by at least 5us. Usually, ENA+ and ENA- are NC (not connected).
#DIR must be ahead of PUL active edge by 5us to ensure correct direction
#According to documentation, a pulse width should be no less than ~7.5 microseconds

class stepper():
    def __init__(self, pi, enable_pin, forward_pin, reverse_pin, pulse_pin):
        self.enable_pin = enable_pin
        self.forward_pin = forward_pin
        self.reverse_pin = reverse_pin
        self.pulse_pin = pulse_pin
        self.pi = pi
        self.pi.set_mode(self.enable_pin, pigpio.OUTPUT)
        self.pi.set_mode(self.forward_pin, pigpio.OUTPUT)
        self.pi.set_mode(self.reverse_pin, pigpio.OUTPUT)
        self.pi.set_mode(self.pulse_pin, pigpio.OUTPUT)
        self.pi.write(self.enable_pin, 0) #Enable low...
        self.pi.write(self.forward_pin, 0)
        self.pi.write(self.reverse_pin, 0)
        self.pi.write(self.pulse_pin, 0)

    def pulse_forward(self):
        self.pi.write(self.reverse_pin, 0)
        self.pi.write(self.forward_pin, 1)
        self.pi.write(self.pulse_pin, 1)
        time.sleep(10*10**-6)
        self.pi.write(self.pulse_pin, 0)

    def pulse_backward(self):
        self.pi.write(self.forward_pin, 0)
        self.pi.write(self.reverse_pin, 1)
        self.pi.write(self.pulse_pin, 1)
        time.sleep(10*10**-6)
        self.pi.write(self.pulse_pin, 0)

    def steps_forward(self, steps, delay):
        for i in range(steps):
            self.pulse_forward()
            time.sleep(delay)

    def steps_backward(self, steps, delay):
        for i in range(steps):
            self.pulse_backward()
            time.sleep(delay)

    def cleanup(self):
        self.pi.write(self.enable_pin, 1) #Disable the stepper
        self.pi.write(self.forward_pin, 0)#All pins low...
        self.pi.write(self.reverse_pin, 0)
        self.pi.write(self.pulse_pin, 0)
        self.pi.stop()

def forward_test(steps, delay):
    pi = pigpio.pi()
    motor = stepper(pi, 26, 13, 19, 6)
    motor.steps_forward(steps, delay)
    motor.cleanup()

if __name__ == "__main__":
    pass