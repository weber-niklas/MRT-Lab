# 1. Get User input
# 1.1 Validate User Input (only chars not ints etc.)
# 1.2 convert input to lower/ upper case
# 2. Dictionary assigning signals -> letters
# 3. Convert input into signal
# 4. Output Signal
#Louis Test 1

from time import sleep
# 1
sentence: str = input("What would you like to translate to morsecode? \n")

# 1.1 
# TODO internet

# 1.2
sentence = sentence.upper()

# 2
# TODO input whole alphabet
# Later: Signals with enumerations
# OR: declare functions before and store them as values in list
alph_signals: dict = {"A": [0, 1], "B": [1, 0, 0, 0], " ": [2]}

# 3
signals: list[int] = []
for char in sentence:
    signals.extend(alph_signals[char])


# 4
# TODO define funcs so they actually turn on LEDs
def short_signal():
    print("Short")

def long_signal():
    print("Long") 

# TODO in python version > 3.10 use match-case not elif
for signal in signals:
    if signal == 0:
        short_signal()
    elif signal == 1:
        long_signal()
    elif signal == 2:
        sleep(0.2)



