import Neutron
from urllib.parse import urlparse, parse_qs
from pytubefix import YouTube
from pytubefix.cli import on_progress
import whisper
from capture_output import capture_output
from extract_subtitle_info import extract_subtitle_info

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
    

def onSubmitUrlClick():
    setIframeSrc()
    
    set_status("Downloading audio...")
    download_audio(win.getElementById("inputUrl").value)
    
    set_status("Transcribing audio...")
    lines = []
    subtitles_info = []
    # Consume the generator
    for line in capture_output(transcribe_audio):
        if "-->" in line and line not in lines:
            try:
                lines.append(line)
                subtitle_info = extract_subtitle_info(line)
                subtitles_info.append(subtitle_info)
                last_time = subtitles_info[-1].end_time
                set_status("Transcribing audio... [last_time]")
            except Exception as err:
                print(err)


win.getElementById("submitUrl").addEventListener("click", Neutron.event(onSubmitUrlClick))

win.show()