"""
Pico - Morse Code
"""

from time import sleep
from machine import Pin

global executing
executing=False

# morse function
def morseOutput(word):
    for char in word:
        for signal in letters[char]:
            signal()


# check validity of string
def validInput():
    while True:
        word=input("What do you want to send?").replace(" ","").upper()
        if word.isalpha():
            return word
        else:
            print("Input not valid.")
            lightError()


# LED functions
def short():  # 0 --> short;
    led_green.value(1)
    sleep(0.1)
    led_green.value(0)
    sleep(0.2)


def long():  # 1-->long
    led_red.value(1)
    sleep(0.5)
    led_red.value(0)
    sleep(0.2)

def wait():
    sleep(1)

def lightError():
    led_red.value(1)
    sleep(3)
    led_red.value(0)

def handle_interrupt(pin):
    global executing  
    executing = not executing

# init LED
led_red = Pin(14, Pin.OUT)
led_green = Pin(15, Pin.OUT)
button = Pin(16, Pin.IN)
button.irq(trigger=Pin.IRQ_RISING, handler=handle_interrupt)

# init Dict
letters: dict = {
    "A": [short, long],
    "B": [long, short, short, short],
    "C": [long, short, long, short],
    "D": [long, short, short],
    "E": [short],
    "F": [short, short, long, short],
    "G": [long, long, short],
    "H": [short, short, short, short],
    "I": [short, short],
    "J": [short, long, long, long],
    "K": [long, short, long],
    "L": [short, long, short, short],
    "M": [long, long],
    "N": [long, short],
    "O": [long, long, long],
    "P": [short, long, long, short],
    "Q": [long, long, short, long],
    "R": [short, long, short],
    "S": [short, short, short],
    "T": [long],
    "U": [short, short, long],
    "V": [short, short, short, long],
    "W": [short, long, long],
    "X": [long, short, short, long],
    "Y": [long, short, long, long],
    "Z": [long, long, short, short],
    "Ä": [short, long, short, long],
    "Ö": [short, short, short, long],
    "Ü": [short, short, long, long],
    " ": [wait],
}
    
def main():
    # init UI-vars
    while True:
        if executing:
            sleep(3)
        else:
            validText = validInput()
            morseOutput(validText)
        
main()