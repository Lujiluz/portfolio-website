from flask import Flask, request, redirect, url_for, session, render_template
import os
import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery
from google.auth.transport.requests import Request

# Flask app setup
app = Flask(__name__)
app.secret_key = 'TRYEMAIL'  # Replace with a secure secret key

# OAuth 2.0 setup
CLIENT_SECRETS_FILE = "credentials.json"  # Path to your OAuth 2.0 client credentials JSON file
SCOPES = ['https://www.googleapis.com/auth/gmail.send']
API_SERVICE_NAME = 'gmail'
API_VERSION = 'v1'

@app.route('/')
def index():
    return 'Welcome to the Flask Gmail API integration!'

@app.route('/authorize')
def authorize():
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES)
    flow.redirect_uri = url_for('oauth2callback', _external=True)

    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true')

    session['state'] = state

    return redirect(authorization_url)

@app.route('/oauth2callback')
def oauth2callback():
    state = session['state']

    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES, state=state)
    flow.redirect_uri = url_for('oauth2callback', _external=True)

    authorization_response = request.url
    flow.fetch_token(authorization_response=authorization_response)

    credentials = flow.credentials
    session['credentials'] = credentials_to_dict(credentials)

    return redirect(url_for('send_email'))

@app.route('/send_email')
def send_email():
    if 'credentials' not in session:
        return redirect('authorize')

    credentials = google.oauth2.credentials.Credentials(
        **session['credentials'])

    service = googleapiclient.discovery.build(
        API_SERVICE_NAME, API_VERSION, credentials=credentials)

    email_message = create_message('me', 'recipient@example.com', 'Test Subject', 'Test Body')
    send_message(service, 'me', email_message)

    session['credentials'] = credentials_to_dict(credentials)

    return 'Email sent successfully!'

def create_message(sender, to, subject, message_text):
    from email.mime.text import MIMEText
    import base64

    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    return {'raw': raw}

def send_message(service, user_id, message):
    try:
        message = service.users().messages().send(userId=user_id, body=message).execute()
        print('Message Id: %s' % message['id'])
        return message
    except Exception as error:
        print(f'An error occurred: {error}')
        return None

def credentials_to_dict(credentials):
    return {'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes}

if __name__ == '__main__':
    app.run('localhost', 8080, debug=True)
