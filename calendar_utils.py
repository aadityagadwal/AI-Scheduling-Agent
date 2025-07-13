from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import os
import logging
import json

# ✅ Set up logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

# ✅ Use correct relative path to the `creds/` folder
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
TOKEN_DIR = os.path.join(CURRENT_DIR, 'creds')  # NOT 'ASA/creds'

def fetch_events(email, time_min, time_max):
    token_path = os.path.join(TOKEN_DIR, f"{email}.json")
    
    if not os.path.exists(token_path):
        logging.warning(f"Token file not found for {email}: {token_path}")
        return []
    
    try:
        with open(token_path, 'r') as f:
            creds_data = json.load(f)
        
        creds = Credentials(
            token=creds_data.get('token'),
            refresh_token=creds_data.get('refresh_token'),
            token_uri=creds_data.get('token_uri'),
            client_id=creds_data.get('client_id'),
            client_secret=creds_data.get('client_secret'),
            scopes=creds_data.get('scopes')
        )
        
        service = build("calendar", "v3", credentials=creds)
        
        events_result = service.events().list(
            calendarId='primary', 
            timeMin=time_min, 
            timeMax=time_max,
            singleEvents=True, 
            orderBy='startTime'
        ).execute()
        
        events = events_result.get('items', [])
        formatted = []

        for event in events:
            start_time = event['start'].get('dateTime') or event['start'].get('date')
            end_time = event['end'].get('dateTime') or event['end'].get('date')
            
            formatted.append({
                "StartTime": start_time,
                "EndTime": end_time,
                "Summary": event.get('summary', 'No Title'),
                "Attendees": [att.get("email") for att in event.get("attendees", [])],
                "NumAttendees": len(event.get("attendees", []))
            })

        logging.info(f"✅ Fetched {len(formatted)} events for {email}")
        return formatted

    except Exception as e:
        logging.error(f"❌ Error fetching events for {email}: {str(e)}")
        return []
