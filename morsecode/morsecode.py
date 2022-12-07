
from time import sleep
from machine import Pin
                                                
led_red = Pin(14, Pin.OUT)
led_green = Pin(15, Pin.OUT)
condition = True

letters: dict =    {"A": [0,1], "B": [1,0,0,0], "C": [1,0,1,0], "D": [1,0,0], "E": [0], "F": [0,0,1,0], "G": [1,1,0],
                    "H": [0,0,0,0], "I": [0,0], "J": [0,1,1,1], "K": [1,0,1], "L": [0,1,0,0], "M": [1,1], "N": [1,0],
                    "O": [1,1,1], "P": [0,1,1,0], "Q": [1,1,0,1], "R": [0,1,0], "S": [0,0,0], "T": [1], "U": [0,0,1],
                    "V": [0,0,0,1], "W": [0,1,1], "X": [1,0,0,1], "Y": [1,0,1,1], "Z": [1,1,0,0], " ": [2],
                    "Ä": [0,1,0,1], "Ö": [0,0,0,1], "Ü": [0,0,1,1]}


word = input("What would you like to send? \n")
word = word.upper()


def checkString(Str):
    
    while condition == True:
        global word

        check_string = word.replace(" ","")
        print(check_string)

        if(check_string.isalpha()):
            print("Valid input.")
            break
        else:
            print("Error occured. False input. Try again.")
            word=input("What would you like to send? \n")
            word = word.upper()

def greenLightOn():       # 0 --> short;
    print("Green on!")
    led_green.value(1)
    sleep(0.1)
    led_green.value(0)
    sleep(0.2)

def redLightOn():         # 1-->long
    print("Red on!")
    led_red.value(1)
    sleep(0.5)
    led_red.value(0)
    sleep(0.2)



checkString(word) 

for char in word:
    print(letters[char])

    for signal in letters[char]:
        print(signal)

        if signal == 0:
            greenLightOn()
        elif signal == 1:
            redLightOn()
        elif signal == 2:
            sleep(1)

