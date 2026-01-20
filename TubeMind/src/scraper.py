import re
from youtube_transcript_api import YouTubeTranscriptApi

def extract_video_id(url):
    """Extracts the 11-character YouTube ID from any YouTube URL."""
    pattern = r'(?:v=|\/|embed\/|shorts\/)([a-zA-Z0-9_-]{11})'
    match = re.search(pattern, url)
    return match.group(1) if match else None

def get_transcript(video_id):
    """Fetches the transcript using the modern .fetch() method."""
    try:
        # 2026 Best Practice: Use fetch() instead of get_transcript()
        # This returns a TranscriptList object which is more reliable
        transcript_data = YouTubeTranscriptApi().fetch(video_id, languages=['en'])
        
        # Convert the object data into a raw list and join the text
        transcript_list = transcript_data.to_raw_data()
        full_text = " ".join([entry['text'] for entry in transcript_list])
        
        return full_text
    except Exception as e:
        print(f"Transcript Error: {str(e)}")
        return None