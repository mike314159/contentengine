


from utils.secrets_store import get_secret

import resend


def send_email(from_addr, to_addr, subject, html):

  if from_addr is None:
    from_addr = "Acme <onboarding@resend.dev>"

  api_key = get_secret("resend_api_key")
  resend.api_key = api_key

  # params = {
  #     "sender": from_addr,
  #     "to": [to_addr],
  #     "subject": subject,
  #     "html": html,
  # }


  params: resend.Emails.SendParams = {
      "from": "Acme <onboarding@resend.dev>",
      "to": [to_addr],
      "subject": subject,
      "html": html,
  }

  email = resend.Emails.send(params)
  print(email)


  # r = resend.Emails.send({
  #   "from": from_addr,
  #   "to": to_addr,
  #   "subject": subject,
  #   "html": html_body
  # })
  # print(r)



if __name__ == "__main__":
  pass

  # from utils.secrets_store import get_secret

  # api_key = get_secret("resend_api_key")
  # resend.api_key = api_key

  # from_addr = "onboarding@resend.dev"
  # to_addr =  "services@carbonlake.com"
  # subject = "Test from Resend Emailer"
  # html_body = "<p>Congrats on sending your <strong>first email</strong>!</p>"

  # result = send_email(from_addr, to_addr, subject, html_body)
  # ''' {'id': '9a4a9e21-3214-4749-a9e9-f501039ac847'} '''

  
# import os
# import resend

# resend.api_key = os.environ["RESEND_API_KEY"]

# params = {
#     "from": "Acme <onboarding@resend.dev>",
#     "to": ["delivered@resend.dev"],
#     "subject": "hello world",
#     "html": "<strong>it works!</strong>",
# }

# email = resend.Emails.send(params)
# print(email)

  email_obj = resend.Emails.send(params)
