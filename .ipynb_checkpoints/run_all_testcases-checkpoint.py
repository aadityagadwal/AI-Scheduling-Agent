# run_all_testcases.py

import requests
import json
import time

CLOUDFLARE_URL = "https://wallpapers-luggage-daily-lease.trycloudflare.com/schedule"
HEADERS = {"Content-Type": "application/json"}

test_cases = [
    {
        "name": "Test Case 1: Both attendees available",
        "data": {
            "Request_id": "6118b54f-907b-4451-8d48-dd13d76033a5",
            "Datetime": "2025-07-02T12:34:55",
            "Location": "IIT Mumbai",
            "From": "userone.amd@gmail.com",
            "Attendees": [
                {"email": "usertwo.amd@gmail.com"},
                {"email": "userthree.amd@gmail.com"}
            ],
            "Subject": "Goals Discussion",
            "EmailContent": "Hi Team. Let's meet next Thursday and discuss about our Goals."
        }
    },
    {
        "name": "Test Case 2: USERTHREE busy",
        "data": {
            "Request_id": "6118b54f-907b-4451-8d48-dd13d76033b5",
            "Datetime": "2025-07-02T12:34:55",
            "Location": "IIT Mumbai",
            "From": "userone.amd@gmail.com",
            "Attendees": [
                {"email": "usertwo.amd@gmail.com"},
                {"email": "userthree.amd@gmail.com"}
            ],
            "Subject": "Client Validation - Urgent",
            "EmailContent": "Hi Team. We’ve just received quick feedback from the client indicating that the instructions we provided aren’t working on their end. Let’s prioritize resolving this promptly. Let’s meet Monday at 9:00 AM to discuss and resolve this issue."
        }
    },
    {
        "name": "Test Case 3: Both busy",
        "data": {
            "Request_id": "6118b54f-907b-4451-8d48-dd13d76033c5",
            "Datetime": "2025-07-02T12:34:55",
            "Location": "IIT Mumbai",
            "From": "userone.amd@gmail.com",
            "Attendees": [
                {"email": "usertwo.amd@gmail.com"},
                {"email": "userthree.amd@gmail.com"}
            ],
            "Subject": "Project Status",
            "EmailContent": "Hi Team. Let's meet on Tuesday at 11:00 A.M and discuss about our on-going Projects."
        }
    },
    {
        "name": "Test Case 4: USERTHREE busy",
        "data": {
            "Request_id": "6118b54f-907b-4451-8d48-dd13d76033d5",
            "Datetime": "2025-07-02T12:34:55",
            "Location": "IIT Mumbai",
            "From": "userone.amd@gmail.com",
            "Attendees": [
                {"email": "usertwo.amd@gmail.com"},
                {"email": "userthree.amd@gmail.com"}
            ],
            "Subject": "Client Feedback",
            "EmailContent": "Hi Team. We’ve received the final feedback from the client. Let’s review it together and plan next steps. Let's meet on Wednesday at 10:00 A.M."
        }
    }
]

def run_all_tests():
    for i, test in enumerate(test_cases):
        print(f"\n===== Running {test['name']} =====")
        response = requests.post(CLOUDFLARE_URL, headers=HEADERS, json=test['data'])
        try:
            parsed = response.json()
            print(json.dumps(parsed, indent=2))
        except json.JSONDecodeError:
            print("Response not in JSON format:", response.text)
        time.sleep(1)  # avoid rate-limiting

if __name__ == "__main__":
    run_all_tests()
