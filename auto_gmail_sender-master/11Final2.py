import smtplib
import ssl
import csv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

sender_email = "idrisim@beloit.edu"
password = input("Type your password and press enter:")

# Read email template from index.html file
with open("index.html") as file:
    message_template = file.read()

# Create secure connection with server and send email
context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    server.login(sender_email, password)
    with open("studentsfile.csv") as file:
        reader = csv.DictReader(file)
        for row in reader:
            first_name = row["First.Name"]
            last_name = row["Last.Name"]
            email = row["email"]
            tuition_fee = row["Tot.Tuition.Fees"]
            books_supplies = row["Tot.Books.Supplies"]
            on_campus_price = row["Tot.OnCampusRB"]
            transportation_fees = row["Tot.Transportation"]
            miscellaneous_expenses = row["Tot.Other.Budget"]
            total_budget = row["Tot.Budget"]
            grant_awarded = row["Tot.grants.awd"]
            estimated_indirect_cost = row["Estimated.indirect.cost"]
            estimated_direct_cost = row["Estimated.direct.cost"]

            personalized_message = message_template.format(
                first_name=first_name,
                last_name=last_name,
                tuition_fee=tuition_fee,
                books_supplies=books_supplies,
                on_campus_price=on_campus_price,
                transportation_fees=transportation_fees,
                miscellaneous_expenses=miscellaneous_expenses,
                total_budget=total_budget,
                grant_awarded=grant_awarded,
                estimated_indirect_cost=estimated_indirect_cost,
                estimated_direct_cost=estimated_direct_cost
            )

            message = MIMEMultipart("alternative")
            message["Subject"] = "Important Financial Information for the Academic Year122"
            message["From"] = sender_email
            message["To"] = email

            part = MIMEText(personalized_message, "html")
            message.attach(part)

            server.sendmail(sender_email, email, message.as_string())
