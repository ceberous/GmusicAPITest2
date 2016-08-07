from gmusicapi import Mobileclient

import gMusicLogin
from Raspi import RaspiInputHandler
from mPlayer import mplayerHandler
from GMusicLocalManager import LocalGManager

import os
import threading
import pickle
import time


# USER DATA 
# ==============================================================
homeDIR = os.path.expanduser("~") 
libDIR = homeDIR + "/GMusicLocalLibrary/"

try:
	localLibrary = pickle.load( open( libDIR + "libDatabase.p" , "rb" ) )
except:
	print("Recreating Library Save File")
	localLibrary = {}
	localLibrary['EDM'] = {}
	localLibrary['Relaxing'] = {}

print( "LocalLibary Size = " + str( len( localLibrary['EDM'] ) ) )

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
# ==============================================================


# 1.) Login / Initialize
#--------#
api = Mobileclient()
api.login( gMusicLogin.getUser() , gMusicLogin.getPass() , Mobileclient.FROM_MAC_ADDRESS )
lManager = LocalGManager()

# 2.) Grab Example Playlist 
#------------------------#
workingPlaylist = api.get_station_tracks( playlists['EDM'][0] , 1000 )


# 3.) Store Results in workingLibraryOBJ
#--------------------------------------#
workingPlaylistOBJ = lManager.analyzePlaylist(workingPlaylist)


# 4.) Check Library for local copy , download if necessary
# ----------------------------------------------------------#
A2 = 0
while A2 < len(workingPlaylistOBJ['songIDS']):
	
	if workingPlaylistOBJ['songIDS'][A2] in localLibrary['EDM']:
		print( workingPlaylistOBJ['trackName'][A2] + " already exists in library" )
	else:
		wURL = api.get_stream_url( workingPlaylistOBJ['songIDS'][A2] , api.android_id , 'hi' )
		lManager.download( libDIR + "/EDM" , workingPlaylistOBJ['songIDS'][A2] + ".mp3" , wURL )
		localLibrary['EDM'][workingPlaylistOBJ['songIDS'][A2]] = workingPlaylistOBJ
		print( "loaded " + workingPlaylistOBJ['songIDS'][A2] + " into localLibrary" )

	#start playing 1st song
	if nowPlaying == False:
		fName = os.path.join( libDIR , "EDM" , workingPlaylistOBJ['songIDS'][A2] + ".mp3" )
		p1 = threading.Thread( target=lManager.playLocalSong , args=(fName,) , kwargs=None )
		p1.start()
		print( "\n[now playing - \"" + workingPlaylistOBJ['songIDS'][A2] +".mp3\"]" +" = " + workingPlaylistOBJ['trackName'][A2] + " - " + workingPlaylistOBJ['artistName'][A2] + "\n" )
		nowPlaying = True

	A2 = A2 + 1


# [emulation] waiting on the raspi main input loop
p1.join()


#Resave Database
pickle.dump( localLibrary , open( libDIR + "libDatabase.p" , "wb" ) )

