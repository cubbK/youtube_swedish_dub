import Neutron
from urllib.parse import urlparse, parse_qs
from pytubefix import YouTube
from pytubefix.cli import on_progress
import whisper
from capture_output import capture_output
from extract_subtitle_info import extract_subtitle_info
from deep_translator import GoogleTranslator

translator = GoogleTranslator(source='auto', target='sv')

win = Neutron.Window("Youtube Sweidsh Dub", size=(1200, 800), css="def.css")
win.display(file="render.html")

def set_status(status):
    win.getElementById("status").innerHTML = status

# Function to download audio
def download_audio(youtube_url, output_path='downloads'):
    
    yt = YouTube(youtube_url, on_progress_callback=on_progress)
    print(yt.title)

    ys = yt.streams.get_audio_only()
    ys.download(filename="audio.mp4", skip_existing=False)

def setIframeSrc():
    url = win.getElementById("inputUrl").value
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    v_value = query_params.get("v", [None])[0]
    
    win.getElementById("youtube-iframe").src = "https://www.youtube.com/embed/" + v_value

def transcribe_audio():
    model = whisper.load_model("turbo")
    result = model.transcribe("audio.mp4", word_timestamps=True, verbose=True)
    
def escape_quotes(text):
    return text.replace('"', '\\"').replace("'", "\\'")

def onSubmitUrlClick():
    setIframeSrc()
    
    set_status("Downloading audio...")
    download_audio(win.getElementById("inputUrl").value)
    
    set_status("Initializing Whisper...")
    lines = []
    subtitles_info = []
    # Consume the generator
    for index, line in enumerate(capture_output(transcribe_audio)):
        if "-->" in line and line not in lines:
            try:
                lines.append(line)
                subtitle_info = extract_subtitle_info(line, index)
                subtitles_info.append(subtitle_info)
                last_time = subtitles_info[-1]["end_time"]
                set_status(f"Transcribing audio...  Done until minute {seconds_to_minutes(last_time)} ")
                
                translation = translator.translate(subtitle_info["text"])
                
                table_row = f"""<tr><th scope="col">{subtitle_info["index"]}</th><th scope="col">{subtitle_info["start_time"]}</th><th scope="col">{subtitle_info["end_time"]}</th><th scope="col">{escape_quotes(subtitle_info["text"])}</th><th scope="col">{escape_quotes(translation)}</th></tr>"""
                # subtitle_div = win.createElement("div")
                # subtitle_div.innerHTML = escape_quotes(subtitle_info['text'])
                win.getElementById("transcription-table").append(table_row)
                
            except Exception as err:
                print(err)

def seconds_to_minutes(seconds):
    # Calculate minutes and remaining seconds
    minutes = int(seconds // 60)
    remaining_seconds = int(seconds % 60)
    
    # Format as MM:SS
    return f"{minutes:02}:{remaining_seconds:02}"

win.getElementById("submitUrl").addEventListener("click", Neutron.event(onSubmitUrlClick))

win.show()