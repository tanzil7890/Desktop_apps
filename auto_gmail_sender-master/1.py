import smtplib, ssl
import csv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

sender_email = "tanzil.student.mail@gmail.com"
receiver_email = "tanzilidrisi@gmail.com"
password = input("Type your password and press enter:")

message = MIMEMultipart("alternative")
message["Subject"] = "multipart test"
message["From"] = sender_email
message["To"] = receiver_email

# Create the plain-text and HTML version of your message
text = """\
Hi, 
How are you?
Real Python has many great tutorials:
www.realpython.com"""
html = """\
<html>
  <body>
    <img style="width: 100%" src="https://cdn-imgix.headout.com/tour/7064/TOUR-IMAGE/44a6d6c4-86fd-4f93-8204-7ffd4fa4e4e4-4445-IMGWorldsofAdventure-2.JPG" alt="Italian Trulli">
    <p>Hi,<br>
       How are you?<br>
       <a href="http://www.realpython.com">Real Python</a> 
       has many great tutorials.
    </p>
  </body>
</html>
"""

# Turn these into plain/html MIMEText objects
part1 = MIMEText(text, "plain")
part2 = MIMEText(html, "html")

# Add HTML/plain-text parts to MIMEMultipart message
# The email client will try to render the last part first
message.attach(part1)
message.attach(part2)

# Create secure connection with server and send email
context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    server.login(sender_email, password)
    with open("contacts_file.csv") as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row
        for name, email, grade in reader:
            server.sendmail(
                sender_email,
                email,
                message.as_string()
            )