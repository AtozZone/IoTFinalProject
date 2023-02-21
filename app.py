from dash import Dash, dcc, html, ctx, Output, Input
import dash_daq as daq
import RPi.GPIO as GPIO 
from time import sleep

GPIO.setwarnings(False) 
GPIO.setmode(GPIO.BCM)

app = Dash(__name__)

IN = 18
OUT = 17

GPIO.setup(IN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(OUT, GPIO.OUT, initial = GPIO.LOW)

while True:
    button_state = GPIO.input(IN)
    if button_state == 0:
        GPIO.output(OUT, GPIO.HIGH)
        print("ON")
    else:
        GPIO.output(OUT, GPIO.LOW)
        print("OFF")
        
if __name__ == "__main__":
 app.run_server(debug=True)