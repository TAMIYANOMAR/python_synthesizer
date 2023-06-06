import os
music_notes = []
path = "./music_notes"
files = os.listdir(path)
for file in files:
    music_notes.append(int(file.split(".")[0]))
print(music_notes)
