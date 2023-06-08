# Python-Synthesizer-CLI
- キー配置はピアノと似たようなイメージ
- exeファイル
    - /dist 
- テンポ:tempo
- キーコンフィグ:key config (0:US,1:JP)
- 音:sound(0:normalモード,1:8ビットモード)
- 動作モード:mode(0:演奏モード,1:記録モード、2:リプレイモード)
- 記録モード:record mode
    - 数字（キー）を組み合わせて音を構成する（2,-4,6)など:make sound with int figures like (2,-4,6) 
    - dを入力すると一つ前の音を削除できる:input d and delete former input(sound)
    - cを入力すると前の音を継続する:input s and c continue former input(sound)
    - sを入力すると休符が入る:input s and mute all sound
    - eを入力すると記録を終了:input e and end record
- リプレイモード
    - 利用可能ファイルが表示されるので数字で選択:input figure of file to replay
![image](https://github.com/TAMIYANOMAR/python_synthesizer/assets/59043309/3a6ed3fa-7fc8-4037-a6b5-223071f851b3)
