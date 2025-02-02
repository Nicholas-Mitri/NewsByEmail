import smtplib
import ssl, os, sys


def send(receiver="", subject="", message="", MIME="plain", encoding="utf-8") -> None:
    """
    Sends an email using Gmail's SMTP server.

    Args:
        receiver (str): Email address of the recipient
        subject (str): Subject line of the email
        message (str): Body content of the email
        MIME (str): MIME type for the email content (default: 'plain')
        encoding (str): Character encoding for the email (default: 'utf-8')

    Returns:
        None
    """
    # Gmail SMTP server settings
    host = "smtp.gmail.com"
    port = 465

    # Email credentials
    username = "ngmitri04@gmail.com"
    password = os.getenv("GMAIL_PASSWORD")
    if not password:
        print(
            "No password found! Please add password to environment/PATH and try again."
        )
        sys.exit()

    # Create SSL context and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(host, port, context=context) as server:
        server.login(username, password)
        email_message = f"Subject: {subject}\nTo: {receiver}\nContent-Type: text/{MIME}; charset={encoding}\n\n{message}"
        server.sendmail(username, receiver, email_message.encode(encoding=encoding))


if __name__ == "__main__":

    # Change to your own email
    receiver = "example@gmail.com"
    message = "hello"
    send(receiver=receiver, subject="test", message=message)
