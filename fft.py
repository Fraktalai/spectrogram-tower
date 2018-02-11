import pyaudio
import numpy
import array
import serial
import colorsys
import time
from color import convertPercentToColorValue

PORT = '/dev/cu.wchusbserial1430'
CHUNK = 1000
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 10000
MAX_MAG = 0
MIN_MAG = 0
        
def getMagnitude(real, imaginary):
    magnitudes = []
    x = 0
    while x < len(real) and x < len(imaginary):
        magnitudes.append(numpy.sqrt(real[x]*real[x] + imaginary[x]*imaginary[x]))
        x += 1
    return magnitudes

def getFrequencyIndex(freq):
    return freq / (RATE / CHUNK)

p = pyaudio.PyAudio()

stream = p.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    frames_per_buffer=CHUNK
)

arduino = serial.Serial(PORT)
time.sleep(2)
print "SERIAL NAME: " + arduino.name
print("recording")

try:
    while True:
        data = stream.read(CHUNK, exception_on_overflow = False)
        nums = array.array('h', data)
        results = numpy.fft.fft(nums)
        freq_bins = numpy.fft.fftfreq(len(nums), 1.0 / RATE)
        results = results[0:(len(results)/2 - 1)]
        freq_bins = 2 * freq_bins[0:(len(freq_bins) / 2 - 1)]
        
        # magnitudes
        mags = getMagnitude(results.real, results.imag)

        # min index
        lower_band_index = getFrequencyIndex(600)

        # frequency filter
        useful_freqs_temp = freq_bins[lower_band_index:]
        useful_freqs = freq_bins[0:57]

        # magnitude filter
        useful_mags_temp = mags[lower_band_index:]
        useful_mags = mags[0:57]

        MAX_MAG = max(useful_mags)
        MIN_MAG = min(useful_mags)

        print useful_freqs, len(useful_freqs)
        print useful_mags, len(useful_mags)

        for mag in useful_mags:
            if mag < MIN_MAG:
                mag = MIN_MAG
            elif mag > MAX_MAG:
                mag = MAX_MAG

            intensity = int((( (mag - MIN_MAG) * 127) / (MAX_MAG - MIN_MAG)))
            arduino.write(chr(intensity))

            
except KeyboardInterrupt:
    arduino.close()
    stream.stop_stream()
    stream.close()
    p.terminate()
