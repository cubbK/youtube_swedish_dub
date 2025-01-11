import Neutron
from urllib.parse import urlparse, parse_qs

win = Neutron.Window("Youtube Sweidsh Dub", size=(1200, 800), css="def.css")
win.display(file="render.html")


def onSubmitUrlClick():
    url = win.getElementById("inputUrl").value
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    v_value = query_params.get("v", [None])[0]
    
    win.getElementById("youtube-iframe").src = "https://www.youtube.com/embed/" + v_value


win.getElementById("submitUrl").addEventListener("click", Neutron.event(onSubmitUrlClick))

win.show()