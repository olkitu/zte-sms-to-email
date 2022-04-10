import requests
import json
from datetime import datetime
import os
import time

URL=os.getenv('URL', 'http://192.168.32.1')
REFERER=URL+"index.html"

MAILGUN_API_URL=os.getenv('MAILGUN_API_URL', 'https://api.mailgun.net/v3/') + os.getenv('MAIL_FROM', 'noreply@example.org').split('@')[1]
MAIL_FROM=os.getenv('MAIL_FROM')
MAIL_TO=os.getenv('MAIL_TO')
print('Mailgun API URL: ' + MAILGUN_API_URL)
print('Mail From: ' + MAIL_FROM)
print('Mail To: ' + MAIL_TO)

# Get Data from API
def get_data(endpoint):
    headers = {'Referer': REFERER}
    response = requests.get(URL+endpoint, headers=headers)
    return response

def post_data(endpoint, data):
    headers = {'Referer': REFERER}
    response = requests.post(URL+endpoint, data=data, headers=headers)
    return response

def get_last_message():
    response = get_data('/goform/goform_get_cmd_process?isTest=false&cmd=sms_data_total&page=0&data_per_page=1&mem_store=1&tags=10&order_by=order+by+id+desc')
    output = json.loads(response.text)
    return output['messages']

def delete_message(id):
    response = post_data('/goform/goform_set_cmd_process', 'isTest=false&goformId=DELETE_SMS&msg_id='+id+';&notCallback=true')
    if response.status_code == 200:
        print("Message " + id +" deleted")
        return True
    else:
        print("Message deletion failed" + response.text)
        return False
    
# Send Email using Mailgun API.
def send_mailgun_mail(number, content, received):
    response = requests.post(MAILGUN_API_URL + '/messages',
        auth=('api', os.getenv('MAILGUN_API_KEY')),
        data={
            "from": MAIL_FROM,
            "to": [ MAIL_TO ],
            "subject": "New message from " + number,
            "text": "Message: " + content + "\r\n" + "Received: " + received
        }
    )
    if response.status_code == 200:
        print("Email Send")
        print(response.text)
        return True
        
    else:
        print("Email sending failed: ")
        print(str(response.status_code) + ' ' + response.text)
        return False

# Run always
while True:
    message = get_last_message()
    if message:
        id = message[0]['id']
        number = message[0]['number']
        received = str(datetime.strptime(message[0]['date'], '%y,%m,%d,%H,%M,%S,+12'))
        content = bytes.fromhex(str(message[0]['content']).replace("00", "")).decode('latin-1')

        print()
        print("Parsing message: ")
        print()
        print("Id: " + id)
        print("Sender: "+ number)
        print("Receive time: " + received)
        print("Message: " + content)
        print()

        # Send message via Mailgun API
        email = send_mailgun_mail(number, content, received)
        # If email sending success, delete message
        if email == True:
          delete_message(id)
    # Wait 1s before try again find message
    time.sleep(1)
  