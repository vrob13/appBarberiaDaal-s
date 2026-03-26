from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from datetime import datetime
import streamlit as st


class GoogleCalendar:
    def __init__(self, calendarid):
        self.calendarid = calendarid
        self.service = self._create_service()

    def _create_service(self):
        credentials_info = dict(st.secrets["google_service_account"])
        credentials = service_account.Credentials.from_service_account_info(
            credentials_info,
            scopes=["https://www.googleapis.com/auth/calendar"]
        )
        service = build("calendar", "v3", credentials=credentials)
        return service

    def get_events(self, date=None):
        if not date:
            events = self.service.events().list(calendarId=self.calendarid).execute()
        else:
            start_date = f"{date}T00:00:00Z"
            end_date = f"{date}T23:59:59Z"
            events = self.service.events().list(
                calendarId=self.calendarid,
                timeMin=start_date,
                timeMax=end_date
            ).execute()

        return events.get("items", [])

    def get_start_times(self, date):
        events = self.get_events(date)
        start_times = []

        for event in events:
            start_info = event.get("start", {})
            start_time = start_info.get("dateTime")

            if not start_time:
                continue

            parsed_start_time = datetime.fromisoformat(start_time.replace("Z", "+00:00"))
            hours_minutes = parsed_start_time.strftime("%H:%M")
            start_times.append(hours_minutes)

        return start_times

    def create_event(self, name_event, start_time, end_time, timezone, attendees=None):
        event = {
            "summary": name_event,
            "start": {
                "dateTime": start_time,
                "timeZone": timezone,
            },
            "end": {
                "dateTime": end_time,
                "timeZone": timezone,
            },
        }

        if attendees:
            event["attendees"] = [{"email": email} for email in attendees]

        try:
            created_event = self.service.events().insert(
                calendarId=self.calendarid,
                body=event
            ).execute()
        except HttpError as error:
            raise Exception(f"An error has occurred: {error}")

        return created_event

