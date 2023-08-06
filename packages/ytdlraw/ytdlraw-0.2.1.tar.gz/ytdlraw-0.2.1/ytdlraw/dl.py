from tkinter.constants import NO
from pytube import YouTube,Playlist

class URLNotEntered(Exception):
    pass

def download_single(url=None):
    try:
        video= YouTube(url).streams.first().download()
        yt = YouTube(url)
        yt.streams.filter(progressive=True,file_extension="mp4").order_by("resolution").desc().first().download()
        
    except Exception as ex:
        raise URLNotEntered("Please enter a (valid) URL")
def download_playlist(url=None):
    
    try:
        yt = Playlist(url)
        for v in yt.videos:
            v.streams.first().download()
    except Exception as ex:
        raise URLNotEntered("Please enter a (valid) URL")

def get_raw_playlist(url=None):
    try:
        pl=Playlist(url)
        return pl
    except:
        raise URLNotEntered("Please enter a (valid) URL")
        
def get_raw_video(url=None):
    try:
        yt=YouTube(url)
        return yt
    except:
        raise URLNotEntered("Please enter a (valid) URL")