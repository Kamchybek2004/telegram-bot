import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

EMAIL_ADDRESS = "kamchy2501@gmail.com"
EMAIL_PASSWORD = "yftp vayz whmz bijs"

def send_email(subject, body):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = EMAIL_ADDRESS
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, EMAIL_ADDRESS, msg.as_string())
        print("Сообщение на почту отправлен успешно!")
    except smtplib.SMTPAuthenticationError as e:
        print(f"Ошибка аутентификации: {e}")
    except Exception as e:
        print(f"Ошибка в: {e}")


