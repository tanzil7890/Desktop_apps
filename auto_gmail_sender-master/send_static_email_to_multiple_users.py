#Desktop app to send the static email to multiple users selected from the .csv file 

import smtplib
import ssl
import csv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import tkinter as tk
from tkinter import filedialog

message_template = """\
<html>
  <body>
    <p>Hi ,<br>
       {body}
    </p>
  </body>
</html>
"""

def send_emails():
    sender_email = sender_email_entry.get()
    password = password_entry.get()
    subject = subject_entry.get()
    body = body_text.get("1.0", tk.END)
    selected_fields = fields_entry.get().split(',')

    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        with filedialog.askopenfile(mode="r", title="Select CSV File") as file:
            reader = csv.DictReader(file)
            for row in reader:
                email = row["email"]

                # Get selected fields from CSV row
                data = {field: row[field] for field in selected_fields}

                # Substitute variables in the message template
                personalized_message = message_template.format(**data, body=body)

                message = MIMEMultipart("alternative")
                message["Subject"] = subject
                message["From"] = sender_email
                message["To"] = email

                part = MIMEText(personalized_message, "html")
                message.attach(part)

                server.sendmail(sender_email, email, message.as_string())

# Create the GUI
window = tk.Tk()
window.title("Email Sender App")

# Create and arrange the GUI elements
sender_label = tk.Label(window, text="Sender Email:")
sender_label.pack()
sender_email_entry = tk.Entry(window)
sender_email_entry.pack()

password_label = tk.Label(window, text="Password:")
password_label.pack()
password_entry = tk.Entry(window, show="*")
password_entry.pack()

subject_label = tk.Label(window, text="Subject:")
subject_label.pack()
subject_entry = tk.Entry(window)
subject_entry.pack()

body_label = tk.Label(window, text="Body:")
body_label.pack()
body_text = tk.Text(window, height=10, width=50)
body_text.pack()

fields_label = tk.Label(window, text="Selected Fields (comma-separated):")
fields_label.pack()
fields_entry = tk.Entry(window)
fields_entry.pack()

send_button = tk.Button(window, text="Send Emails", command=send_emails)
send_button.pack()

# Run the GUI main loop
window.mainloop()
