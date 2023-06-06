import math
import numpy as np
import pyaudio
import struct
import threading
from pynput import keyboard
import os
import time
import functions

RATE= 44100        
bufsize = 256
play_mode = 0 #0:play 1:record 3:replay
sound_mode = 0 #0:normal 1:8bit
shift = 0
pitch = []
key_board = 0

# 音階の周波数を定義
key_name =        ["z","s","x","d","c","v","g","b","h","n","j","m",",","l",".",";","/","q","2","w","3","e","r","5","t","6","y","7","u","i","9","o","0","p","[","=","]","\\"]
key_name_for_jp = ["z","s","x","d","c","v","g","b","h","n","j","m",",","l",".",";","/","q","2","w","3","e","r","5","t","6","y","7","u","i","9","o","0","p","@","[",":","]" ]
key_diff =        [-9 ,-8 ,-7 ,-6 ,-5 ,-4 ,-3 ,-2 ,-1 , 0 , 1 , 2 , 3 , 4 , 5 , 6 , 7 , 3 , 4 , 5 , 6 , 7 , 8 , 9 ,10 , 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 24 ]
key_frequency = {}
music_notes = []
tempo = 120
x=np.arange(bufsize)
pos = 0 #位相（波形を保つための変数）

def print_greeting():
    global sound_mode , shift , key_board , play_mode , tempo
    print(" ####")
    print("##  ##               ##    ##")
    print("##     ##  ## #####  ##### ##      ####   #### ## #####  ####  #####")
    print(" ####  ##  ## ##  ## ##    #####  ##  ## ##          ## ##  ## ##  ##")
    print("    ##  ##### ##  ## ##    ##  ## ###### ####  ##   ##  ###### ##")
    print("##  ##    ##  ##  ## ## ## ##  ## ##        ## ##  ##   ##     ##")
    print("####    ###   ##  ##  ###  ##  ##  ##### ####  ## #####  ##### ##")
    print("      ###")
    print("")
    print("Input 0 or 1 , 2 to play_mode select (0:play 1:record 2:replay)")
    play_mode = int(input())
    print("Input 0 or 1 to sound_mode select (0:normal 1:8bit)")
    sound_mode = int(input())
    print("Input number to shift pitch")
    shift = int(input())
    if play_mode == 0:
        print("Input number to select keyboard (0:US 1:JP)")
        key_board = int(input())
        print("Start synthesizer : Press \"shift + a\" to down pitch , \"shift + d\" to up pitch")
        print("")
    elif play_mode == 1 or play_mode == 2:
        print("Input tempo")
        tempo = int(input())


def synthesize():
    global pos , sound_mode
    wave = np.zeros(bufsize)

    if len(pitch) == 0: #リストに音階が入っていないときは何もしない
        return wave

    for i in pitch: #リストに追加されている音階を合成
        t = i * (x+pos) / RATE
        t = t - np.trunc(t)
        
        wave += np.sin(2.0*np.pi*t)
        wave -= np.sin(2.0*np.pi*t*t)
        wave += np.sin(2.0*np.pi*t*t*t)
        if sound_mode == 1:
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
    # 動的に音量を変更するのは逆に良くない、安定しない
    if len(pitch) > 4:
        volume = 0.1 * 3 / 6
    else:
        volume = 0.1
    wave = wave * volume
    pos += bufsize

    return wave


# 音を再生する関数
def audioplay():
    p = pyaudio.PyAudio()
    stream=p.open(format = pyaudio.paInt16,
            channels = 1,
            rate = RATE,
            frames_per_buffer = bufsize,
            output = True)

    while stream.is_active():
        buf = functions.synthesize()
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
    global pitch , shift
    try:
        if key.char == 'A':
            shift -= 1
            create_pitch()
        elif key.char == 'D':
            shift += 1
            create_pitch()
        if key.char in key_frequency and key_frequency[key.char] not in pitch:
            pitch.append(key_frequency[key.char]) #リストに音階を追加
    except AttributeError:
        pass






def create_pitch():
    global key_frequency,key_name,key_diff,shift,key_name_for_jp,key_board
    if key_board == 0:
        for key,diff in zip(key_name,key_diff):
            key_frequency[key] = 440 * math.pow(2,(diff + shift) * (1/12.0))
    else:
        for key,diff in zip(key_name_for_jp,key_diff):
            key_frequency[key] = 440 * math.pow(2,(diff + shift) * (1/12.0))

def get_music_notes():
    global music_notes
    music_notes = []
    path = "./python_project/python_synthesizer/music_notes"
    files = os.listdir(path)
    for file in files:
        music_notes.append(file.split(".")[0])

def record():
    global pitch , shift
    print("Input music notes")
    print("Input \"e\" to finish or \"p\" to play , \"d\" to delete")
    music_note = []
    note_count = 0
    while True:
        note = input()
        if note == "e":
            break
        elif note == "p":
            for note in music_note:
                core = note.split(",")
                for i in core:
                    if i == "s":
                        pitch = []
                        continue
                    if i == "c":
                        continue
                    pitch.append(440 * math.pow(2,(int(i) + shift) * (1/12.0)))
                time.sleep(1.00 /(tempo * 4 / 60.0))
            pitch.clear()
            print("")
            print("Input music notes")
            print("Input \"e\" to finish or \"p\" to play , \"d\" to delete")
            for note in music_note:
                print(note)
        elif note == "d":
            music_note.pop(note_count - 1)
            note_count -= 1
            print("")
            print("Input music notes")
            print("Input \"e\" to finish or \"p\" to play , \"d\" to delete")
            for note in music_note:
                print(note)
        else:
            music_note.append(note)
            note_count += 1
    if len(note) > 0:
        print("Input music name")
        music_name = input()
        music_name = music_name + ".txt"
        f = open("./python_project/python_synthesizer/music_notes/" + music_name,"w")
        for note in music_note:
            f.write(note + "\n")
        f.close()
    return

def replay():
    global music_notes, pitch
    get_music_notes()
    print("Input number to select music notes or \"e\" to exit")
    for i in range(len(music_notes)):
        print(str(i) + ":" + str(music_notes[i]))
    num = input()
    if num == "e":
        return
    else:
        music_num = music_notes[int(num)]
        f = open("./python_project/python_synthesizer/music_notes/" + music_num + ".txt","r")
        music_note = f.readlines()
        f.close()
        for note in music_note:
            core = note.split(",")
            for i in core:
                if i == "s\n":
                    pitch = []
                    continue
                if i == "c\n":
                    continue
                pitch.append(440 * math.pow(2,(int(i) + shift) * (1/12.0)))
            time.sleep(1.00 /(tempo * 4 / 60.0))
        pitch.clear()