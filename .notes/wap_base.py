#This Program is intended to run on RaspberryPi Pico W. It logs in into existing wireless Networks and provides Web Inerface to toggle LED and watch current Temperature.

import network, socket

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
wap = network.WLAN(network.AP_IF) #wireless interface object as access point
wap.config(essid=SSID, password=PASS)
wap.active(True)
ip=wap.ifconfig()[0]
print("IP-Address: " + str(ip))
print("Port: " + str(PORT))

sock = socket.socket()
sock.bind((ip, PORT))
sock.listen()

lastText="None"
lastValid=False
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
        if (reqText.find("/?input=")+1):
          lastText = reqText[(reqText.find("/?input=")+9):(reqText.find(" HTTP/1.1"))]
        
        html = WEBSITE % (str(lastValid), lastText)

        conn.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n') #HTTP status line and header
        conn.send(html)
        conn.close()
    except OSError:
        conn.close()
        print('Error occured')