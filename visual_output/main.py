"""
Pico - Morse Code
    - web-parts inspired by code shown in lecture
"""

from time import sleep
from machine import Pin
import network, socket

#morse function
def morseOutput(word):
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

#check validity of string
def checkString(word):
    while condition == True:
        if(word.isalpha()):
            return True
        else:
            return False

#LED functions
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

#init LED
led_red = Pin(14, Pin.OUT)
led_green = Pin(15, Pin.OUT)
condition = True

#init Dict
letters: dict =    {"A": [0,1], "B": [1,0,0,0], "C": [1,0,1,0], "D": [1,0,0], "E": [0], "F": [0,0,1,0], "G": [1,1,0],
                    "H": [0,0,0,0], "I": [0,0], "J": [0,1,1,1], "K": [1,0,1], "L": [0,1,0,0], "M": [1,1], "N": [1,0],
                    "O": [1,1,1], "P": [0,1,1,0], "Q": [1,1,0,1], "R": [0,1,0], "S": [0,0,0], "T": [1], "U": [0,0,1],
                    "V": [0,0,0,1], "W": [0,1,1], "X": [1,0,0,1], "Y": [1,0,1,1], "Z": [1,1,0,0], " ": [2],
                    "Ä": [0,1,0,1], "Ö": [0,0,0,1], "Ü": [0,0,1,1]}

#constants for web - interface
SSID = 'WAP-Morsecode'
PASS = 'PicoPi123'
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

#configure WAP
wap = network.WLAN(network.AP_IF) 
wap.config(essid=SSID, password=PASS)
wap.active(True)

ip=wap.ifconfig()[0]

#give user IP and PORT (to enter in Browser and access UI)
print("IP-Address: " + str(ip))
print("Port: " + str(PORT))

#init Socket
sock = socket.socket()
sock.bind((ip, PORT))
sock.listen()

#init UI-vars
lastText="NONE"
lastValid=False

#init Pins
while True:
    try:
        conn, addr = sock.accept()
        print("Connected to: " + str(addr))
    except socket.error:
        print('Socket error, exiting.')
        break
    try:
        request = conn.recv(1024)
        reqText = str(request)
        #if input is submitted (else the find returns -1)
        if (reqText.find("/?input=")+1):
            #extract the input from recieved
            tempText = reqText[(reqText.find("/?input=")+9):(reqText.find(" HTTP/1.1"))]
            #a bit of manipulation (no spaces... implemented)
            lastValid=checkString(tempText)
            if lastValid:
                lastText=tempText.upper()
                lastText = lastText.replace(" ","")
        #formatting website
        html = WEBSITE % (str(lastValid), lastText)

        conn.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n') #HTTP status line and header
        conn.send(html)
        conn.close()
        #the LAST VALID text is morsed 
        morseOutput(lastText)
    except OSError:
        conn.close()
        print('Error occured')                                              

