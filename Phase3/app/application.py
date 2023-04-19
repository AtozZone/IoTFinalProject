#pytorch
#cmd installations
#pip install pydash
#pip install dash_daq
#sudo apt-get remove thonny
#sudo apt-get install thonny
#pip install dash-bootstrap-components
#pip install dash_mqtt
#pip install paho-mqtt

import dash.dependencies
import dash_daq as daq
from dash import html, Input, Output, dcc, Dash, State
import dash_bootstrap_components as dbc
import RPi.GPIO as GPIO
import Freenove_DHT as DHT
import time as time
import smtplib
import email
import imaplib
import dash_mqtt
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

is_sent = True

Motor1 = 15 # Enable Pin | 22 board
Motor2 = 13 # Input Pin  | 27 board
Motor3 = 11 # Input Pin  | 17 board
#setup GPIO outputs
lightpin = 12
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(lightpin, GPIO.OUT)
lightsensor = 0
LEDStatus = False
hasLEDEmailSent = False
humi = 0
temp = 0
RFID = ""

DHTPin = 40 #define the pin of DHT11
dht = DHT.DHT(DHTPin) #create a DHT class object

# def get_both(): 
#     global is_sent   
#     #for i in range(0,15):
#     #    chk = dht.readDHT11() #read DHT11 and get a return value. Then determine whether data read is normal according to the return value.
#     #    if (chk is dht.DHTLIB_OK): #read DHT11 and get a return value. Then determine whether data read is normal according to the return value.
#     #        print("DHT11,OK!")
#     #        break
#     #    time.sleep(0.1)
#     chk = dht.readDHT11()
#     humi = dht.humidity
#     temp = dht.temperature
#     if (temp >= 24 and is_sent):
#         send_email(temp)   
#         is_sent = False
#     receive_reply()
#     humi = '{0:0.1f}'.format(humi)
#     temp = '{0:0.1f}'.format(temp)
#     print(humi)
#     print(temp)
#     #time.sleep(5)
#     return temp, humi

def motor_on():
    global Motor1 # Enable Pin | 22 board
    global Motor2 # Input Pin  | 27 board
    global Motor3 # Input Pin  | 17 board
    GPIO.setup(Motor1,GPIO.OUT)
    GPIO.setup(Motor2,GPIO.OUT)
    GPIO.setup(Motor3,GPIO.OUT)

    GPIO.output(Motor1,GPIO.HIGH)
    GPIO.output(Motor2,GPIO.LOW)
    GPIO.output(Motor3,GPIO.HIGH)
    
def send_email(temp):
    
    # Set up the email addresses and password
    my_address = "iotburner28@gmail.com" # Replace with your own Gmail address
    my_password = "uefa acwp roct hnuc" # Replace with your Gmail password
    recipient_address = "ilikefortniteseason4@gmail.com" # Replace with the recipient's email address

    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = my_address
    msg['To'] = recipient_address
    msg['Subject'] = "IoT Fan"

    # Add the body to the email
    body = "The current temperature is " + str(temp) + ". Would you like to turn on the fan?"
    msg.attach(MIMEText(body, 'plain'))
     
    # Log in to the Gmail SMTP server
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(my_address, my_password)

    # Send the email
    text = msg.as_string()
    server.sendmail(my_address, recipient_address, text)

    # Log out of the server
    print('sent to ' + recipient_address)
    server.quit()

def receive_reply():
    EMAIL = "iotburner28@gmail.com" # Replace with your own Gmail address
    PASSWORD = "uefa acwp roct hnuc" # Replace with your Gmail password
    SERVER = "imap.gmail.com"

    # connect to the server and go to its inbox
    mail = imaplib.IMAP4_SSL(SERVER)
    mail.login(EMAIL, PASSWORD)

    mail.select('inbox')
    status, data = mail.search(None, 'ALL')
    mail_ids = []

    for block in data:
        mail_ids += block.split()

    for i in mail_ids:
        status, data = mail.fetch(i, '(RFC822)')

        for response_part in data:
            if isinstance(response_part, tuple):
                message = email.message_from_bytes(response_part[1])

                mail_from = message['from']
                mail_subject = message['subject']

                if message.is_multipart():
                    mail_content = ''

                    for part in message.get_payload():
                        if part.get_content_type() == 'text/plain':
                            mail_content += part.get_payload()
                else:
                    mail_content = message.get_payload()

                if mail_content == 'yes' or 'yes' in mail_subject.lower() or any('yes' in recipient.lower() for recipient in message.get_all('to', [])) or 'yes' in mail_content.lower():
                    print(f'From: {mail_from}')
                    print(f'Subject: {mail_subject}')
                    print(f'Content: {mail_content}')
                    #can start motor
                    motor_on()
                    
def on_message(client, userdata, msg):
    global hasLEDEmailSent
    global is_sent
    global lightsensor
    global LEDStatus
    global temp
    global humi
    global RFID
    
    date = time.strftime('%d/%m/%Y %H:%M:%S')
    print(msg.payload.decode("utf-8")) 
    
    if('photoValue' in msg.topic):
        lightsensor = float(msg.payload.decode("utf-8"))
        print(lightsensor + float(0))
        
        if (lightsensor <= 650) and (hasLEDEmailSent is False):
            current_time = datetime.now().strftime("%H:%M")
            light_email(current_time)
            hasLEDEmailSent = True
            LEDStatus = True
            time.sleep(3)
            print(LEDStatus)
        else:
            LEDStatus = False
            print(LEDStatus)
            
    if ('temperature' in msg.topic):
        temp = float(msg.payload.decode("utf-8"))
        if (temp >= 24 and is_sent):
            send_email(temp)
            is_sent = False
        receive_reply()
        
    if ('humidity' in msg.topic):
        humi = float(msg.payload.decode("utf-8"))
    if ('rfid' in msg.topic):
        RFID = msg.payload.decode("utf-8")
        print(RFID)

def light_email(current_time):
# Set up the email addresses and password
    my_address = "iotburner28@gmail.com" # Replace with your own Gmail address
    my_password = "uefa acwp roct hnuc" # Replace with your Gmail password
    recipient_address = "ilikefortniteseason4@gmail.com" # Replace with the recipient's email address
    print("method was called")
    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = my_address
    msg['To'] = recipient_address
    msg['Subject'] = "IoT Lightsensor"

    # Add the body to the email
    body = f"The Light is ON at {current_time}."
    msg.attach(MIMEText(body, 'plain'))

    # Log in to the Gmail SMTP server
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(my_address, my_password)

    # Send the email
    text = msg.as_string()
    server.sendmail(my_address, recipient_address, text)

    # Log out of the server
    print('sent to ' + recipient_address)
    server.quit()
    
    # Publish a message to a topic that the dashboard is subscribed to
    publish.single("dashboard/message", "Email has been sent", hostname="localhost")
            
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    #client.subscribe("IoTlab/photoValue")
    client.subscribe("vanieriot/photoValue")
    client.subscribe("vanieriot/temperature")
    client.subscribe("vanieriot/humidity")
    client.subscribe("vanieriot/rfid")

#initialize app
app = Dash(__name__)

on_image = app.get_asset_url('on.png')
off_image = app.get_asset_url('off.png')
initial_image = on_image if LEDStatus else off_image

@app.callback(
    Output('light-image', 'src'),
    Input('interval-component', 'n_intervals'),
    State('light-image', 'src'))

def update_image(n, src):
    # Update LED image
    new_image = on_image if LEDStatus else off_image
    if new_image != src:
        return new_image
    else:
        return dash.no_update

app.title = 'Phase 3'
#dashboard layout
app.layout = html.Div([
    html.H1(children='Control Panel', style={'text-align': 'center', 'font-size': '300%'}),

    html.Div(
    [
        dcc.Graph(
            id="temp-gauge",
            figure={
                "data": [
                    {
                        "type": "indicator",
                        "value": temp,
                        "mode": "gauge+number",
                        "title": {"text": "Temperature"},
                        "gauge": {
                            "axis": {"range": [None, 50]},
                            "bar": {"color": "#f44336"},
                            "threshold": {
                                "line": {"color": "black", "width": 4},
                                "thickness": 0.75,
                                "value": 35,
                            },
                            "steps": [
                                {"range": [0, 10], "color": "rgb(242, 242, 242)"},
                                {"range": [10, 20], "color": "rgb(217, 217, 217)"},
                                {"range": [20, 30], "color": "rgb(191, 191, 191)"},
                                {"range": [30, 40], "color": "rgb(166, 166, 166)"},
                                {"range": [40, 50], "color": "rgb(140, 140, 140)"},
                            ],
                            "borderwidth": 2,
                            "bordercolor": "#b0bec5",
                            "height": 100,  # Set the height of the gauge to 150 pixels
                            "width": 100,  # Set the width of the gauge to 150 pixels
                        },
                    }
                ]
            },
            style={"width": "30%", "display": "inline-block"},
        ),
        
       dcc.Graph(
        id="humi-gauge",
        figure={
            "data": [
                {
                    "type": "indicator",
                    "value": humi,
                    "mode": "gauge+number",
                    "title": {"text": "Humidity"},
                    "gauge": {
                        "axis": {"range": [None, 100]},
                        "bar": {"color": "#2196f3"},
                        "threshold": {
                            "line": {"color": "black", "width": 4},
                            "thickness": 0.75,
                            "value": 70,
                        },
                        "steps": [
                            {"range": [0, 20], "color": "#e1f5fe"},
                            {"range": [20, 40], "color": "#b3e5fc"},
                            {"range": [40, 60], "color": "#81d4fa"},
                            {"range": [60, 80], "color": "#4fc3f7"},
                            {"range": [80, 100], "color": "#29b6f6"},
                        ],
                        "borderwidth": 2,
                        "bordercolor": "#b0bec5",
                        "bgcolor": "rgba(0,0,0,0)",
                    },
                }
            ]
        },
        style={"width": "30%", "display": "inline-block"},
    ),
        
      dcc.Graph(
        id="light-gauge",
        figure={
            "data": [
                {
                    "type": "indicator",
                    "value": lightsensor,
                    "mode": "gauge+number",
                    "title": {"text": "Light Intensity"},
                    "gauge": {
                        "axis": {"range": [None, 1000]},
                        "bar": {"color": "yellow"},  # change bar color to yellow
                        "threshold": {
                            "line": {"color": "black", "width": 4},
                            "thickness": 0.75,
                            "value": 35,
                        },
                        "steps": [
                            {"range": [0, 200], "color": "#fff9c4"},  # change step color to pale yellow
                            {"range": [200, 400], "color": "#fff59d"},
                            {"range": [400, 600], "color": "#fff176"},
                            {"range": [600, 800], "color": "#ffee58"},
                            {"range": [800, 1000], "color": "#ffeb3b"},
                        ],
                        "borderwidth": 2,
                        "bordercolor": "#b0bec5",
                },
            }
        ]
    },
    style={"width": "30%", "display": "inline-block"},
)
        
    ],
    style={"text-align": "center"},
),
  html.Div(
   style={'text-align': 'center'},
    children=[
        html.Div([
            html.H1("Email Status"),
            html.Div(
                id="email-status",
                children="Email not yet sent",
                style={'font-size': '24px'}  # add font size style
            )
        ], style={'display': 'inline-block'}),
        
        html.Div([
            html.H1("Light Status"),
            html.Img(id='light-image', src=initial_image, height=200, width=200),
        ], style={'display': 'inline-block'}),

        html.Div([
            html.H1("Fan Status"),
            html.Img(id='fan-image', src=app.get_asset_url("fan.png"), height=200, width=200),
        ], style={'display': 'inline-block'}),
    ]
),
    dcc.Interval(
        id='interval-component',
        interval=2 * 1000,  # updates every 2 seconds
        n_intervals=0
    )
], style={'font-size': '15px'})

# create a callback function that updates the email status text
@app.callback(
    Output("email-status", "children"),
    [Input("interval-component", "n_intervals")],
)
def update_email_status(n):
    global hasLEDEmailSent
    
    if hasLEDEmailSent:
        return "Email has been sent"
    else:
        return "Email not yet sent"

# create an interval component that updates every 5 seconds
@app.callback(Output("interval-component", "interval"), [Input("interval-component", "n_intervals")])
def update_interval(n):
    return 5 * 1000

# create a function that updates hasLEDEmailSent
def update_email_sent_status():
    global hasLEDEmailSent
    
    # do some check to update hasLEDEmailSent
    hasLEDEmailSent = True


@app.callback(
    Output("temp-gauge", "figure"),
    Output("humi-gauge", "figure"),
    Output("light-gauge", "figure"),
    Input('interval-component', 'n_intervals')
)
def update_gauges(n):
    global temp, humi, lightsensor
    
    temp_fig = {
        "data": [
            {
                "type": "indicator",
                "value": temp,
                "mode": "gauge+number",
                "title": {"text": "Temperature"},
                "gauge": {
                    "axis": {"range": [None, 50]},
                    "bar": {"color": "#f44336"},
                    "threshold": {
                        "line": {"color": "black", "width": 4},
                        "thickness": 0.75,
                        "value": 35,
                    },
                    "steps": [
                        {"range": [0, 10], "color": "rgb(242, 242, 242)"},
                        {"range": [10, 20], "color": "rgb(217, 217, 217)"},
                        {"range": [20, 30], "color": "rgb(191, 191, 191)"},
                        {"range": [30, 40], "color": "rgb(166, 166, 166)"},
                        {"range": [40, 50], "color": "rgb(140, 140, 140)"},
                    ],
                    "borderwidth": 2,
                    "bordercolor": "#b0bec5",
                    "height": 100,  # Set the height of the gauge to 150 pixels
                    "width": 100,  # Set the width of the gauge to 150 pixels
                },
            }
        ]
    }
    
    humi_fig = {
        "data": [
                {
                    "type": "indicator",
                    "value": humi,
                    "mode": "gauge+number",
                    "title": {"text": "Humidity"},
                    "gauge": {
                        "axis": {"range": [None, 100]},
                        "bar": {"color": "#2196f3"},
                        "threshold": {
                            "line": {"color": "black", "width": 4},
                            "thickness": 0.75,
                            "value": 70,
                        },
                        "steps": [
                            {"range": [0, 20], "color": "#e1f5fe"},
                            {"range": [20, 40], "color": "#b3e5fc"},
                            {"range": [40, 60], "color": "#81d4fa"},
                            {"range": [60, 80], "color": "#4fc3f7"},
                            {"range": [80, 100], "color": "#29b6f6"},
                        ],
                        "borderwidth": 2,
                        "bordercolor": "#b0bec5",
                        "bgcolor": "rgba(0,0,0,0)",
                },
            }
        ]
    }
    
    light_fig = {
        "data": [
                {
                    "type": "indicator",
                    "value": lightsensor,
                    "mode": "gauge+number",
                    "title": {"text": "Light Intensity"},
                    "gauge": {
                        "axis": {"range": [None, 1000]},
                        "bar": {"color": "yellow"},  # change bar color to yellow
                        "threshold": {
                            "line": {"color": "black", "width": 4},
                            "thickness": 0.75,
                            "value": 35,
                        },
                        "steps": [
                            {"range": [0, 200], "color": "#fff9c4"},  # change step color to pale yellow
                            {"range": [200, 400], "color": "#fff59d"},
                            {"range": [400, 600], "color": "#fff176"},
                            {"range": [600, 800], "color": "#ffee58"},
                            {"range": [800, 1000], "color": "#ffeb3b"},
                        ],
                        "borderwidth": 2,
                        "bordercolor": "#b0bec5",
                },
            }
        ]
    }
    
    return temp_fig, humi_fig, light_fig

# def update_values(n):
#     temp, humi = get_both()
#     return f'Temperature: {temp} C', f'Humidity: {humi}%'
#

# @app.callback(
#     Output('led-img', 'children'),
#     Input('led-img', 'n_clicks')
# )

#function to control the button on the dashboard
# def control_output(n_clicks):
#     #check if n_clicks is 1 or 0
#     if n_clicks % 2 == 1:
#         print(n_clicks % 2)
#         #turns off light
#         GPIO.output(lightpin, GPIO.LOW)
#         #returns updated img
#         return html.Img(src=app.get_asset_url('off.png'),width='200px', height='200px')
#     else:
#         print(n_clicks % 2)
#         #turns on light
#         GPIO.output(lightpin, GPIO.HIGH)
#         return html.Img(src=app.get_asset_url('on.png'),width='200px', height='200px')
    
# Define the callback function for the button
@app.callback(
    Output('output', 'children'),
    Input('button', 'n_clicks')
)
def update_output(n_clicks):
    if n_clicks % 2 == 1:
        print(n_clicks % 2)
        #turns off motor
        GPIO.output(Motor1,GPIO.LOW)
        #returns updated img
        return ''
    else:
        print(n_clicks % 2)
        #turns on motor
        motor_on()
        return ''

#runs server
if __name__ == '__main__':
    print ('Program is starting ... ')
    client = mqtt.Client()
    client.connect("0.0.0.0", 1883)
    client.on_connect = on_connect
    client.on_message = on_message
    client.loop_start()
    app.run_server(debug=True) 
