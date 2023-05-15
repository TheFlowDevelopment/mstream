# -*- coding: utf-8 -*-
"""
Created on Mon May 15 16:18:24 2023

@author: Ef
"""
import configparser
import vlc
from youtubesearchpython import VideosSearch
from pytube import YouTube
import json

cp = configparser.ConfigParser()
cp.read("config.ini")

streamingservice = cp["UNIVAR"]['streaming_service']
streamingconnector = cp['UNIVAR']['streaming_connector']
print('Launching app..')
print(f'Streaming service: {streamingservice}')
print(f'Streaming connector: {streamingconnector}')

Instance = vlc.Instance("--vout=dummy")
player = Instance.media_player_new()

running = True

last = []
def search(i):
    searcharg = i.split(' ')[1:]
    saf = ''
    for i in searcharg:
        saf = saf + i + ' '
    videosSearch = VideosSearch(saf, limit = 1)
    return videosSearch.result()
while running:
    i = input("Please enter your prompt or type /h to help: ")
    if i.split(' ')[0] == 'start':
        result = search(i)
        result = result['result'][0]
        type_ = result['type']
        id_ = result['id']
        title = result['title']
        publishedTime = result['publishedTime']
        duration = result['duration']
        viewCount = result['viewCount']['short']
        channelName = result['channel']['name']
        a_title = result['accessibility']['title'] #for playlists
        link = result['link']
        print(f'Playing: {title} | {channelName} | {viewCount} | {duration}')
        last = [a_title, link]
        video = YouTube(link)
        best = video.streams.filter(only_audio=True, file_extension='mp4').first().url
        Media = Instance.media_new(best)
        Media.get_mrl()
        player.set_media(Media)
        player.play()
        
    if i == 'pause':
        try:
            player.pause()
        except Exception as e:
            e = e
            pass
        
    if i == 'play':
        try:
            player.play()
        except Exception as e:
            e = e
            pass
        
    if i == 'stop':
        try:
            player.stop()
        except Exception as e:
            e = e 
            pass
        
        
    if i == "quit":
        print('deattaching...')
        running = False
        
    
