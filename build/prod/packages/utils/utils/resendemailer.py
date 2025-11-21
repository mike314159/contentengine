

from utils.secrets_store import get_secret
import resend
import os

class ResendEmailer:


    def __init__(self, from_name: str, from_addr: str):
        self.api_key = get_secret("resend_api_key")
        resend.api_key = self.api_key
        self.from_name = from_name
        self.from_addr = from_addr


    def send_email(self, to_addr, subject, html):
        # if from_addr is None:
        #     from_addr = "Acme <onboarding@resend.dev>"

        params: resend.Emails.SendParams = {
            "from": f"{self.from_name} <{self.from_addr}>",
            "to": [to_addr],
            "subject": subject,
            "html": html,
        }

        try:
            response = resend.Emails.send(params)
            email_id = response.get("id", None)
            # {
            #     "id": "49a3999c-0ce1-4ea6-ab68-afcd6dc2e794"
            # }
            print("Sent Email Id: ", email_id)
            return True, email_id
        
        except Exception as e:
            print("Error sending email")
            print(e)
            return False, None

    def get_email(self, email_id):
        return resend.Emails.get(email_id=email_id)
    
    def render_html_template(self, template_fn, attrs):
        if not os.path.exists(template_fn):
            return None
        template = open(template_fn, "r").read()
        for k, v in attrs.items():
            replace_str = "{{%s}}" % k
            template = template.replace(replace_str, v)
        return template
    