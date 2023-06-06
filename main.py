import threading
from pynput import keyboard
import functions

if __name__ == "__main__":
    thread = threading.Thread(target=functions.audioplay)
    thread.start()
    while True:
        functions.print_greeting()
        functions.create_pitch()
        if functions.play_mode == 1:
            functions.record()
        elif functions.play_mode == 2:
            functions.replay()
        else:
            with keyboard.Listener(on_release = functions.on_release,on_press = functions.on_press) as listener:
                listener.join()
