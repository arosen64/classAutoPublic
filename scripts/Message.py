import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import base64
from email.message import EmailMessage
import google.auth
from googleapiclient.discovery import build
from enviorVars import SENDER_EMAIL

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/gmail.send","https://www.googleapis.com/auth/gmail.readonly"]


def get_mail():
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("mail_token.json"):
    creds = Credentials.from_authorized_user_file("mail_token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("mail_token.json", "w") as token:
      token.write(creds.to_json())

  try:
    # Call the Gmail API
    service = build("gmail", "v1", credentials=creds)

  except HttpError as error:
    # TODO(developer) - Handle errors from gmail API.
    print(f"An error occurred: {error}")

  return service  


class Gmail:
  MAIL = get_mail()

  def send_message(self,recipient:str,subject:str,body:str,sender:str=SENDER_EMAIL):
    try:
      message = EmailMessage()

      message.set_content(body)

      message["To"] = recipient
      message["From"] = sender
      message["Subject"] = subject

      # encoded message
      encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

      create_message = {"raw": encoded_message}
      # pylint: disable=E1101
      self.MAIL.users().messages().send(userId="me", body=create_message).execute()
    except HttpError as error:
      print(f"An error occurred: {error}")
