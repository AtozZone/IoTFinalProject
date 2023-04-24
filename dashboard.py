# LED image
# temp gauge
# humi gauge
# motor status
# light intensity
# status of the light
# email notification

#import RPi.GPIO as GPIO
# import Freenove_DHT as DHT
import dash
import dash_bootstrap_components as dbc
from dash import html, Input, Output, dcc, Dash
import dash_daq as daq
from dash.dependencies import Input, Output
import time as time
import smtplib
import email
import imaplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

is_sent = True

Motor1 = 15  # Enable Pin | 22 board
Motor2 = 13  # Input Pin  | 27 board
Motor3 = 11  # Input Pin  | 17 board
# setup GPIO outputs
lightpin = 12
# GPIO.setmode(GPIO.BOARD)
# GPIO.setwarnings(False)
# GPIO.setup(lightpin, GPIO.OUT)

DHTPin = 40  # define the pin of DHT11
# dht = DHT.DHT(DHTPin) #create a DHT class object


# def get_both():
#     global is_sent
#     # for i in range(0,15):
#     #    chk = dht.readDHT11() #read DHT11 and get a return value. Then determine whether data read is normal according to the return value.
#     #    if (chk is dht.DHTLIB_OK): #read DHT11 and get a return value. Then determine whether data read is normal according to the return value.
#     #        print("DHT11,OK!")
#     #        break
#     #    time.sleep(0.1)
#     # chk = dht.readDHT11()
#     # humi = dht.humidity
#     # temp = dht.temperature
#     if temp >= 24 and is_sent:
#         send_email(temp)
#         is_sent = False
#     receive_reply()
#     humi = "{0:0.1f}".format(humi)
#     temp = "{0:0.1f}".format(temp)
#     print(humi)
#     print(temp)
#     # time.sleep(5)
#     return temp, humi


# def motor_on():
#     global Motor1  # Enable Pin | 22 board
#     global Motor2  # Input Pin  | 27 board
#     global Motor3  # Input Pin  | 17 board
#     # GPIO.setup(Motor1,GPIO.OUT)
#     # GPIO.setup(Motor2,GPIO.OUT)
#     # GPIO.setup(Motor3,GPIO.OUT)

#     # GPIO.output(Motor1,GPIO.HIGH)
#     # GPIO.output(Motor2,GPIO.LOW)
#     # GPIO.output(Motor3,GPIO.HIGH)


# def send_email(temp):
#     # Set up the email addresses and password
#     my_address = "iotburner28@gmail.com"  # Replace with your own Gmail address
#     my_password = "uefa acwp roct hnuc"  # Replace with your Gmail password
#     recipient_address = (
#         "ilikefortniteseason4@gmail.com"  # Replace with the recipient's email address
#     )

#     # Create the email message
#     msg = MIMEMultipart()
#     msg["From"] = my_address
#     msg["To"] = recipient_address
#     msg["Subject"] = "IoT Fan"

#     # Add the body to the email
#     body = (
#         "The current temperature is "
#         + str(temp)
#         + ". Would you like to turn on the fan?"
#     )
#     msg.attach(MIMEText(body, "plain"))

#     # Log in to the Gmail SMTP server
#     server = smtplib.SMTP("smtp.gmail.com", 587)
#     server.starttls()
#     server.login(my_address, my_password)

#     # Send the email
#     text = msg.as_string()
#     server.sendmail(my_address, recipient_address, text)

#     # Log out of the server
#     print("sent to " + recipient_address)
#     server.quit()


# def receive_reply():
#     EMAIL = "iotburner28@gmail.com"  # Replace with your own Gmail address
#     PASSWORD = "uefa acwp roct hnuc"  # Replace with your Gmail password
#     SERVER = "imap.gmail.com"

#     # connect to the server and go to its inbox
#     mail = imaplib.IMAP4_SSL(SERVER)
#     mail.login(EMAIL, PASSWORD)

#     mail.select("inbox")
#     status, data = mail.search(None, "ALL")
#     mail_ids = []

#     for block in data:
#         mail_ids += block.split()

#     for i in mail_ids:
#         status, data = mail.fetch(i, "(RFC822)")

#         for response_part in data:
#             if isinstance(response_part, tuple):
#                 message = email.message_from_bytes(response_part[1])

#                 mail_from = message["from"]
#                 mail_subject = message["subject"]

#                 if message.is_multipart():
#                     mail_content = ""

#                     for part in message.get_payload():
#                         if part.get_content_type() == "text/plain":
#                             mail_content += part.get_payload()
#                 else:
#                     mail_content = message.get_payload()

#                 if (
#                     mail_content == "yes"
#                     or "yes" in mail_subject.lower()
#                     or any(
#                         "yes" in recipient.lower()
#                         for recipient in message.get_all("to", [])
#                     )
#                     or "yes" in mail_content.lower()
#                 ):
#                     print(f"From: {mail_from}")
#                     print(f"Subject: {mail_subject}")
#                     print(f"Content: {mail_content}")
#                     # can start motor
#                     motor_on()


# sets up the app and gets external css like bootstrap
app = dash.Dash(
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        "/assets/style.css",
        "https://fonts.googleapis.com/css?family=Roboto",
    ]
)
app.title = "Phase 4"

# sidebar design
sidebar = html.Div(
    [
        html.H6("IoT", className="display-block text-center fs-1"),
        html.H6("Dashboard", className="display-block text-center fs-1"),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/index", active="exact"),
                dbc.NavLink("Page 1", href="/page1", active="exact"),
                dbc.NavLink("Page 2", href="/page2", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
        dbc.NavLink(
            "Username",
            href="/login",
            active="exact",
            className="mt-auto text-center fs-3",
        ),
        dbc.NavLink(
            "Logout", href="/index", active="exact", className="text-center py-3 fs-3"
        ),
    ],
    className="sidebar d-flex flex-column flex-shrink-0 p-2 text-white bg-dark",
    style={
        "width": "15rem",
        "height": "100vh",
        "border": "0.5px solid gray",
    },
)
temp = 19
humi = 33
# gauge design
gauge = html.Div(
    [
        html.Div(
            [
                html.H3(
                    "Temperature",
                    className="bold text-center p-4 text-light",
                ),
                daq.Gauge(
                    id="temp-gauge",
                    label={
                        # gets temperature from static value
                        "label": "{:.2f}°C".format(temp),
                        "style": {
                            "fontSize": "20px",
                            "fontWeight": "bold",
                            "fontFamily": "Roboto, sans-serif",
                            "color": "white",
                        },
                    },
                    color={
                        "gradient": True,
                        "ranges": {
                            "#00C0F5": [0, 25],
                            "#E3FC00": [25, 50],
                            "#FFBB00": [50, 75],
                            "red": [75, 100],
                        },
                    },
                    value=temp,
                    min=0,
                    max=100,
                    labelPosition="bottom",
                    style={
                        "textAlign": "center",
                        "fontFamily": "Roboto, sans-serif",
                        "color": "white",
                        "height": "30vh",
                    },
                    scale=3,
                    showCurrentValue=False,
                ),
            ],
            className="gauge card text-light mx-5",
            style={"background-color": "#1c1e22"},
        ),
        html.Div(
            [
                html.H3(
                    "Humidity",
                    className="bold text-center p-4 text-light",
                ),
                daq.Gauge(
                    id="humi-gauge",
                    label={
                        # change temperature value here
                        "label": "{:}%".format(humi),
                        "style": {
                            "fontSize": "20px",
                            "fontWeight": "bold",
                            "fontFamily": "Roboto, sans-serif",
                            "color": "white",
                        },
                    },
                    color={
                        "gradient": True,
                        "ranges": {
                            "#00FFF7": [0, 33],
                            "#00BBFF": [33, 66],
                            "#0022FF": [66, 100],
                        },
                    },
                    value=humi,
                    min=0,
                    max=100,
                    labelPosition="bottom",
                    style={
                        "textAlign": "center",
                        "fontFamily": "Roboto, sans-serif",
                        "color": "white",
                        "height": "30vh",
                    },
                    scale=3,
                    showCurrentValue=False,
                ),
            ],
            className="card text-light mx-5 mt-5",
            style={"background-color": "#1c1e22"},
        ),
    ],
    className="",
    style={"height": "100%"},
)

dcc.Interval(
    id="interval-component", interval=2 * 1000, n_intervals=0  # updates every 2 seconds
)

slider = html.Div(
    className="card m-5",
    style={
        "background-color": "#1c1e22",
        "width": "325px",
        "height": "80vh",
        "text-align": "center",
    },
    children=[
        html.H3("Light Intensity", className="bold text-center p-4 text-light"),
        html.Img(
            src="https://www.onlygfx.com/wp-content/uploads/2022/03/sun-clipart-set-5.png",
            className="img-fluid mx-auto",
            style={"width": "60px", "height": "60px", "margin-top": "20px"},
        ),
        html.Div(
            style={"padding-left": "23px"},
            children=[
                dcc.Slider(
                    id="my-slider",
                    min=0,
                    max=1000,
                    value=700,
                    step=1,
                    marks={400: {"label": "400"}},
                    vertical=True,
                    disabled=True,
                    className="slider-container d-flex justify-content-center align-items-center m-auto",
                ),
                html.P(
                    "",
                    id="slider-value",
                    className="text-light m-5 fs-3",
                    style={"padding-right": "22px"},
                ),
            ],
        ),
        html.P(
            "Email Status",
            className="text-light fs-3 pt-5 mt-5",
            style={"textDecoration": "underline"},
        ),
        html.P("Email has been received", className="text-light fs-5"),
    ],
)


@app.callback(
    Output("slider-value", "children"),
    [Input("my-slider", "value")],
)
def update_slider_value(value):
    return f"{value}"


status = html.Div(
    [
        html.Div(
            [
                html.H3(
                    "LED Status",
                    className="bold text-center p-4 text-light",
                ),
                html.Img(
                    id="led-image",
                    src="/assets/off.png",
                    className="img-fluid mx-auto my-5",
                    style={"width": "100px", "height": "100px", "margin-top": "20px"},
                ),
                daq.PowerButton(
                    id="our-power-button-1",
                    on=False,
                    color="#faf561",
                    style={"padding-bottom": "20px"},
                ),
            ],
            className="card text-light mx-5",
            style={
                "background-color": "#1c1e22",
                "margin-bottom": "230px",
            },  # add margin to the bottom of the card
        ),
        html.Div(
            [
                html.H3(
                    "LED Status",
                    className="bold text-center p-4 text-light",
                ),
                html.Img(
                    src="/assets/off-blue-fan.png",
                    className="img-fluid mx-auto my-5",
                    style={"width": "100px", "height": "100px", "margin-top": "20px"},
                ),
                daq.PowerButton(
                    id="our-power-button-2",
                    on=False,
                    color="#61e1fa",
                    style={"padding-bottom": "20px", "pointer-events": "none"},
                ),
            ],
            className="card text-light mx-5",
            style={
                "background-color": "#1c1e22",
                "margin-top": "20px",
            },  # add margin to the top of the card
        ),
    ],
    className="my-5",
    style={"height": "100%", "width": "400px"},
)

@app.callback(
    Output("led-image", "src"),
    Input("our-power-button-1", "on")
)
def update_image(on):
    if on:
        return "/assets/on.png"
    else:
        return "/assets/off.png"

# displays all the components
content = html.Div(
    [
        html.H2("Content", className="display-4"),
        html.Hr(),
        html.P("Welcome to the content area!"),
    ],
    style={"padding": "2rem"},
)

app.layout = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(sidebar, width="auto"),
                dbc.Col(gauge, width="auto", style={"margin-left": "200px"}),
                dbc.Col(slider, width="auto"),
                dbc.Col(status, style={"margin-right": "0"}),
            ],
            style={"align-items": "center"},
        )
    ],
    className="bg-dark",
)

if __name__ == "__main__":
    app.run(debug=True)
