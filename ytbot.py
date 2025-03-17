import gradio as gr
import re  # For extracting video ID
from youtube_transcript_api import YouTubeTranscriptApi  # For extracting transcripts

def get_video_id(url):    
    # Regex pattern to match different YouTube video URL formats
    pattern = (
        r"(?:https?:\/\/)?(?:www\.)?"
        r"(?:youtube\.com\/(?:[^\/]+\/.+\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|youtu\.be\/|youtube\.com\/shorts\/)"
        r"([a-zA-Z0-9_-]{11})"
    )
    
    match = re.search(pattern, url)
    return match.group(1) if match else None

def get_transcript(url):
    """Fetches the transcript for a given YouTube URL."""
    video_id = get_video_id(url)
    if not video_id:
        return "Invalid YouTube URL. Please enter a valid one."
    
    try:
        transcript_data = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
        transcript = "\n".join([entry['text'] for entry in transcript_data])
        return transcript
    except Exception as e:
        return f"Error fetching transcript: {str(e)}"

def youtube_transcript_app():
    with gr.Blocks() as interface:
        gr.Markdown("""<h2 style='text-align: center;'>YouTube Video Transcript Generator</h2>""")
        
        video_url = gr.Textbox(label="YouTube Video URL", placeholder="Paste the YouTube Video URL here")
        transcript_output = gr.Textbox(label="Generated Transcript", lines=10, interactive=False)
        generate_btn = gr.Button("Generate Transcript")
        
        generate_btn.click(get_transcript, inputs=video_url, outputs=transcript_output)
    
    return interface

# Run the Gradio app
youtube_transcript_app().launch()
