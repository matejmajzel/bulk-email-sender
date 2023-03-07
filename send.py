import csv, ssl, time
from email.mime.image import MIMEImage
import os
from settings import SENDER_EMAIL, PASSWORD, DISPLAY_NAME, SUBJECT
from smtplib import SMTP
import smtplib
import markdown
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders


def get_msg(csv_file_path, template):
    with open(csv_file_path, encoding="utf8") as file:
        headers = file.readline().split(';')
        headers[len(headers) - 1] = headers[len(headers) - 1][:-1]
    # i am opening the csv file two times above and below INTENTIONALLY, changing will cause error
    with open(csv_file_path, 'r', encoding="utf8") as file:
        data = csv.DictReader(file, delimiter=";")
        for row in data:
            required_string = template
            for header in headers:
                if header == "NAME" or header == "EMAIL":
                    value = row[header]
                    required_string = required_string.replace(f'${header}', value)

                if header == "SEX":
                    value = row[header]
                    if value == "M":
                        required_string = required_string.replace(f'${header}', "Mr.")
                    if value == "Z":
                        required_string = required_string.replace(f'${header}', "Mrs.")
                

            yield row['EMAIL'], required_string


def send_emails(server: SMTP, template):

    sent_count = 0

    for receiver, message in get_msg('prod-textence.csv', template):

        multipart_msg = MIMEMultipart("alternative")

        multipart_msg["Subject"] = SUBJECT
        multipart_msg["From"] = DISPLAY_NAME + f' <{SENDER_EMAIL}>'
        multipart_msg["To"] = receiver

        text = message
        html = markdown.markdown(text)

        part1 = MIMEText(text, "plain", "utf-16")
        part2 = MIMEText(html, "html", "utf-16")

        multipart_msg.attach(part1)
        multipart_msg.attach(part2)


        try:
            server.sendmail(SENDER_EMAIL, receiver,
                            multipart_msg.as_string())
        except Exception as err:
            print(f'Problem occurend while sending to {receiver} ')
            print(err)
            input("PRESS ENTER TO CONTINUE")
        else:
            sent_count += 1
        print(f"Sent {sent_count} emails") 
        time.sleep(10)
        

    print(f"Finished with the count: {sent_count} emails")
    


if __name__ == "__main__":
    host = "smtp.m1.websupport.sk"
    port = 465  # TLS replaced SSL in 1999
    context = ssl.create_default_context()
    with open('compose.md', encoding="utf-8") as f:
        template = f.read()
    try:
        with smtplib.SMTP_SSL(host, port) as server:
            server.connect(host=host, port=port)
            server.ehlo()
            server.login(user=SENDER_EMAIL, password=PASSWORD)

            send_emails(server, template)
            server.quit()
    except Exception as e:
        # Print any error messages to stdout
        print(e)
    


# AAHNIK 2020
