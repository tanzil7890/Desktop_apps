import smtplib, ssl
import csv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

sender_email = "idrisim@beloit.edu"
password = input("Type your password and press enter:")

message = MIMEMultipart("alternative")
message["Subject"] = "Notifying students about their grades."
message["From"] = sender_email

html = """\
<html>
  <body>
    <img style="width: 100%" src="https://cdn-imgix.headout.com/tour/7064/TOUR-IMAGE/44a6d6c4-86fd-4f93-8204-7ffd4fa4e4e4-4445-IMGWorldsofAdventure-2.JPG" alt="Italian Trulli">
    <p>Hi {name},<br>
       How are you?<br>
       <a href="http://www.realpython.com">Real Python</a> 
       has many great tutorials. <br>
       Your grade is {grade}. Enjoy the summer.
    </p>
  </body>
</html>
"""

# Create secure connection with server and send email
context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    server.login(sender_email, password)
    with open("contactFile1.csv") as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row
        for name, email, grade in reader:
            personalized_html = html.format(name=name, grade=grade)
            message = MIMEMultipart("alternative")
            message["Subject"] = "NOTIFYING STUDENTS ABOUT THEIR GRADES Test"
            message["From"] = sender_email
            message["To"] = email

            part = MIMEText(personalized_html, "html")
            message.attach(part)

            server.sendmail(sender_email, email, message.as_string())
