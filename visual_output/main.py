"""
Pico - Morse Code
    - web-parts inspired by code shown in lecture
"""

from time import sleep, time
from machine import Pin
import network
import socket
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
<head>
<style>
#parent{
display: flex;
justify-content: center;
align-items: center;
}
body {
  min-height: 100vh;
  padding: 0;
}
</style>
</head>
<body id="parent">
<h2>MorseCode - Input</h2>
<form>
  <label> Service currently %s</label><br> 
  <label>Was last text valid Input? %s</label><br>
  <label>Last entered text: %s</label><br>
  <label>Enter text:</label><br>
  <input type="text" id="input" name="input" value=" "><br>
  <input type="submit" value="Submit">
</form>
</body>
</html>
"""


executing = False

def main():
    # init UI-vars
    lastText = ""
    lastValid = False

    while True:

        conn, addr = sock.accept()
        print("Connected to: " + str(addr))

            
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
                lastValid = checkString(check_tempText)

                if lastValid:
                    lastText = tempText.replace("+", " ")
                    lastText = lastText.upper()
                else:
                    lastText = ""

            # formatting website
            if executing:
                html = WEBSITE % (f"<font color=\"green\"><b>available</b></font>", str(lastValid), lastText)
            else:
                html = WEBSITE % (f"<font color=\"firebrick\"><b>unavailable</b></font>", str(lastValid), lastText)

            conn.send(
                "HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n"
            )  # HTTP status line and header
            conn.send(html)
            conn.close()
            
            # the LAST VALID text is morsed
            if lastValid and executing:
                morseOutput(lastText)                
                

        except OSError:
            conn.close()
            print("Error occured")

last_interrupt = time()
def handle_interrupt(pin):
    global last_interrupt
    current_time = time()
    print(f"Difference: {current_time-last_interrupt}")
    if current_time-last_interrupt >= 2:
        last_interrupt = current_time
        print(f"last_interrupt: {last_interrupt}")

        global executing
        executing = not executing
        print(f"Executing: {executing}")

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
print(sock)

if __name__ == "__main__":
    button.irq(trigger=Pin.IRQ_RISING, handler=handle_interrupt)

    main()