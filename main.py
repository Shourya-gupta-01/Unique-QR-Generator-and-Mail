import os
import qrcode
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import pandas as pd

# Control sending via environment variable. Default is False for safety.
SEND_EMAIL = True

unique_qr = ""            # any string consist of symbols and characters

SMTP_HOST = os.environ.get('SMTP_HOST', 'smtp.gmail.com')
SMTP_PORT = int(os.environ.get('SMTP_PORT', '587'))

data = pd.read_csv("")           # csv file

sender_email = ""                # Sender's mail

cnt = 0
qr_code = []

for i in data[""]:               # name of column in which emails are written

    recipient_email = i
    img = qrcode.make(unique_qr + str(cnt))
    qr_code.append(unique_qr + str(cnt))
    cnt += 1
    img.save(f"{i[:6]}.png")
    
    filename = f"{i[:6]}.png"
    
    if recipient_email != "":
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = ""      # subject of the mail

        body = ""                # body of the mail
        msg.attach(MIMEText(body, 'plain'))
        
        attachment = open(filename, "rb")
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", "attachment; filename=ticket")
        msg.attach(part)

        # Send email only if allowed — helpful for local testing
        if SEND_EMAIL:
            try:
                s = smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=30)
                s.ehlo()
                if SMTP_PORT == 587:
                    s.starttls()
                    s.ehlo()
                # Use the SMTP_PASSWORD provided via environment variable
                s.login(sender_email, "")        # App password key
                s.sendmail(sender_email, recipient_email, msg.as_string())
                s.quit()
                print(f"Email sent to {recipient_email}")
            except smtplib.SMTPAuthenticationError as e:
                print(f"Authentication failed when sending to {recipient_email}: {e}")
                print("If you use Gmail, create an App Password and set it in the SMTP_PASSWORD environment variable.")
            except smtplib.SMTPConnectError as e:
                print(f"Could not connect to SMTP server {SMTP_HOST}:{SMTP_PORT}: {e}")
            except Exception as e:
                print(f"Failed to send to {recipient_email}: {type(e).__name__}: {e}")
                
data["qr_code"] = qr_code
data.to_csv("updated_attedee_list.csv")