




import requests

def send_email(recipient, subject, text_body, html_body):
    
    key = 'key-6l6it74s9nhyg2uewl16jfia-r84bc05'
    sandbox = 'particlestew.mailgun.org'
    #recipient = 'particlestew@gmail.com'
    
    request_url = 'https://api.mailgun.net/v3/{0}/messages'.format(sandbox)
    request = requests.post(request_url, auth=('api', key), data={
        'from': 'particlestew@gmail.com',
        'to': recipient,
        'subject': subject,
        'text': text_body,
        'html': html_body
    })
    
    print ('Status: {0}'.format(request.status_code))
    print ('Body:   {0}'.format(request.text))

    
    
    

if __name__ == "__main__":


    send_email("particlestew@gmail.com", "Hello", "Hello World", "Hello World")