import smtplib
import ssl
import csv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

sender_email = "idrisim@beloit.edu"
password = input("Type your password and press enter:")

# Also, if there is preferred name available then please use it instead of first_name and last_name.

message_template = """\
<html>
  <body>
    <p>Hi {name},<br>
       I hope this email finds you well. As the new academic year approaches, we would like to provide you with important information regarding the financial aspects of your education at our institution. Please take a moment to review the following details:<br>
       <br>
        Total Tuition Fee: {tuition_fee}<br>
        Total Books and Supplies: {books_supplies}<br>
        On-Campus Price: {on_campus_price}<br>
        Transportation Fees: {transportation_fees}<br>
        Miscellaneous Expenses: {miscellaneous_expenses}<br>
        <br>
        Total Budget You Need to Consider: {total_budget}<br>
        <br>
        Grant Awarded for Student: {grant_awarded}<br>
        <br>
        Estimated Indirect Cost: {estimated_indirect_cost}<br>
        Estimated Direct Cost: {estimated_direct_cost}<br>
        <br>
        To ensure a smooth financial process, please verify if you have filled out the Free Application for Federal Student Aid (FAFSA). It is crucial to complete the FAFSA to determine your eligibility for federal financial aid. If you have not yet filled out the FAFSA, we highly recommend doing so promptly to maximize your financial assistance opportunities.<br>
        <br>
        If you have any questions or need assistance regarding your financial aid package or the FAFSA application, please reach out to our Financial Aid Office. They are ready to guide you through the process and provide you with any necessary support.<br>
        <br>
        We understand that managing the costs of education can be challenging, but we are committed to helping you make the most of your academic journey. Remember that there are various resources available to support you financially, and our team is dedicated to exploring all possible options to make your education affordable and accessible.<br>
        <br>
        Thank you for choosing our institution as your educational partner. We look forward to assisting you in achieving your academic goals.<br>
        <br>
       <br>
       <br>
       
    </p>
  </body>
</html>
"""

# Create secure connection with server and send email
context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    server.login(sender_email, password)
    with open("studentsfile.csv") as file:
        reader = csv.DictReader(file)
        for row in reader:
            first_name = row["First.Name"]
            preferred_name = row["Preferred.Name"]
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

            # Use preferred name if available, otherwise use first_name and last_name
            if preferred_name:
                name = preferred_name
            else:
                name = f"{first_name} {last_name}"

            personalized_message = message_template.format(
                name=name,
                #last_name=last_name,
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
            message["Subject"] = "Important Financial Information for the Academic Year22"
            message["From"] = sender_email
            message["To"] = email

            part = MIMEText(personalized_message, "html")
            message.attach(part)

            server.sendmail(sender_email, email, message.as_string())


            
