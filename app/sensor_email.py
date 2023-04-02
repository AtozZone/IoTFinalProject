import RPi.GPIO as GPIO
import smtplib
import email
import imaplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from time import sleep

# Set up GPIO (subject to changes)
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)

def send_email(current_time):
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


# Main loop
while True:
    # Check light intensity
    light_intensity = #**Code to read current light intensity**#
    if light_intensity < 400:
        # Turn on LED
        GPIO.output(18, GPIO.HIGH)
        
        # Send email notification
        current_time = datetime.now().strftime("%H:%M")
        #**uses the send_email method**#
        send_email(current_time)
    else:
        # Turn off LED
        GPIO.output(18, GPIO.LOW)
    
    # Wait for 10 seconds before checking again
    sleep(10)
