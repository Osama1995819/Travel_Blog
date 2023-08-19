import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Email configuration
sender_email = 'your_sender_email@example.com'
receiver_email = 'osamanaeem1995@gmail.com'
subject = 'Subject of your email'
message = 'Hello, this is the body of your email.'

# Setup the MIME
msg = MIMEMultipart()
msg['From'] = sender_email
msg['To'] = receiver_email
msg['Subject'] = subject

# Attach the message to the MIME
msg.attach(MIMEText(message, 'plain'))

# Connect to the SMTP server
smtp_server = 'smtp.gmail.com'
smtp_port = 587
smtp_username = 'your_smtp_username'
smtp_password = 'your_smtp_password'

try:
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()  # Use TLS
    server.login(smtp_username, smtp_password)

    # Send email
    server.sendmail(sender_email, receiver_email, msg.as_string())
    print('Email sent successfully!')
except Exception as e:
    print('Error sending email:', e)
finally:
    server.quit()
