import math
import numpy as np
import pyaudio
import struct
import threading
from pynput import keyboard

RATE= 44100        
bufsize = 256
mode = 0
shift = 0
pitch = []

# 音階の周波数を定義
key_name = ["z","s","x","d","c","v","g","b","h","n","j","m",",","l",".",";","/","q","2","w","3","e","r","5","t","6","y","7","u","i","9","o","0","p","[","=","]", "\\"]
key_diff = [-9 ,-8 ,-7 ,-6 ,-5 ,-4 ,-3 ,-2 ,-1 , 0 , 1 , 2 , 3 , 4 , 5 , 6 , 7 , 3 , 4 , 5 , 6 , 7 , 8 , 9 ,10 , 11, 12, 13, 14, 15, 16, 17, 18, 19, 20 ,21 ,22, 24]
key_frequency = {}



x=np.arange(bufsize)
pos = 0 #位相（波形を保つための変数）
# 波形を生成する関数
def synthesize():
    global pos , mode
    wave = np.zeros(bufsize)

    if len(pitch) == 0: #リストに音階が入っていないときは何もしない
        return wave

    for i in pitch: #リストに追加されている音階を合成
        t = i * (x+pos) / RATE
        t = t - np.trunc(t)
        
        wave += np.sin(2.0*np.pi*t)
        wave -= np.sin(2.0*np.pi*t*t)
        wave += np.sin(2.0*np.pi*t*t*t)
        if mode == 1:
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

    # 音量が大きくなりすぎないように調整
    if len(pitch) > 4:
        volume = 0.1 * 3 / 6
    else:
        volume = 0.1
    wave = wave * volume
    pos += bufsize

    return wave

# 音を再生する関数
def audioplay():
    p=pyaudio.PyAudio()
    stream=p.open(format = pyaudio.paInt16,
            channels = 1,
            rate = RATE,
            frames_per_buffer = bufsize,
            output = True)

    while stream.is_active():
        buf = synthesize()
        buf = (buf * 32768.0).astype(np.int16)
        buf = struct.pack("h" * len(buf), *buf)
        stream.write(buf)


# キー入力を受け付ける関数（キーを離したとき）
def on_release(key):
    global pitch
    try:
        if key.char in key_frequency:  
            pitch.remove(key_frequency[key.char]) #リストに入っている音階を削除
    except AttributeError:
        pass

# キー入力を受け付ける関数（キーを押したとき）
def on_press(key):
    global pitch
    try:
        if key.char in key_frequency and key_frequency[key.char] not in pitch:
            pitch.append(key_frequency[key.char]) #リストに音階を追加
    except AttributeError:
        pass

def print_greeting():
    global mode , shift
    print(" ####")
    print("##  ##               ##    ##")
    print("##     ##  ## #####  ##### ##      ####   #### ## #####  ####  #####")
    print(" ####  ##  ## ##  ## ##    #####  ##  ## ##          ## ##  ## ##  ##")
    print("    ##  ##### ##  ## ##    ##  ## ###### ####  ##   ##  ###### ##")
    print("##  ##    ##  ##  ## ## ## ##  ## ##        ## ##  ##   ##     ##")
    print("####    ###   ##  ##  ###  ##  ##  ##### ####  ## #####  ##### ##")
    print("      ###")
    print("")
    print("Press 0 or 1 to mode select (0:normal 1:8bit)")
    mode = int(input())
    print("Press number to shift pitch")
    shift = int(input())

def create_pitch():
    global key_frequency,key_name,key_diff,shift
    for key,diff in zip(key_name,key_diff):
        key_frequency[key] = 440 * math.pow(2,(diff + shift) * (1/12.0))

if __name__ == "__main__":
    print_greeting()
    create_pitch()
    thread = threading.Thread(target=audioplay)
    thread.start()
    with keyboard.Listener(on_release=on_release,on_press=on_press) as listener:
        listener.join()
