import smtplib
import ssl
import csv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

sender_email = "idrisim@beloit.edu"
password = input("Type your password and press enter:")

message_template = """\
<html>
  <body>
    <p>Hi {First.Name} {Last.Name},<br>
       I hope this email finds you well. As the new academic year approaches, we would like to provide you with important information regarding the financial aspects of your education at our institution. Please take a moment to review the following details:<br>
       <br>
        Total Tuition Fee: {Total.tuition.fee}<br>
        Total Books and Supplies: {Total.books.supplies}<br>
        On-Campus Price: {On.Campus.price}<br>
        Transportation Fees: {Transportation.fees}<br>
        Miscellaneous Expenses: {Miscellaneous.expenses}<br>
        <br>
        Total Budget You Need to Consider: {Total.budget}<br>
        <br>
        Grant Awarded for Student: {Grant.awarded.for.student}<br>
        <br>
        Estimated Indirect Cost: {Estimated.indirect.cost}<br>
        Estimated Direct Cost: {Estimated.direct.cost}<br>
        <br>
        To ensure a smooth financial process, please verify if you have filled out the Free Application for Federal Student Aid (FAFSA). It is crucial to complete the FAFSA to determine your eligibility for federal financial aid. If you have not yet filled out the FAFSA, we highly recommend doing so promptly to maximize your financial assistance opportunities.<br>
        <br>
        If you have any questions or need assistance regarding your financial aid package or the FAFSA application, please reach out to our Financial Aid Office. They are ready to guide you through the process and provide you with any necessary support.<br>
        <br>
        We understand that managing the costs of education can be challenging, but we are committed to helping you make the most of your academic journey. Remember that there are various resources available to support you financially, and our team is dedicated to exploring all possible options to make your education affordable and accessible.<br>
        <br>
        Thank you for choosing our institution as your educational partner. We look forward to assisting you in achieving your academic goals.<br>
        <br>
    </p>
  </body>
</html>
"""

# Create secure connection with server and send email
context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    server.login(sender_email, password)
    with open("students_file.csv") as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row
        for row in reader:
            first_name, last_name, email, total_tuition_fee, total_books_supplies, on_campus_price, transportation_fees, miscellaneous_expenses, total_budget, grant_awarded, estimated_indirect_cost, estimated_direct_cost, is_fafsa_filled = row

            personalized_message = message_template.format(
                First=first_name,
                Last=last_name,
                Total={'tuition': 'USD ' + total_tuition_fee},
                Total.books={'supplies': 'USD ' + total_books_supplies},
                On={'Campus': 'USD ' + on_campus_price},
                Transportation={'fees': 'USD ' + transportation_fees},
                Miscellaneous={'expenses': 'USD ' + miscellaneous_expenses},
                Grant={'awarded': 'USD ' + grant_awarded},
                Estimated={'indirect': 'USD ' + estimated_indirect_cost, 'direct': 'USD ' + estimated_direct_cost}
            )

            message = MIMEMultipart("alternative")
            message["Subject"] = "Important Financial Information for the Academic Year"
            message["From"] = sender_email
            message["To"] = email

            part = MIMEText(personalized_message, "html")
            message.attach(part)

            server.sendmail(sender_email, email, message.as_string())
