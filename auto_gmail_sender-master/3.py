import smtplib

# Set the sender and receiver email IDs
sender_email_id = "tanzil.student.mail@gmail.com"
receiver_email_ids = ["tanzilidrisi@gmail.com", "tanzilidrisi68@gmail.com"]

# Set the subject and body of the email
subject = "This is an automated email"
body = "This is the body of the email"

# Create a connection to the SMTP server
server = smtplib.SMTP("smtp.gmail.com", 587)

# Login to the SMTP server
server.login(sender_email_id, "Talha@7890")

# Send the email to all the receivers
for receiver_email_id in receiver_email_ids:
    server.sendmail(sender_email_id, receiver_email_id, subject + "\n" + body)

# Close the connection to the SMTP server
server.quit()
