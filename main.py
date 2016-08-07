from gmusicapi import Mobileclient

import gMusicLogin
from Raspi import RaspiInputHandler
from mPlayer import mplayerHandler
from GMusicLocalManager import LocalGManager

import os
import pickle
from pygame import mixer
import time


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
mixer.pre_init(44100, -16, 2, 2048)

homeDIR = os.path.expanduser("~") 
libDIR = homeDIR + "/GMusicLocalLibrary/"

try:
	localLibrary = pickle.load( open( libDIR + "libDatabase.p" , "rb" ) )
except:
	print("Recreating Library Save File")
	localLibrary = {}
	localLibrary['EDM'] = {}
	localLibrary['Relaxing'] = {}

try:
	playlists = pickle.load( open( libDIR + "libPlaylists.p" , "rb" ) )
except:
	print("Recreating Playlists Save File")
	playlists = {}
	playlists['EDM'] = []
	playlists['Relaxing'] = []
	playlists['EDM'].append('4b40425b-2e11-388f-aeed-ea736b88662c')
	pickle.dump( playlists , open( libDIR + "libPlaylists.p" , "wb" ) )


nowPlaying = False

workingPlaylist = None

workingPlaylistOBJ = {}
workingPlaylistOBJ['playistGenre'] 	= ""
workingPlaylistOBJ['playlistName'] 	= ""
workingPlaylistOBJ['playlistID'] 	= ""
workingPlaylistOBJ['songIDS'] 	 	= []
workingPlaylistOBJ['trackName']  	= []
workingPlaylistOBJ['artistName'] 	= []
workingPlaylistOBJ['albumID'] 	 	= []
workingPlaylistOBJ['artURL'] 	 	= []
# ==============================================================



# 1.) Login
#--------#
api = Mobileclient()
api.login( gMusicLogin.getUser() , gMusicLogin.getPass() , Mobileclient.FROM_MAC_ADDRESS )


# 2.) Grab Example Playlist 
#------------------------#
workingPlaylist = api.get_station_tracks( playlists['EDM'][0] , 1000 )


# 3.) Store Results in workingLibraryOBJ
#--------------------------------------#
workingPlaylistOBJ['playlistGenre'] = workingPlaylist[0]['genre']
for x in workingPlaylist:

	workingPlaylistOBJ['songIDS'].append( x['nid'] )
	workingPlaylistOBJ['trackName'].append( x['title'] )
	workingPlaylistOBJ['artistName'].append( x['artist'] )
	workingPlaylistOBJ['albumID'].append( x['albumId'] )
	workingPlaylistOBJ['artURL'].append( x['albumArtRef'][0]['url'] )


# DEBUG INFO
print( "LocalLibary Size = " + str( len( localLibrary['EDM'] ) ) )
workingPlaylistLEN = len(workingPlaylistOBJ['trackName'])
print("Filled workingPlaylist with " + str(workingPlaylistLEN) + " songs" )
# DEBUG INFO




# 4.) Check Library for local copy , download if necessary
# ----------------------------------------------------------#
lManager = LocalGManager()

A2 = 0
while A2 < workingPlaylistLEN:
	
	if workingPlaylistOBJ['songIDS'][A2] in localLibrary['EDM']:
		#print( workingPlaylistOBJ['trackName'][A2] + " already exists in library" )
		if nowPlaying == False:
			#start playing 1st song
			fName = os.path.join( libDIR , "EDM" , workingPlaylistOBJ['songIDS'][A2] + ".mp3" )
			mixer.init()
			mixer.music.load(fName)
			mixer.music.play()
			print( "\n[now playing - \"" + workingPlaylistOBJ['songIDS'][A2] +".mp3\"]" +" = " + workingPlaylistOBJ['trackName'][A2] + " - " + workingPlaylistOBJ['artistName'][A2] + "\n" )
			nowPlaying = True

	else:

		wURL = api.get_stream_url( workingPlaylistOBJ['songIDS'][A2] , api.android_id , 'hi' )
		lManager.download( libDIR + "/EDM" , workingPlaylistOBJ['songIDS'][A2] + ".mp3" , wURL )

		localLibrary['EDM'][workingPlaylistOBJ['songIDS'][A2]] = workingPlaylistOBJ
		print( "loaded " + workingPlaylistOBJ['songIDS'][A2] + " into localLibrary" )

	A2 = A2 + 1


while mixer.music.get_busy() == True:
	continue

#Resave Database
pickle.dump( localLibrary , open( libDIR + "libDatabase.p" , "wb" ) )

