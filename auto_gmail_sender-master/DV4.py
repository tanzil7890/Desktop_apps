import smtplib
import ssl
import csv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import tkinter as tk
from tkinter import filedialog

def send_emails():
    sender_email = sender_email_entry.get()
    password = password_entry.get()
    subject = subject_entry.get()
    body = body_text.get("1.0", tk.END)
    selected_fields = fields_listbox.curselection()
    selected_fields = [fields_listbox.get(idx) for idx in selected_fields]
    
    with open(file_path, newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            email = row["email"]
            personalized_body = body
            for field in selected_fields:
                if field in row:
                    field_value = row[field]
                    personalized_body = personalized_body.replace(field, field_value)

            message = MIMEMultipart("alternative")
            message["Subject"] = subject
            message["From"] = sender_email
            message["To"] = email

            part = MIMEText(personalized_body, "html")
            message.attach(part)

            context = ssl.create_default_context()
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                server.login(sender_email, password)
                server.sendmail(sender_email, email, message.as_string())

def browse_file():
    global file_path
    file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    file_path_label.config(text=file_path)

root = tk.Tk()
root.title("Email Sender")
root.geometry("500x600")

# Sender Email
sender_email_label = tk.Label(root, text="Sender Email:")
sender_email_label.pack()
sender_email_entry = tk.Entry(root)
sender_email_entry.pack()

# Password
password_label = tk.Label(root, text="Password:")
password_label.pack()
password_entry = tk.Entry(root, show="*")
password_entry.pack()

# Subject
subject_label = tk.Label(root, text="Subject:")
subject_label.pack()
subject_entry = tk.Entry(root)
subject_entry.pack()

# Body
body_label = tk.Label(root, text="Body:")
body_label.pack()
body_text = tk.Text(root, height=10)
body_text.pack()

# Fields
fields_label = tk.Label(root, text="Fields:")
fields_label.pack()
fields_listbox = tk.Listbox(root, selectmode=tk.MULTIPLE)
fields_listbox.pack()

# Browse CSV File
browse_button = tk.Button(root, text="Browse", command=browse_file)
browse_button.pack()

# File Path Label
file_path_label = tk.Label(root, text="")
file_path_label.pack()

# Send Button
send_button = tk.Button(root, text="Send Emails", command=send_emails)
send_button.pack()

root.mainloop()

