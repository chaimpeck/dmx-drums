import dmx  # https://github.com/bitbyt3r/dmx
from time import sleep, time
import math
from threading import Thread
import mido

TOTAL_EASING_TIME = 500 # milliseconds
MIDI_USB_NAME = 'Simmons e-Drum:Simmons e-Drum MIDI 1 24:0'

# from here https://easings.net/#easeOutElastic
def ease(x: float):
    c4 = (2 * math.pi) / 3
    
    if x == 0 or x == 1:
        return x

    return math.pow(2, -10 * x) * math.sin((x * 10 - 0.75) * c4) + 1;

class Lights:
    def __init__(self, channel=1):
        self.channel = channel
        self.sender = dmx.DMX_Serial()
        self.current_color = None
        self.last_pulse_time = None
        self.update_thread = Thread(target=self.updater)
        self.update_thread.daemon = True

        self.sender.start()
        self.update_thread.start()

    def updater(self):
        while True:
            if not self.current_color or not self.last_pulse_time:
                continue
            
            duration = 1000 * (time() - self.last_pulse_time) # milliseconds
            x = min(duration / TOTAL_EASING_TIME, 1.)

            # amp = ease(min(duration / TOTAL_EASING_TIME, 1.))

            amp = 1. - x            
            self.sender.set_data(
                [0,] * (self.channel - 1) + 
                [int(amp * 255), ] + 
                self.current_color
            )

    def set_color(self, color):
        self.current_color = color
        self.last_pulse_time = time()



def demo():
    lights = Lights()
    for color in (
        [255,0,0],
        [0,255,0],
        [0,0,255],
        [0,255,255],
        [255,0,255],
        [255,255,0],
        [255,255,255]
    ):
        lights.set_color(color)
        sleep(.5)

def listen_midi():
    lights = Lights()
    with mido.open_input(MIDI_USB_NAME) as inport:
        for msg in inport:
            if msg.type == "note_on":
                lights.set_color([255,255,255])
                print(msg.velocity)
                #time.sleep(.02)

if __name__ == "__main__":
    listen_midi()
    sleep(.1)

    