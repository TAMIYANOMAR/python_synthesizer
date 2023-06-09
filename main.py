import threading
import initializer
import functions
import replayer
import recorder
import os

if __name__ == "__main__":
    
    thread = threading.Thread(target=functions.audioplay)
    thread.start()
    thread2 = threading.Thread(target=functions.key_input)
    thread2.start()
    
    while True:
        _initializer = initializer.Initializer()
        _initializer.print_greeting()

        tempo = _initializer.tempo_getter()
        play_mode = _initializer.playmode_getter()
        sound_mode = _initializer.soundmode_getter()
        shift = _initializer.shift_getter()
        key_board = _initializer.key_board_getter()
        
        functions.create_pitch()

        if _initializer.play_mode == 1:
            recorder_instance = recorder.Recorder(shift,tempo)
            recorder_instance.record(functions.pitch)
        elif _initializer.play_mode == 2:
            replayer_instance = replayer.Replayer(tempo,shift)
            replayer_instance.replay(functions.pitch)
        else:
            functions.play = True
            while functions.play:
                pass
            input("Press Enter to continue...")
            os.system('cls')
