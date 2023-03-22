#pytorch
#cmd installations
#pip install pydash
#pip install dash_daq
#sudo apt-get remove thonny
#sudo apt-get install thonny
#pip install dash-bootstrap-components

import dash.dependencies
import dash_daq as daq
from dash import html, Input, Output, dcc, Dash
import dash_bootstrap_components as dbc
import RPi.GPIO as GPIO
import Freenove_DHT as DHT
import time as time
import smtplib
import email
import imaplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

is_sent = True

Motor1 = 15 # Enable Pin | 22 board
Motor2 = 13 # Input Pin  | 27 board
Motor3 = 11 # Input Pin  | 17 board
#setup GPIO outputs
lightpin = 12
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(lightpin, GPIO.OUT)

DHTPin = 40 #define the pin of DHT11
dht = DHT.DHT(DHTPin) #create a DHT class object

def get_both(): 
    global is_sent   
    #for i in range(0,15):
    #    chk = dht.readDHT11() #read DHT11 and get a return value. Then determine whether data read is normal according to the return value.
    #    if (chk is dht.DHTLIB_OK): #read DHT11 and get a return value. Then determine whether data read is normal according to the return value.
    #        print("DHT11,OK!")
    #        break
    #    time.sleep(0.1)
    chk = dht.readDHT11()
    humi = dht.humidity
    temp = dht.temperature
    if (temp >= 24 and is_sent):
        send_email(temp)   
        is_sent = False
    receive_reply()
    humi = '{0:0.1f}'.format(humi)
    temp = '{0:0.1f}'.format(temp)
    print(humi)
    print(temp)
    #time.sleep(5)
    return temp, humi

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

#initialize app
app = Dash(__name__)
app.title = 'Phase 2'

#initialize image
led_img = html.Img(src=app.get_asset_url('off.png'),width='150px', height='150px')


temp, humi = get_both()
#dashboard layout
app.layout = html.Div([
    html.H1(children='Control Panel'),
    html.H4(children='LED Status'),
    html.Div(id='led-box', children=[
        html.H1(children=True, style={'text-align': 'center'}),
        html.Button(led_img, id='led-img', n_clicks = 0)
    ]),
    
    html.Br(),html.Br(),html.Br(),
    
    html.Div([
        html.Button('Turn on fan', id='button'),
        html.Div(id='output')
    ]),
    
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
                                {"range": [0, 10], "color": "#e1f5fe"},
                                {"range": [10, 20], "color": "#b3e5fc"},
                                {"range": [20, 30], "color": "#81d4fa"},
                                {"range": [30, 40], "color": "#4fc3f7"},
                                {"range": [40, 50], "color": "#29b6f6"},
                            ],
                            "borderwidth": 2,
                            "bordercolor": "#b0bec5",
                        },
                    }
                ]
            },
            style={"width": "50%", "display": "inline-block"},
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
                            "bar": {"color": "#4caf50"},
                            "threshold": {
                                "line": {"color": "black", "width": 4},
                                "thickness": 0.75,
                                "value": 70,
                            },
                            "steps": [
                                {"range": [0, 20], "color": "#e8f5e9"},
                                {"range": [20, 40], "color": "#c8e6c9"},
                                {"range": [40, 60], "color": "#a5d6a7"},
                                {"range": [60, 80], "color": "#81c784"},
                                {"range": [80, 100], "color": "#66bb6a"},
                            ],
                            "borderwidth": 2,
                            "bordercolor": "#b0bec5",
                        },
                    }
                ]
            },
            style={"width": "50%", "display": "inline-block"},
        ),
    ],
    style={"text-align": "center"},
),

    dcc.Interval(
        id='interval-component',
        interval=2 * 1000,  # updates every 2 seconds
        n_intervals=0
    )
], style={'font-size': '24px'})

@app.callback(
    Output("temp-gauge", "figure"),
    Output("humi-gauge", "figure"),
    Input('interval-component', 'n_intervals')
)
def update_gauges(n):
    temp, humi = get_both()
    
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
                        {"range": [0, 10], "color": "#e1f5fe"},
                        {"range": [10, 20], "color": "#b3e5fc"},
                        {"range": [20, 30], "color": "#81d4fa"},
                        {"range": [30, 40], "color": "#4fc3f7"},
                        {"range": [40, 50], "color": "#29b6f6"},
                    ],
                    "borderwidth": 2,
                    "bordercolor": "#b0bec5",
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
                    "bar": {"color": "#4caf50"},
                    "threshold": {
                        "line": {"color": "black", "width": 4},
                        "thickness": 0.75,
                        "value": 70,
                    },
                    "steps": [
                        {"range": [0, 20], "color": "#e8f5e9"},
                        {"range": [20, 40], "color": "#c8e6c9"},
                        {"range": [40, 60], "color": "#a5d6a7"},
                        {"range": [60, 80], "color": "#81c784"},
                        {"range": [80, 100], "color": "#66bb6a"},
                    ],
                    "borderwidth": 2,
                    "bordercolor": "#b0bec5",
                },
            }
        ]
    }
    
    return temp_fig, humi_fig

# def update_values(n):
#     temp, humi = get_both()
#     return f'Temperature: {temp} C', f'Humidity: {humi}%'
#

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
        return html.Img(src=app.get_asset_url('off.png'),width='200px', height='200px')
    else:
        print(n_clicks % 2)
        #turns on light
        GPIO.output(lightpin, GPIO.HIGH)
        return html.Img(src=app.get_asset_url('on.png'),width='200px', height='200px')
    
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
    app.run_server(debug=True) 
