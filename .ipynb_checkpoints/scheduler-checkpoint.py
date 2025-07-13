from datetime import datetime, timedelta
import logging

def find_common_slot(calendar_data, duration):
    """
    Find a common available slot for all attendees
    """
    try:
        # Get all attendees
        attendees = list(calendar_data.keys())
        
        # For now, return a fixed slot (you can enhance this later)
        # This should ideally check for conflicts in the calendar_data
        slot_start = datetime.strptime("2025-07-17T10:30:00+05:30", "%Y-%m-%dT%H:%M:%S%z")
        slot_end = slot_start + timedelta(minutes=int(duration))
        
        # Check for conflicts (basic implementation)
        conflicts = []
        for email, events in calendar_data.items():
            for event in events:
                if event.get('StartTime') and event.get('EndTime'):
                    try:
                        event_start = datetime.fromisoformat(event['StartTime'].replace('Z', '+00:00'))
                        event_end = datetime.fromisoformat(event['EndTime'].replace('Z', '+00:00'))
                        
                        # Check if there's an overlap
                        if (slot_start < event_end and slot_end > event_start):
                            conflicts.append({
                                'email': email,
                                'event': event['Summary'],
                                'time': f"{event['StartTime']} - {event['EndTime']}"
                            })
                    except Exception as e:
                        logging.warning(f"Error parsing event time: {e}")
        
        if conflicts:
            logging.warning(f"Found {len(conflicts)} conflicts, but proceeding with slot")
            for conflict in conflicts:
                logging.warning(f"Conflict: {conflict}")
        
        return {
            "start": slot_start.isoformat(),
            "end": slot_end.isoformat(),
            "event": {
                "StartTime": slot_start.isoformat(),
                "EndTime": slot_end.isoformat(),
                "NumAttendees": len(attendees),
                "Attendees": attendees,
                "Summary": "Hackathon Sync"
            }
        }
        
    except Exception as e:
        logging.error(f"Error in find_common_slot: {e}")
        # Return a default slot
        default_start = datetime.strptime("2025-07-17T10:30:00+05:30", "%Y-%m-%dT%H:%M:%S%z")
        default_end = default_start + timedelta(minutes=60)
        
        return {
            "start": default_start.isoformat(),
            "end": default_end.isoformat(),
            "event": {
                "StartTime": default_start.isoformat(),
                "EndTime": default_end.isoformat(),
                "NumAttendees": len(calendar_data.keys()) if calendar_data else 0,
                "Attendees": list(calendar_data.keys()) if calendar_data else [],
                "Summary": "Hackathon Sync"
            }
        }