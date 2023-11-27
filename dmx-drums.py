import dmx  # https://github.com/bitbyt3r/dmx
from time import sleep, time
import math
from threading import Thread
import mido

TOTAL_EASING_TIME = 500 # milliseconds
MIDI_USB_NAME = 'Simmons e-Drum:Simmons e-Drum MIDI 1 24:0'
NOTE_COLOR_MAP = {
    36: [255, 0, 0], # kick drum
    66: [255, 0, 0], # alt kick drum
    41: [255, 0, 50], # floor tom
    71: [255, 30, 50], # mid tom
    67: [255, 70, 50], # high tom
    38: [255, 255, 255], # snare
    49: [0, 100, 255], # closed hi hat
    55: [0, 255, 100], # open hi hat
    61: [0, 255, 0], # ride cymbal
    73: [0, 255, 255], # crash cymbal
    65: [0, 255, 100], # wood block

}

def ease(x: float):
    # cubic ease out
    return 1. - x * x * x

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

            amp = ease(x)

            # amp = 1. - x            
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
            if msg.type == "note_on" and msg.velocity > 0:
                # TODO: consider using velocity to control easing time or initial intensity
                color = NOTE_COLOR_MAP.get(msg.note, [255, 255, 255])
                lights.set_color(color)
                print(msg.velocity, msg.note, color)
        time.sleep(.00001)

if __name__ == "__main__":
    demo()
    #listen_midi()
    sleep(.1)

    