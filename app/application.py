#pytorch
#cmd installations
#pip install pydash
#pip install dash_daq
#sudo apt-get remove thonny
#sudo apt-get install thonny
#pip install dash-bootstrap-components

import dash.dependencies
import dash_daq as daq
from dash import html, Input, Output, dcc, Dash, ctx
import dash_bootstrap_components as dbc
import RPi.GPIO as GPIO
import Freenove_DHT as DHT

#setup GPIO outputs
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(18, GPIO.OUT)

#initialize app
app = Dash(__name__)
app.title = 'Phase 2'
#initialize image
led_img = html.Img(src=app.get_asset_url('off.png'),width='300px', height='300px')

#dashboard layout
app.layout = html.Div(children=[
    html.H1(children='Phase 2'),
    html.H2(children='LED Dashboard'),
    html.Div(id='led-box', children=[
        html.H1(children=True, style={'text-align': 'center'}),
        html.Button(led_img, id='led-img', n_clicks = 0)
    ]),
])

#callback method to write the event behaviour
@app.callback(
    Output('led-img', 'children'),
    Input('led-img', 'n_clicks')
)

#function to control the button on the dashboard 
def control_output(n_clicks):
    #check if n_clicks is 1 or 0 
    if n_clicks % 2 == 1:
        print(n_clicks % 2)
        #turns off light
        GPIO.output(18, GPIO.LOW)
        #returns updated img
        return html.Img(src=app.get_asset_url('off.png'),width='300px', height='300px')
    else:
        print(n_clicks % 2)
        #turns on light
        GPIO.output(18, GPIO.HIGH)
        return html.Img(src=app.get_asset_url('on.png'),width='300px', height='300px')


DHTPin = 13 #define the pin of DHT11
def loop():
    dht = DHT.DHT(DHTPin) #create a DHT class object
    counts = 0 # Measurement counts
    while(True):
        counts += 1
        print("Measurement counts: ", counts)
        for i in range(0,15):
            chk = dht.readDHT11() #read DHT11 and get a return value. Then determine whether data read is normal according to the return value.
            if (chk is dht.DHTLIB_OK): #read DHT11 and get a return value. Then determine whether data read is normal according to the return value.
                print("DHT11,OK!")
                break
            time.sleep(0.1)
            print("Humidity : %.2f, \t Temperature : %.2f \n"%(dht.humidity,dht.temperature))
            time.sleep(2) 

#runs server
if __name__ == '__main__':
    app.run_server(debug=True)
    print ('Program is starting ... ') 
    try:
        loop()
    except KeyboardInterrupt:
        GPIO.cleanup()
        exit() 
