
import sys
sys.path.insert(0, "..")

from utils.secrets_store import get_secret

import resend
from resend_emailer import send_email

api_key = get_secret("resend_api_key")
print("API Key: ", api_key)
resend.api_key = api_key

from_addr = "onboarding@resend.dev"
to_addr =  "services@carbonlake.com"
subject = "Test from Resend Emailer"
html_body = "<p>Congrats on sending your <strong>first email</strong>!</p>"

result = send_email(from_addr, to_addr, subject, html_body)
''' {'id': '9a4a9e21-3214-4749-a9e9-f501039ac847'} '''

