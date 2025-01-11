import Neutron
from urllib.parse import urlparse, parse_qs
from pytubefix import YouTube
from pytubefix.cli import on_progress

url = "url"



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


def onSubmitUrlClick():
    setIframeSrc()
    
    set_status("Downloading audio...")
    download_audio(win.getElementById("inputUrl").value)


win.getElementById("submitUrl").addEventListener("click", Neutron.event(onSubmitUrlClick))

win.show()