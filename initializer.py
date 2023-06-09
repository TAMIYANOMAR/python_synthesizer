class Initializer:
  def __init__(self):
    self.tempo = 120
    self.play_mode = 0 #0:play 1:record 3:replay
    self.sound_mode = 0 #0:normal 1:8bit
    self.shift = 0
    self.key_board = 0 #0:US 1:JP
    
  def tempo_getter(self):
    return self.tempo

  def playmode_getter(self):
    return self.play_mode
  
  def soundmode_getter(self):
    return self.sound_mode
  
  def shift_getter(self):
    return self.shift
  
  def key_board_getter(self):
     return self.key_board

  def greeting(self):
    print(" ####")
    print("##  ##               ##    ##")
    print("##     ##  ## #####  ##### ##      ####   #### ## #####  ####  #####")
    print(" ####  ##  ## ##  ## ##    #####  ##  ## ##          ## ##  ## ##  ##")
    print("    ##  ##### ##  ## ##    ##  ## ###### ####  ##   ##  ###### ##")
    print("##  ##    ##  ##  ## ## ## ##  ## ##        ## ##  ##   ##     ##")
    print("####    ###   ##  ##  ###  ##  ##  ##### ####  ## #####  ##### ##")
    print("      ###")

  def input_int(self,*args):
    while True:
        try:
            num = int(input())
            if args[0] == "f":
                return int(num)
            elif int(num) in args:
                return int(num)
            print("Please Input Accurate Number")
        except ValueError:
            print("Please Input Number")


  def print_greeting(self):
    self.greeting()
    print("")
    print("Input play_mode (0:play 1:record 2:replay)")
    self.play_mode = int(self.input_int(0,1,2))
    print("Input sound_mode (0:normal 1:8bit)")
    self.sound_mode = int(self.input_int(0,1))
    print("Input number to shift pitch")
    self.shift = int(self.input_int("f"))
    if self.play_mode == 0:
        print("Input number to select keyboard (0:US 1:JP)")
        self.key_board = int(self.input_int(0,1))
        print("Start synthesizer : Press \"shift + a\" to down pitch , \"shift + d\" to up pitch")
        print("")
    elif self.play_mode == 1 or self.play_mode == 2:
        print("Input tempo")
        self.tempo = int(self.input_int("f"))