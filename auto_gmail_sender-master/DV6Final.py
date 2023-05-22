#It is personlised Desktop email sender from the .csv file.
#It can alse check whether the .csv file have any value in Preferred.Name section, 
#if there is then print preferred_name as a recipient_name. Else, if it is not present then print First.Name and Last.Name instead

import smtplib
import ssl
import csv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from tkinter import Tk, Label, Entry, Text, Button, filedialog


#For sending an email to the desired senders which are available in the .csv file

def send_emails():
    sender_email = sender_email_entry.get()
    password = password_entry.get()
    subject = subject_entry.get()
    body = body_text.get("1.0", "end-1c")
    csv_file = file_path_label.cget("text")

    # Read the CSV file and extract the data
    rows = []
    with open(csv_file) as file:
        reader = csv.DictReader(file)
        for row in reader:
            rows.append(row)

    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        for row in rows:
            # Get the preferred name or use first name and last name
            preferred_name = row["Preferred.Name"]
            first_name = row["First.Name"]
            last_name = row["Last.Name"]

            #This is to check whether preferred_name has any value or not, if not then use first_name and last_name
            recipient_name = preferred_name if preferred_name else f"{first_name} {last_name}"

            personalized_body = body.replace("{recipient_name}", recipient_name)
            for key in row.keys():
                placeholder = "{" + key + "}"
                personalized_body = personalized_body.replace(placeholder, row[key])
            
            message = MIMEMultipart("alternative")
            message["Subject"] = subject
            message["From"] = sender_email
            message["To"] = row["email"]

            part = MIMEText(personalized_body, "html")
            message.attach(part)

            server.sendmail(sender_email, row["email"], message.as_string())


def browse_csv_file():
    file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    file_path_label.config(text=file_path)

# Create the main window
window = Tk()
window.title("Email Sender App")
window.geometry("500x500")

# Sender Email
sender_email_label = Label(window, text="Sender Email:")
sender_email_label.pack()
sender_email_entry = Entry(window)
sender_email_entry.pack()

# Password
password_label = Label(window, text="Password:")
password_label.pack()
password_entry = Entry(window, show="*")
password_entry.pack()

# Subject
subject_label = Label(window, text="Subject:")
subject_label.pack()
subject_entry = Entry(window)
subject_entry.pack()

# Body
body_label = Label(window, text="Body:")
body_label.pack()
body_text = Text(window, height=10)
body_text.pack()

# CSV File
csv_file_label = Label(window, text="CSV File:")
csv_file_label.pack()
file_path_label = Label(window, text="")
file_path_label.pack()
browse_button = Button(window, text="Browse", command=browse_csv_file)
browse_button.pack()

# Send Button
send_button = Button(window, text="Send Emails", command=send_emails)
send_button.pack()

# Start the main loop
window.mainloop()
