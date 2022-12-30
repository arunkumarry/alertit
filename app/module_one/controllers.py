import os
from app.module_one.models import Mongo
import requests
from flask import Blueprint, request, jsonify, Response
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse, Say
import imaplib
import email


mod = Blueprint('routes', __name__, url_prefix='/v1')

@mod.route('/email', methods=['GET', 'POST'])
def send_email():
  mail = imaplib.IMAP4_SSL('imap.gmail.com', 993)
  print(mail)
  # imaplib module implements connection based on IMAPv4 protocol
  mail.login('arunr.rubydev@gmail.com', 'Suvisu606670')
  mail.list() # Lists all labels in GMail
  mail.select('inbox') # Connected to inbox.
  result, data = mail.uid('search', None, "ALL")
  print(data)
  # search and return uids instead
  i = len(data[0].split()) # data[0] is a space separate string
  print(i)
  for x in reversed(range(i)):
    latest_email_uid = data[0].split()[x] # unique ids wrt label selected
    result, email_data = mail.uid('fetch', latest_email_uid, '(RFC822)')
    # fetch the email body (RFC822) for the given ID
    raw_email = email_data[0][1]
    #continue inside the same for loop as above
    raw_email_string = raw_email.decode('utf-8')
    # converts byte literal to string removing b''
    email_message = email.message_from_string(raw_email_string)
    print(email.utils.parseaddr(email_message['From'])[1])
    if email.utils.parseaddr(email_message['From'])[1] == 'no-reply@swiggy.in' :
    # this will loop through all the available multiparts in mail
      print(email_message['subject'])
      return email_message['subject']
  return("Done")




@mod.route("/voice", methods=['GET', 'POST'])
def voice():

  """Respond to incoming phone calls with a 'Hello world' message"""
  # Start our TwiML response
  resp = VoiceResponse()

  # Read a message aloud to the caller
  a = send_email("no-reply@swiggy.in")
  resp.say(a, voice='alice')
  print(str(resp))
  return Response(str(resp), mimetype="application/xml")



@mod.route('/alert', methods=['POST'])
def voice_alert():
  data = request.get_json()
  print(data)
  # Your Account Sid and Auth Token from twilio.com/console
  # DANGER! This is insecure. See http://twil.io/secure
  if data['id'] > 3 :
      account_sid = 'ACfafbdebecca52f1d12afb60b79cfeb64'
      auth_token = '8fc4dfc8243a158ae58ab7423fc48073'
      client = Client(account_sid, auth_token)
      #r = requests.get('http://localhost:5000/v1/voice')
      call = client.calls.create(
                              url='http://localhost:5000/v1/voice',
                              to='+917780497748',
                              from_='+16143289021'
                          )

      print(call.sid)
      return(call.sid)
  else :
      print("NA")