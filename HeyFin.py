from __future__ import print_function
import base64
import httplib2
import os

from email.mime.text import MIMEText

from apiclient import discovery
from apiclient import errors

import oauth2client
from oauth2client import client
from oauth2client import tools

try:
    import argparse
    parser = argparse.ArgumentParser(parents=[tools.argparser])
    parser.add_argument('message', help='The message to send to Fin')
    parser.add_argument('-t', dest='title', help='The optional title of the message')  # nopep8
    flags = parser.parse_args()
except ImportError:
    flags = None

# View all scopes here:  https://developers.google.com/gmail/api/auth/scopes
SCOPES = 'https://mail.google.com/'  # All scopes here.

CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'FinMessenger'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'fin_messenger.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else:  # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


def SendMessage(service, user_id, message):
    """Send an email message.

    Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    message: Message to be sent.

    Returns:
    Sent Message.
    """
    try:
        message = (service.users().messages().send(userId=user_id, body=message).execute())  # nopep8
        return message
    except errors.HttpError as error:
        print ('An error occurred: %s' % error)


def CreateMessage(sender, to, subject, message_text):
    """Create a message for an email.

    Args:
    sender: Email address of the sender.
    to: Email address of the receiver.
    subject: The subject of the email message.
    message_text: The text of the email message.

    Returns:
    An object containing a base64 encoded email object.
    """
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    raw = None
    try:
        raw = {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}
    except Exception:
        raw = {'raw': base64.urlsafe_b64encode(message.as_string())}
    return raw


def SendFinAMessage():
    """Sends an email to Fin with the subject and body passed in as arguments.

    args:
        required 1st arg: Title if -t is not supplied. Body if -t is present.
        -t [title]: (Optional) This will be the title and the 1st arg is the
        body.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)

    body = "The title says it all :)"
    subject = ""
    if flags:
        if flags.title:
            subject = flags.title
            body = flags.message
        else:
            subject = flags.message
    # msg = CreateMessage("zfleischman@gmail.com", "zfleischman@in.getfin.com", subject, body)  # nopep8
    msg = CreateMessage("zfleischman@gmail.com", "zfleischman@gmail.com", subject, body)  # nopep8
    sentMessage = SendMessage(service, "me", msg)
    if sentMessage:
        print ("Message sent!")

if __name__ == '__main__':
    SendFinAMessage()
