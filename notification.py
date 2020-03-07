from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
# FOR CREATE MESSAGES
import base64
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import mimetypes
import os

from apiclient import errors

# If modifying these scopes, delete the file token.pickle.
SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.send',
    'https://mail.google.com/' 
    ]

def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                '../credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)

    # Call the Gmail API
    results = service.users().labels().list(userId='me').execute()
    labels = results.get('labels', [])

    if not labels:
        print('No labels found.')
    else:
        print('Labels:')
        for label in labels:
            print(label['name'])

def CreateMessage(sender, to, subject, message_text):
    """Create a message for an email.

    Args:
        sender: Email address of the sender.
        to: Email address of the receiver.
        subject: The subject of the email message.
        message_text: The text of the email message.

    Returns:
        An object containing a base64url encoded email object.
    """
    message = MIMEText(message_text, 'html')
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    raw = base64.urlsafe_b64encode(message.as_bytes())
    raw = raw.decode()
    return {'raw': raw}

def send_email(sender, to, subject, message):
    """Send an email message.

    Args:
        sender: Sender Email Address.
        to: Recepient Email Address. 
        subject: Email Subject.
        message: Message to be sent.

    Returns:
        Sent Message.
    """

    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # GMAIL Service
    service = build('gmail', 'v1', credentials=creds)
    # Create message by CreateMessage function
    raw_message = CreateMessage(sender, to, subject, message)
    # Call the Gmail API
    send = service.users().messages().send(userId='me', body=raw_message).execute()
    if not send:
        print('message not sent')
    else:
        print('message successfully sent')

template_notification = '''<table style="background-color:#fff;margin:5% auto;width:100%;max-width:600px" cellspacing="0" cellpadding="0" border="0" bgcolor="#fff" align="center">

	<tbody><tr>
		<td>
			<table style="padding:10px 15px;font-size:14px" width="100%" cellspacing="0" cellpadding="0" border="0" bgcolor="#0b5b67" align="center">
				<tbody><tr>
					<td style="padding:5px 0 0" width="60%" align="center">
						<span style="font-family:Roboto,RobotoDraft,Helvetica,Arial,sans-serif;color:#fff">LAPORAN MASALAH {}</span>
					</td>
				</tr>
			</tbody></table>
		</td>
	</tr>
	<tr>
		<td style="padding:25px 15px 10px">
			<table width="100%">
				<tbody><tr>
					<td>
						<h1 style="font-family:Roboto,RobotoDraft,Helvetica,Arial,sans-serif;margin:0;font-size:16px;font-weight:bold;line-height:24px;color:rgba(0,0,0,0.70)">Ada Keluhan Baru nih bro,</h1>
					</td>
				</tr>
				<tr>
					<td>
						<p style="font-family:Roboto,RobotoDraft,Helvetica,Arial,sans-serif;margin:0;font-size:16px;line-height:24px;color:rgba(0,0,0,0.70)">Laporan Masalah {}:<br>
                            {}<br>Tanggal Kejadian : {}<br>Kamu bisa kontak korban di Email {}<br>Klik <a href="https://admin.tukulsa.site/{}">di sini</a> untuk masuk ke halaman admin</p>
					</td>
                </tr>
                <tr>
                    <td>
                        <h1 style="font-family:Roboto,RobotoDraft,Helvetica,Arial,sans-serif;margin:0;font-size:16px;font-weight:bold;line-height:24px;color:rgba(0,0,0,0.70)">Good Luck Bro! Semoga Cepet Selesai Masalahnya</h1>
                    </td>
                </tr>
			</tbody></table>
		</td>
	</tr>
</tbody></table>'''

if __name__ == '__main__':
    main()