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
import time as time

#setup GPIO outputs
lightpin = 12
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(lightpin, GPIO.OUT)

DHTPin = 40 #define the pin of DHT11
dht = DHT.DHT(DHTPin) #create a DHT class object

def get_both():    
    #for i in range(0,15):
    #    chk = dht.readDHT11() #read DHT11 and get a return value. Then determine whether data read is normal according to the return value.
    #    if (chk is dht.DHTLIB_OK): #read DHT11 and get a return value. Then determine whether data read is normal according to the return value.
    #        print("DHT11,OK!")
    #        break
    #    time.sleep(0.1)
    chk = dht.readDHT11()
    humi = dht.humidity
    temp = dht.temperature
    humi = '{0:0.1f}'.format(humi)
    temp = '{0:0.1f}'.format(temp)
    print(humi)
    print(temp)
    #time.sleep(5)
    return temp, humi
    
#initialize app
app = Dash(__name__)
app.title = 'Phase 2'

#initialize image
led_img = html.Img(src=app.get_asset_url('off.png'),width='300px', height='300px')

#dashboard layout
app.layout = html.Div([
    html.H1(children='Control Panel'),
    html.H2(children='LED Dashboard'),
    html.Div(id='led-box', children=[
        html.H1(children=True, style={'text-align': 'center'}),
        html.Button(led_img, id='led-img', n_clicks = 0)
    ]),
    
    html.Div([
        html.H2("Humidity: "),
        html.Div(id='humidity_value')
    ]),
    
    html.Div([
        html.H2("Temperature: "),
        html.Div(id='temperature_value')
    ]),
    
    dcc.Interval(
        id='interval-component',
        interval=2*1000, # updates every 2 seconds
        n_intervals=0
    )
])

@app.callback(
    Output('humidity_value', 'children'),
    Output('temperature_value', 'children'),
    Input('interval-component', 'n_intervals')
)

def update_values(n):
    temp, humi = get_both()
    return f'Temperature: {temp} C', f'Humidity: {humi}%'

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
        GPIO.output(lightpin, GPIO.LOW)
        #returns updated img
        return html.Img(src=app.get_asset_url('off.png'),width='300px', height='300px')
    else:
        print(n_clicks % 2)
        #turns on light
        GPIO.output(lightpin, GPIO.HIGH)
        return html.Img(src=app.get_asset_url('on.png'),width='300px', height='300px')

#runs server
if __name__ == '__main__':
    print ('Program is starting ... ')
    app.run_server(debug=True) 