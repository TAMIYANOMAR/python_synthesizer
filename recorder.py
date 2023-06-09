import time
import math

class Recorder:
  def __init__(self,shift,tempo):
      self.shift = shift
      self.tempo = tempo
    
  def record(self, pitch):
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
                        pitch.clear()
                        continue
                    if i == "c":
                        continue
                    pitch.append(440 * math.pow(2,(int(i) + self.shift) * (1/12.0)))
                time.sleep(1.00 /(self.tempo * 4 / 60.0))
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
        f = open("./music_notes/" + music_name,"w")
        for note in music_note:
            f.write(note + "\n")
        f.close()
    return