"""
Pico - Morse Code
    wireless solution
    - web-parts inspired by code shown in lecture
"""

from time import sleep, time
from machine import Pin
import network
import socket


# output: looping over string, looping over output-function-array
def morse_output(word):
    for char in word:
        for signal in letters[char]:
            signal()


# check if string is only consisting of letters or spaces
def check_string(user_input: str):
    user_input=user_input.replace("+","")
    if user_input.isalpha() or len(user_input) == 0:
        return True
    else:
        return False


# LED functions for output
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
    " ": [wait],
}

# constants for web interface
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
<div id="center">
<h2>MorseCode Converter</h2>
<form>
  <center>
  <label> Service currently %s</label><br> 
  <label>Was last input valid? %s</label><br>
  <label>Last entered text: %s</label><br>
  <br/>
  <label>Enter text:</label><br>
  <input type="text" id="input" name="input" value=" "><br>
  <input type="submit" value="Submit">
  </center>
</form>
</div>
</body>
</html>
"""

# init global variable for execution state (set by hardware button)
executing = False

# creating website, asking for user input
def main():
    # colors change if input was not valid
    input_valid_display = {
        True: '<font color="#44CA3B"> Yes </font>',
        False: '<font color="#EE441A"> No </font>',
    }
    # init UI-vars
    last_user_input = ""
    morse_input = ""
    last_input_valid = False

    # main loop - waiting for connection, checking input, output
    while True:

        conn, addr = sock.accept()

        try:
            request = conn.recv(1024)
            req_text = str(request)

            # if input is submitted (else the find returns -1)
            if req_text.find("/?input=") + 1:

                # extract the input from recieved
                last_user_input = req_text[
                    (req_text.find("/?input=") + 9) : (req_text.find(" HTTP/1.1"))
                ]

                last_input_valid = check_string(last_user_input)
                
                # only output when input was valid
                if last_input_valid:
                    last_user_input = last_user_input.replace("+", " ")
                    morse_input = last_user_input.upper()
                else:
                    last_user_input = ""

            # formatting website (changing colors dependend on hardware button press)
            if executing:
                html = WEBSITE % (
                    f'<font color="green"><b>available</b></font>',
                    input_valid_display[last_input_valid],
                    last_user_input,
                )
            else:
                html = WEBSITE % (
                    f'<font color="firebrick"><b>unavailable</b></font>',
                    input_valid_display[last_input_valid],
                    last_user_input,
                )
            # HTTP status line and header
            conn.send(
                "HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n"
            )  
            conn.send(html)
            conn.close()

            # outputting morse signal
            if executing and last_input_valid:
                morse_output(morse_input)

        except OSError:
            conn.close()
            print("Error occured")

#save time stamp of last interrupt (button is oszillating)
last_interrupt = time()


def handle_interrupt(pin):
    global last_interrupt
    current_time = time()
    #checking for minimum time difference (prevent double clicks, oszillating)
    if current_time - last_interrupt >= 2:
        last_interrupt = current_time
        global executing
        #inverting executing
        executing = not executing

# interface object creation
wap = network.WLAN(network.AP_IF)
wap.config(essid=SSID, password=PASS)
wap.active(True)

#saving ip for socket
ip = wap.ifconfig()[0]

# give user IP and PORT (to enter in Browser and access UI)
print("IP-Address: " + str(ip))
print("Port: " + str(PORT))

# init Socket
sock = socket.socket()
sock.bind((ip, PORT))
sock.listen()

#setting up interrupt
button.irq(trigger=Pin.IRQ_RISING, handler=handle_interrupt)

#starting to wait for input
main()
