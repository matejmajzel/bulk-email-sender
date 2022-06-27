import os
from dotenv import load_dotenv

load_dotenv()

DISPLAY_NAME = os.getenv('display_name')
SENDER_EMAIL = os.getenv('sender_email')
PASSWORD = os.getenv('password')
SUBJECT = os.getenv('subject')

try:
    assert DISPLAY_NAME
    assert SENDER_EMAIL
    assert PASSWORD
    assert SUBJECT
except AssertionError:
    print('Please set up credentials. Read https://github.com/aahnik/automailer#usage')
else:
    print('Credentials loaded successfully')
