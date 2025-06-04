# outlook.py
# ---- Outlook Calendar Integration using Microsoft Graph API ----

import requests
from datetime import datetime
import os

# Environment variables or secrets config
client_id = os.getenv("MS_CLIENT_ID")
client_secret = os.getenv("MS_CLIENT_SECRET")
tenant_id = os.getenv("MS_TENANT_ID")
user_id = os.getenv("MS_USER_ID")

def get_access_token():
    """Authenticate using client credentials and return a Microsoft Graph API token."""
    url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "client_id": client_id,
        "scope": "https://graph.microsoft.com/.default",
        "client_secret": client_secret,
        "grant_type": "client_credentials"
    }

    response = requests.post(url, headers=headers, data=data)
    response.raise_for_status()
    return response.json().get("access_token")

def create_outlook_event(subject, start_time, end_time, body=None, location="NIOA Clinic"):
    """Create a new event in the Outlook calendar associated with the service user."""
    try:
        access_token = get_access_token()

        url = f"https://graph.microsoft.com/v1.0/users/{user_id}/calendar/events"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

        event_payload = {
            "subject": subject,
            "start": {
                "dateTime": start_time.isoformat(),
                "timeZone": "Europe/Athens"
            },
            "end": {
                "dateTime": end_time.isoformat(),
                "timeZone": "Europe/Athens"
            },
            "location": {
                "displayName": location
            },
        }

        if body:
            event_payload["body"] = {
                "contentType": "Text",
                "content": body
            }

        response = requests.post(url, headers=headers, json=event_payload)
        response.raise_for_status()
        return response.json()

    except Exception as e:
        print(f"[!] Failed to create Outlook event: {e}")
        return None

def get_outlook_events(start_date, end_date):
    """Fetch Outlook calendar events between start_date and end_date."""
    try:
        access_token = get_access_token()

        url = (
            f"https://graph.microsoft.com/v1.0/users/{user_id}/calendarView?"
            f"startDateTime={start_date.isoformat()}&endDateTime={end_date.isoformat()}"
        )

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Prefer": 'outlook.timezone="Europe/Athens"',
        }

        response = requests.get(url, headers=headers)
        response.raise_for_status()

        return response.json().get("value", [])

    except Exception as e:
        print(f"[!] Failed to fetch Outlook events: {e}")
        return []

def is_time_slot_available(start_time, end_time):
    """Checks if a given time slot is free in the Outlook calendar."""
    events = get_outlook_events(start_time, end_time)

    for event in events:
        event_start = datetime.fromisoformat(event['start']['dateTime'])
        event_end = datetime.fromisoformat(event['end']['dateTime'])

        if not (end_time <= event_start or start_time >= event_end):
            return False  # Overlap found

    return True

def schedule_if_available(subject, start_time, end_time, body=None, location="NIOA Clinic"):
    """Schedule an event only if the time slot is available in Outlook."""
    if is_time_slot_available(start_time, end_time):
        print("✅ Time slot is available. Creating event...")
        return create_outlook_event(subject, start_time, end_time, body, location)
    else:
        print("❌ Time slot is NOT available. Please choose a different time.")
        return None
