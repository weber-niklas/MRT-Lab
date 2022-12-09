# 1. Get User input
# 1.1 Validate User Input (only chars not ints etc.)
# 1.2 convert input to lower/ upper case

from utime import sleep
import machine

led_red = machine.Pin(14, machine.Pin.OUT) #Pin 19, long signel
led_green = machine.Pin(15, machine.Pin.OUT) #Pin 20, short signal
# user input
sentence: str = input("What would you like to translate to morsecode? \n")

# exeptions input
# TODO internet

sentence = sentence.upper()

# Dictionary with mosel alphabet
alph_signals: dict = {"A": [0,1], "B": [1,0,0,0], "C": [1,0,1,0], "D": [1,0,0], "E": [0], "F": [0,0,1,0], "G": [1,1,0],
                    "H": [0,0,0,0], "I": [0,0], "J": [0,1,1,1], "K": [1,0,1], "L": [0,1,0,0], "M": [1,1], "N": [1,0],
                    "O": [1,1,1], "P": [0,1,1,0], "Q": [1,1,0,1], "R": [0,1,0], "S": [0,0,0], "T": [1], "U": [0,0,1],
                    "V": [0,0,0,1], "W": [0,1,1], "X": [1,0,0,1], "Y": [1,0,1,1], "Z": [1,1,0,0], " ": [2],
                    "Ä": [0,1,0,1], "Ö": [0,0,0,1], "Ü": [0,0,1,1]}

# input converted to signal
signals: list[int] = [] 
for char in sentence:
    signals.extend(alph_signals[char])


# functions for short and long signel
def short_signal():
    led_green.value(1)
    sleep(0.1)
    led_green.value(0)
    sleep(0.2)

def long_signal():
    led_red.value(1)
    sleep(0.5)
    led_red.value(0)
    sleep(0.2) 

# output
# TODO in python version > 3.10 use match-case not elif
for signal in signals:
    if signal == 0:
        short_signal()
    elif signal == 1:
        long_signal()
    elif signal == 2:
        sleep(0.2)




