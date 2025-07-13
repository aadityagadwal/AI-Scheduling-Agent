import json
import re
from datetime import datetime, timedelta
from openai import OpenAI

BASE_URL = "http://localhost:4000/v1"
MODEL_ID = "/home/user/Models/meta-llama/Meta-Llama-3.1-8B-Instruct"
client = OpenAI(api_key="NULL", base_url=BASE_URL)

def extract_meeting_info(request_data):
    email_text = request_data.get("EmailContent", "")
    current_date = request_data.get("Datetime", "")
    
    # Try LLM first
    try:
        response = client.chat.completions.create(
            model=MODEL_ID,
            temperature=0.0,
            messages=[{
                "role": "system",
                "content": "You are a JSON extraction assistant. You MUST respond with ONLY valid JSON. No explanations, no markdown, no additional text."
            }, {
                "role": "user",
                "content": f"""
Current date and time: {current_date}

Extract meeting information from this email and return ONLY this JSON structure:

{{
  "Start": "YYYY-MM-DDTHH:MM:SS+05:30",
  "End": "YYYY-MM-DDTHH:MM:SS+05:30", 
  "Duration_mins": number
}}

Email: {email_text}
"""
            }]
        )
        
        content = response.choices[0].message.content.strip()
        
        # Enhanced JSON extraction
        def extract_json_robust(text):
            # Remove markdown
            cleaned = re.sub(r"```json|```", "", text).strip()
            
            # Find JSON block with balanced braces
            start = cleaned.find('{')
            if start == -1:
                return None
                
            brace_count = 0
            for i in range(start, len(cleaned)):
                if cleaned[i] == '{':
                    brace_count += 1
                elif cleaned[i] == '}':
                    brace_count -= 1
                    if brace_count == 0:
                        return cleaned[start:i+1]
            return None
        
        json_part = extract_json_robust(content)
        
        if json_part:
            try:
                parsed_json = json.loads(json_part)
                # Validate required fields
                required_fields = ["Start", "End", "Duration_mins"]
                if all(field in parsed_json for field in required_fields):
                    return parsed_json
            except json.JSONDecodeError:
                pass
                
    except Exception as e:
        print(f"LLM extraction failed: {e}")
    
    # Fallback to rule-based extraction
    return create_fallback_response(email_text, current_date)

def create_fallback_response(email_text, current_date):
    """Create a fallback response using rule-based extraction"""
    try:
        # Parse the current date
        base_date = datetime.fromisoformat(current_date.replace('Z', '+00:00'))
        
        # Extract duration from email
        duration_match = re.search(r'(\d+)\s*(minutes?|mins?|hour?s?)', email_text.lower())
        if duration_match:
            duration_num = int(duration_match.group(1))
            duration_unit = duration_match.group(2)
            if 'hour' in duration_unit:
                duration_mins = duration_num * 60
            else:
                duration_mins = duration_num
        else:
            duration_mins = 60  # Default to 1 hour
        
        # Look for day references
        day_pattern = r'\b(monday|tuesday|wednesday|thursday|friday|saturday|sunday)\b'
        day_match = re.search(day_pattern, email_text.lower())
        
        if day_match:
            target_day = day_match.group(1)
            days_map = {
                'monday': 0, 'tuesday': 1, 'wednesday': 2, 'thursday': 3,
                'friday': 4, 'saturday': 5, 'sunday': 6
            }
            
            # Find the next occurrence of that day
            current_weekday = base_date.weekday()
            target_weekday = days_map[target_day]
            
            days_ahead = target_weekday - current_weekday
            if days_ahead <= 0:
                days_ahead += 7
            
            target_date = base_date + timedelta(days=days_ahead)
        else:
            target_date = base_date + timedelta(days=1)
        
        # Set default time (9:00 AM)
        start_time = target_date.replace(hour=9, minute=0, second=0, microsecond=0)
        end_time = start_time + timedelta(minutes=duration_mins)
        
        return {
            "Start": start_time.strftime("%Y-%m-%dT%H:%M:%S+05:30"),
            "End": end_time.strftime("%Y-%m-%dT%H:%M:%S+05:30"),
            "Duration_mins": duration_mins
        }
        
    except Exception as e:
        print(f"Fallback extraction failed: {e}")
        return {
            "Start": "2025-07-16T09:00:00+05:30",
            "End": "2025-07-16T10:00:00+05:30", 
            "Duration_mins": 60
        }
