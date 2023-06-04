import math
import numpy as np
import pyaudio
import struct
import threading
from pynput import keyboard

RATE= 44100        
bufsize = 256
pitch = []

key_name = ["z","s","x","d","c","v","g","b","h","n","j","m",",","l",".",";","/","q","2","w","3","e","r","5","t","6","y","7","u","i","9","o","0","p","[","=","]", "\\"]
key_diff = [-9 ,-8 ,-7 ,-6 ,-5 ,-4 ,-3 ,-2 ,-1 , 0 , 1 , 2 , 3 , 4 , 5 , 6 , 7 , 3 , 4 , 5 , 6 , 7 , 8 , 9 ,10 , 11, 12, 13, 14, 15, 16, 17, 18, 19, 20 ,21 ,22, 24]
key_frequency = {}
for key,diff in zip(key_name,key_diff):
  key_frequency[key] = 440 * math.pow(2,diff * (1/12.0))

x=np.arange(bufsize)
pos = 0
def synthesize():
    global pos
    wave = np.zeros(bufsize)
    for i in pitch:
        t = i * (x+pos) / RATE
        t = t - np.trunc(t)
        
        wave += np.sin(2.0*np.pi*t)
        wave -= np.sin(2.0*np.pi*t*t)
        wave += np.sin(2.0*np.pi*t*t*t)
        wave -= np.sin(15*np.pi*t) * 0.25
        wave += np.sin(8.5*np.pi*t) * 0.25
        wave -= np.sin(4.2*np.pi*t) * 0.22
        wave += np.sin(1*np.pi*t) * 0.23
        wave -= np.sin(0.120*np.pi*t) * 0.18
        wave += np.sin(0.215*np.pi*t) * 0.156
        wave -= np.sin(1.1*np.pi*t) * 0.134
        wave += np.sin(0.545*np.pi*t) * 0.25
        wave -= np.sin(4*np.pi*t*t) * 0.125
        wave += np.sin(1*np.pi*t*t) * 0.125
        wave -= np.sin(0.123*np.pi*t*t) * 0.121
        wave += np.sin(0.225*np.pi*t*t) * 0.125
        wave -= np.sin(1.2*np.pi*t*t) * 0.124
        wave += np.sin(0.54*np.pi*t*t) * 0.138

    wave_max = np.max(wave)
    print(wave_max)
    if len(pitch) > 4:
        volume = 0.1 * 3 / 6
    else:
        volume = 0.1
    wave = wave * volume
    pos += bufsize

    if len(pitch) == 0:
        velosity = 0.0
    else:
        velosity = 1.0
    wave = velosity * wave

    return wave

playing = 1
def audioplay():
    print ("Start Streaming")
    p=pyaudio.PyAudio()
    stream=p.open(format = pyaudio.paInt16,
            channels = 1,
            rate = RATE,
            frames_per_buffer = bufsize,
            output = True)

    while stream.is_active():
        buf = synthesize()
        buf = (buf * 32768.0).astype(np.int16)#16ビット整数に変換
        buf = struct.pack("h" * len(buf), *buf)
        stream.write(buf)
        if playing == 0:
            break


def on_release(key):
    global pitch
    try:
        if key.char in key_frequency:  
            pitch.remove(key_frequency[key.char])
    except AttributeError:
        pass

def on_press(key):
    global pitch
    try:
        if key.char in key_frequency and key_frequency[key.char] not in pitch:
            pitch.append(key_frequency[key.char])
    except AttributeError:
        pass

if __name__ == "__main__": 
    thread = threading.Thread(target=audioplay)
    thread.start()
    with keyboard.Listener(on_release=on_release,on_press=on_press) as listener:
        listener.join()
