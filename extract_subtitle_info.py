import re

def extract_subtitle_info(line):
    # Define the regular expression pattern to match the timestamp and text
    pattern = r"\[(\d{2}):(\d{2})\.(\d{3})\s*-->\s*(\d{2}):(\d{2})\.(\d{3})\]\s*(.*)"
    
    # Match the pattern to the line
    match = re.match(pattern, line)
    
    if match:
        # Extract start time, end time, and text
        start_minute, start_second, start_milisecond, end_minute, end_second, end_milisecond, text = match.groups()
        
        # Convert start and end times to seconds
        start_time_seconds = int(start_minute) * 60 + int(start_second) + int(start_milisecond) / 1000
        end_time_seconds = int(end_minute) * 60 + int(end_second) + int(end_milisecond) / 1000
        
        # Create an object with the extracted data
        subtitle = {
            "start_time": start_time_seconds,
            "end_time": end_time_seconds,
            "text": text.strip()
        }
        
        return subtitle
    else:
        return None