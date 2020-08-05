import smtplib

# In the end of send_email - file should be deleted


class Email(object):
    def __init__(self, status_file_name, gmail_sender, gmail_receiver, gmail_password):
        self.status_file_name = status_file_name
        self.gmail_sender = gmail_sender
        self.gmail_receiver = gmail_receiver
        self.gmail_password = gmail_password

    def send(self):
        with open(self.status_file_name, "r") as f_status:
            email_content = f_status.read()

        print(email_content)

        subject = "Yad2 item's report"
        body = email_content

        message = """From: %s\nTo: %s\nSubject: %s\n\n%s
        """ % (self.gmail_sender, ", ".join(self.gmail_receiver), subject, body)

        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(self.gmail_sender, self.gmail_password)
        server.sendmail(self.gmail_sender, self.gmail_receiver, message)
        server.close()
        print('Daily report e-mail sent!')


