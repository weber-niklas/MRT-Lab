"""
Pico - Morse Code
    - web-parts inspired by code shown in lecture
"""

from time import sleep
from machine import Pin
import network, socket
import sys

# morse function
def morseOutput(word):
    for char in word:
        for signal in letters[char]:
            signal()


# check validity of string
def checkString(word: str):
    if word.isalpha():
        return True
    else:
        return False


# LED functions
def short():  # 0 --> short;
    print("Green on!")
    led_green.value(1)
    sleep(0.1)
    led_green.value(0)
    sleep(0.2)


def long():  # 1-->long
    print("Red on!")
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


# init LED
led_red = Pin(14, Pin.OUT)
led_green = Pin(15, Pin.OUT)
button = Pin(16, Pin.IN)



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

# constants for web - interface
SSID = "WAP-Morsecode"
PASS = "PicoPi123"
PORT = 80
WEBSITE = """<!DOCTYPE html>
<html>
<body>
<h2>MorseCode - Input</h2>
<form>
  <label>Was last text valid Input? %s</label><br>
  <label>Last entered text: %s</label><br>
  <label>Enter text:</label><br>
  <input type="text" id="input" name="input" value=" "><br>
  <input type="submit" value="Submit">
</form> 
</body>
</html>
"""


def main():
    # configure WAP
    wap = network.WLAN(network.AP_IF)
    wap.config(essid=SSID, password=PASS)
    wap.active(True)

    ip = wap.ifconfig()[0]

    # give user IP and PORT (to enter in Browser and access UI)
    print("IP-Address: " + str(ip))
    print("Port: " + str(PORT))

    # init Socket
    sock = socket.socket()
    sock.bind((ip, PORT))
    sock.listen()

    # init UI-vars
    lastText = ""
    lastValid = False
    while True:
        try:
            conn, addr = sock.accept()
            print("Connected to: " + str(addr))
        except socket.error:
            print("Socket error, exiting.")
            break
        try:
            request = conn.recv(1024)
            reqText = str(request)

            # if input is submitted (else the find returns -1)
            if reqText.find("/?input=") + 1:

                # extract the input from recieved
                tempText = reqText[
                    (reqText.find("/?input=") + 9) : (reqText.find(" HTTP/1.1"))
                ]

                # a bit of manipulation (no spaces... implemented)
                check_tempText = tempText.replace("+", "")
                print(check_tempText)
                lastValid = checkString(check_tempText)
                print(lastValid)

                if lastValid:
                    lastText = lastText.replace("+", " ")
                    lastText = tempText.upper()
                else:
                    lastText = ""

            # formatting website
            html = WEBSITE % (str(lastValid), lastText)

            conn.send(
                "HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n"
            )  # HTTP status line and header
            conn.send(html)
            conn.close()
            
            # the LAST VALID text is morsed
            if lastValid:
                morseOutput(lastText)
            else:
                lightError()

        except OSError:
            conn.close()
            print("Error occured")

executing = False

def handle_interrupt(pin):
    global executing
    executing = not executing

    if executing:
        main()

button.irq(trigger=Pin.IRQ_RISING, handler=handle_interrupt)