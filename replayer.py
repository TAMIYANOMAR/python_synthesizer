import os
import time
import math
class Replayer:
    def __init__(self, tempo, shift):
      self.music_notes = self.get_music_notes()
      self.tempo = tempo
      self.shift = shift
    
    def get_music_notes(self):
      music_notes = []
      path = "./music_notes"
      files = os.listdir(path)
      for file in files:
          music_notes.append(file.split(".")[0])
      return music_notes

    def replay(self,pitch):
      print("Input number to select music notes or \"e\" to exit")
      for i in range(len(self.music_notes)):
          print(str(i) + ":" + str(self.music_notes[i]))
      num = input()
      if num == "e":
          return
      else:
          music_num = self.music_notes[int(num)]
          f = open("./music_notes/" + music_num + ".txt","r")
          music_note = f.readlines()
          f.close()
          for note in music_note:
              core = note.split(",")
              for i in core:
                  if i == "s\n":
                      pitch.clear()
                      continue
                  if i == "c\n":
                      continue
                  pitch.append(440 * math.pow(2,(int(i) + self.shift) * (1/12.0)))
              time.sleep(1.00 /(self.tempo * 4 / 60.0))
          pitch.clear()