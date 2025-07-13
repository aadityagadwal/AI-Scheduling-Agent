from flask import Flask, request, jsonify
from ai_agent import extract_meeting_info
from calendar_utils import fetch_events
from scheduler import find_common_slot

app = Flask(__name__)

@app.route('/')
def index():
    return {"status": "Flask app is running!"}

@app.route('/schedule', methods=['POST'])
def schedule():
    request_data = request.get_json()
    try:
        # Step 1: Parse email content using LLaMA
        processed = extract_meeting_info(request_data)
        print(f"Processed data: {processed}")
        
        # Step 2: Fetch calendar events for each attendee
        calendar_data = {}
        for attendee in request_data.get("Attendees", []):
            email = attendee.get("email")
            calendar_data[email] = fetch_events(email, processed["Start"], processed["End"])
        
        # Step 3: Find common available slot
        slot = find_common_slot(calendar_data, processed["Duration_mins"])
        
        # Step 4: Build response
        output = {
            **request_data,
            "EventStart": slot["start"],
            "EventEnd": slot["end"],
            "Attendees": [
                {
                    "email": email,
                    "events": events + [slot["event"]]
                } for email, events in calendar_data.items()
            ]
        }
        
        return jsonify({
            "processed": processed,
            "output": output
        })
        
    except Exception as e:
        print(f"Error in schedule endpoint: {str(e)}")
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5060)