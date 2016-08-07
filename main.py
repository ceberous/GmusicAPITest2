from gmusicapi import Mobileclient

import sys , select , tty , termios

import psutil

import urllib
from tqdm import tqdm

from flask import Response
import requests
from io import BytesIO

import os
import subprocess
import threading
import time

import gMusicLogin
from Raspi import RaspiInputHandler
from mPlayer import mplayerHandler
from mManager import Downloader

# Raspi Input Setup
# ==============================================================
#import Rpi.GPIO as GPIO

#GPIO.setmode( GPIO.BCM )
#GPIO.setup( 23 , GPIO.IN , pull_up_down=GPIO.PUD_UP )
#GPIO.setup( 24 , GPIO.IN , pull_up_down=GPIO.PUD_DOWN )

# ==============================================================



# {tracking} - functions
# ==============================================================
'''
#allStations = api.get_all_stations()

#print all local saved playlists
for x in playlists:
	i = 0
	while i < len(playlists[x]):
		print(playlists[x][i])
		i = i + 1;
'''
# ==============================================================



# USER DATA 
# ==============================================================

HALF_MB = 524288  # in bytes
MP3_TYPE = 'audio/mpeg'

playlists = {}
playlists['EDM'] = []
playlists['Relaxing'] = {}

playlists['EDM'].append('4b40425b-2e11-388f-aeed-ea736b88662c')


nowPlaying = None
workingPlaylist = None
workingPLAYLISTSongIDs = []
# ==============================================================


api = Mobileclient()
api.login( gMusicLogin.getUser() , gMusicLogin.getPass() , Mobileclient.FROM_MAC_ADDRESS )



workingPlaylist = api.get_station_tracks( playlists['EDM'][0] , 1000 )
for x in workingPlaylist:
	print(x['artist'] + " |=| " + x['title'] + " |=| " + x['nid'])
	workingPLAYLISTSongIDs.append(x['nid'])


workingPlaylistLEN = len(workingPLAYLISTSongIDs)
print("Filled workingPlaylist with " + str(workingPlaylistLEN) + " songs" )




'''
pI = 0
tmp_Downloader = Downloader()
while pI < workingPlaylistLEN:
	
	wURL = api.get_stream_url( workingPLAYLISTSongIDs[pI] , api.android_id , 'hi' )

	nowPlaying = mplayerHandler();
	nowPlaying.startPlayerPROC(mp3Test)
	inputHandler = RaspiInputHandler(nowPlaying)
	
	#tmp_Downloader.download( wURL )

	print("done with song")
	pI = pI + 1

'''



wURL = api.get_stream_url( workingPLAYLISTSongIDs[0] , api.android_id , 'hi' )
response1 = requests.get( wURL , stream=True )
with open( "2.mp3" , 'wb' ) as f:
	for data in tqdm( response1.iter_content(chunk_size=HALF_MB) ):
		f.write(data)