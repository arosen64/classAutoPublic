import datetime
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

def get_service():
  # If modifying these scopes, delete the file token.json.
    SCOPES = ["https://www.googleapis.com/auth/calendar"]
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("cal_token.json"):
        creds = Credentials.from_authorized_user_file("cal_token.json", SCOPES)
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
        with open("cal_token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("calendar", "v3", credentials=creds)

    except HttpError as error:
        print(f"An error occurred: {error}")
    
    return service

class Google_Calendar:
    CAL = get_service()

    def get_all(self):
        return self.CAL.calendarList().list().execute()

    # creates an event in the given calendar
    def add_event(self,cal_id,event_name:str,start_time:datetime, end_time:datetime, timeZone:str='America/New_York',description:str="",location:str="") -> None:
        event = {
            'summary': event_name,
            'location': location,
            'description': description,
            'start': {
                'dateTime': start_time.isoformat(),
                'timeZone': timeZone,
            },
            'end': {
                'dateTime': end_time.isoformat(),
                'timeZone': timeZone,
            },
            'reminders': {
                'useDefault': False,
                'overrides': [
                {'method': 'popup', 'minutes': 60},
                ],
            },
        }

        self.CAL.events().insert(calendarId=cal_id, body=event).execute()

    def get_events(self,cal_id:str):
        return self.CAL.events().list(calendarId=cal_id).execute()
    
    def update_event(self,cal_id:str,event_id:str,start_time:datetime, end_time:datetime, timeZone:str='America/New_York') -> None:
        event = self.CAL.events().get(calendarId=cal_id, eventId=event_id).execute()
        event['start']['dateTime'] = start_time.isoformat()
        event['end']['dateTime'] = end_time.isoformat()
        event['start']['timeZone'] = timeZone
        event['end']['timeZone'] = timeZone
        self.CAL.events().update(calendarId=cal_id, eventId=event_id, body=event).execute()

