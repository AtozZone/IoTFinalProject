#cmd installations
#pip install pydash
#pip install dash_daq
#sudo apt-get remove thonny
#sudo apt-get install thonny
#pip dash-bootstrap-components

import dash.dependencies
import dash_daq as daq
from dash import html, Input, Output, dcc, Dash, ctx
import dash_bootstrap_components as dbc
import RPi.GPIO as GPIO

#setup GPIO outputs
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(18, GPIO.OUT)

#create dashboard
app = Dash(__name__)

#initialize image
led_img = html.Img(src=app.get_asset_url('off.png'),width='300px', height='300px')

#dashboard layout
app.layout = html.Div(children=[
    html.H1(children='Phase 1 - Dashboard'),
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

#runs server
if __name__ == '__main__':
    app.run_server(debug=True)
