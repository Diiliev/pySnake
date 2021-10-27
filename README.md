# pySnake
This is the game Snake written in python.

# Credit where credit is due
This project is my interpretation of "Code Bro"'s tutorial: "Python snake game 🐍". You can watch it here: https://youtu.be/bfRwxS5d0SI

# How to play
You can download the executable game file from dist/Snake.exe.
The snake is controlled with the arrow keys, glhf.

# How to generate executable
```
$ pyinstaller --exclude-module _bootlocale -F -w -i icon/Snake.ico Snake.py
```