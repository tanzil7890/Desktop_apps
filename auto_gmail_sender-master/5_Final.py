


import smtplib, ssl
import csv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

sender_email = "idrisim@beloit.edu"
password = input("Type your password and press enter:")

message = MIMEMultipart("alternative")
message["Subject"] = "Important Financial Information for the Academic Year"
message["From"] = sender_email

html = """\
<html>
  <body>
    <p>Hi {firstName}{lastName},<br>
       I hope this email finds you well. As the new academic year approaches, we would like to provide you with important information regarding the financial aspects of your education at our institution. Please take a moment to review the following details:<br>
       <br>
        Total Tuition Fee:{totTuitionFees} <br>
        
       
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
        for firstName, email, totTuitionFees  in reader:
            personalized_html = html.format(firstName=firstName, totTuitionFees= totTuitionFees)
            message = MIMEMultipart("alternative")
            message["Subject"] = "Important Financial Information for the Academic Year"
            message["From"] = sender_email
            message["To"] = email

            part = MIMEText(personalized_html, "html")
            message.attach(part)

            server.sendmail(sender_email, email, message.as_string())




