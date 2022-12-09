'''
The following code runs on the wap-pico.
Functionality:  - provide web-ui
                - wap-functionality
                - broadcasts morsecode
Inspiration: Code shown in Lecture 4
'''
import network, socket
import machine

SSID = 'morsecode'
PASS = 'PicoPi123'
PORT = 80
WEBSITE = """<!DOCTYPE html>
<html>
  <head>
    <title>Morsecode - input panel</title>
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
    <h1>Morsecode - input panel</h1>
    <fieldset>
      <legend>Temperatur</legend>
      <label for="temperaturText">Onboard-ADC:&nbsp;</label
      ><input
        type="text"
        value="%s &#8451;"
        id="temperaturText"
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

