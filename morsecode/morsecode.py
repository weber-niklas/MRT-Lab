import machine

from time import sleep
from machine import Pin

led = Pin(25, Pin.OUT)
word = input("Was möchten Sie ausgeben? \n")
word = word.upper()


def greenLightOn():       # 0 --> short;
    print("Green on!")
    led.value(1)
    sleep(0.1)
    led.value(0)


def redLightOn():         # 1-->long
    print("Red on!")
    led.value(1)
    sleep(0.5)
    led.value(0)

letters: dict = {"A": [0,1], "B": [1,0,0,0], "C": [1,0,1,0], "D": [1,0,0], "E": [0], "F": [0,0,1,0], "G": [1,1,0],
                    "H": [0,0,0,0], "I": [0,0], "J": [0,1,1,1], "K": [1,0,1], "L": [0,1,0,0], "M": [1,1], "N": [1,0],
                    "O": [1,1,1], "P": [0,1,1,0], "Q": [1,1,0,1], "R": [0,1,0], "S": [0,0,0], "T": [1], "U": [0,0,1],
                    "V": [0,0,0,1], "W": [0,1,1], "X": [1,0,0,1], "Y": [1,0,1,1], "Z": [1,1,0,0], " ": [2],
                    "Ä": [0,1,0,1], "Ö": [0,0,0,1], "Ü": [0,0,1,1]}


for char in word:
    print(letters[char])

    for signal in letters[char]:
        print(signal)

        if signal == 0:
            greenLightOn()
        elif signal == 1:
            redLightOn()
        elif signal == 2:
            sleep(0.2)

