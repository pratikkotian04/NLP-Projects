from pytube import YouTube
from pytube import Playlist
import re
import os
import subprocess
'''
# ask for the link from user
link = input("Enter the link of YouTube video you want to download:  ")
yt = YouTube(link)

# Showing details
print("Title: ", yt.title)
print("Number of views: ", yt.views)
print("Length of video: ", yt.length)
print("Rating of video: ", yt.rating)
# Getting the highest resolution possible
'''
# path = r'D:\\Love_Songs\\'
play = Playlist("https://www.youtube.com/playlist?list=PLq-ReH8AtmQiF5L4RKMIxk5xCrPMAYW9i")
play._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")
print(len(play.video_urls))
for url in play.video_urls:
    yt = YouTube(url)
    #
    _filename = "_".join(str(re.sub("-", " ", yt.title)).split())
    audio = yt.streams.get_audio_only()
    audio.download(filename=_filename)
    mp4 = "%s.mp4" % _filename
    mp3 = "%s.mp3" % _filename
    ffmpeg = ('ffmpeg -i %s ' % mp4 + mp3)
    subprocess.call(ffmpeg, shell=True)

files_in_directory = os.listdir(os.getcwd())
filtered_files = [file for file in files_in_directory if file. endswith(".mp4")]
for file in filtered_files:
    path_to_file = os.path.join(os.getcwd(), file)
    os.remove(path_to_file)

print('Download Complete')


'''
ys = yt.streams.get_highest_resolution()
y_audio = yt.streams.filter(only_audio=True).all()
y_audio[3].download()
print(y_audio)
# Starting download
print("Downloading...")
y_audio[0].download("D:\\")
# ys.download()
print("Download completed!!")
'''
