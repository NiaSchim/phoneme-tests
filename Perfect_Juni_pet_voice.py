import numpy as np
from math import sin
import math
from random import uniform
from pynkTrombone.voc import Voc
import pyaudio
import signal
import sys

def play_random_tongue_positions(stream, voc, pitch=567*(1+(2/9))):
    running = True
    counter = 0

    def signal_handler(sig, frame):
        nonlocal running
        running = False

    signal.signal(signal.SIGINT, signal_handler)

    while running:
        tongue_pos = uniform(0,1) #scale of zero to one?
        tongue_diam = math.pi #scale of zero to one?
        mouth_pos = sin(counter * 0.01) * 0.5 + 0.5

        voc.tongue_shape(tongue_pos, tongue_diam)
        voc.tract_diameters[22] = mouth_pos
        voc.frequency = pitch

        output = voc.play_chunk()
        output = (output * 32767).astype(np.int16)
        stream.write(output.tobytes())
        counter += 1

    stream.stop_stream()
    stream.close()


if __name__ == '__main__':
    voc = Voc(44100)
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=44100,
                    output=True,
                    frames_per_buffer=1024)

    print("Press Ctrl+C to stop playing the sound.")
    play_random_tongue_positions(stream, voc)

    p.terminate()
