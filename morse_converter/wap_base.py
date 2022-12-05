#This Program is intended to run on RaspberryPi Pico W. It logs in into existing wireless Networks and provides Web Inerface to toggle LED and watch current Temperature.

import network, socket
import machine as pi

DAC = 3.3/(65535) #Convert Digtial input from ADC back to analog Voltage

led = pi.Pin("LED", pi.Pin.OUT)
state_led = False

SSID = 'HenningsPicoPi'
PASS = 'PicoPi123'
PORT = 80
WEBSITE = """<!DOCTYPE html>
<html>
  <head>
    <title>Pico Pi - Controller</title>
    <style>
      h1 {
        text-align: center;
        font-size: 28px;
      }
      fieldset {
        width: 340px;
        margin: 0 auto;
      }
      label {
        width: 190px;
        display: inline-block;
      }
      input[type="text"] {
        width: 120px;
      }
      input[type="text"],
      label {
        font-size: 20px;
      }
      legend {
        font-size: 26px;
      }
    </style>
  </head>
  <body>
    <h1>Hennings' Pico Pi - Control Center</h1>
    <fieldset>
      <legend>Temperatur</legend>
      <label for="temperaturText">Onboard-ADC:&nbsp;</label
      ><input
        type="text"
        value="%s &#8451;"
        id="temperaturText"
        disabled="disabled"
      /><br />
    </fieldset>
    <fieldset>
      <legend>LED-Control</legend>
      <label for="ledText">Toggle:&nbsp;</label
      ><input
        type="button"
        value="toggle"
        onclick='toggleLed("led")'
        id="ledText"
      />
      <script>
        function toggleLed(led) {
          var xhttp = new XMLHttpRequest();
          xhttp.open("GET", "/led/" + led, true);
          xhttp.send();
        }
      </script>
      <br />
    </fieldset>
  </body>
</html>"""

adc = pi.ADC(4) 

wap = network.WLAN(network.AP_IF) #wireless interface object as access point
wap.config(essid=SSID, password=PASS)
wap.active(True)
ip=wap.ifconfig()[0]
print("IP-Address: " + str(ip))
print("Port: " + str(PORT))

sock = socket.socket()
sock.bind((ip, PORT))
sock.listen()


while True:
    try:
        conn, addr = sock.accept()
        print("Connected to: " + str(addr))
    except socket.error:
        print('Socket error, exiting.')
        break
    try:
        d_voltage=adc.read_u16()
        a_voltage=d_voltage * DAC
        temp = 27 - (a_voltage -0.706) / 0.001721
        
        request = conn.recv(1024)
        request = str(request)
        
        req_state_led = request.find('/led/led') == 6
        if req_state_led and state_led:
            state_led = False
            led.value(0)
        elif not req_state_led and state_led:
            state_led = True
            led.value(1)
        elif req_state_led and not state_led:
            state_led = True
            led.value(1)
        
        html = WEBSITE % (temp)

        conn.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n') #HTTP status line and header
        conn.send(html)
        conn.close()

    except OSError:
        conn.close()
        print('Error occured')