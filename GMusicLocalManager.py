from tqdm import tqdm
import requests

from pygame import mixer
import os

import time

class LocalGManager:

	def __init__(self):

		mixer.pre_init(44100, -16, 2, 2048)

	def download( self , directoryPATH , fileName , wURL ):

		if not os.path.exists( directoryPATH ):
			os.makedirs(directoryPATH)

		response1 = requests.get( wURL , stream=True )
		
		with open( os.path.join( directoryPATH , fileName )  , 'wb' ) as f:
			for data in tqdm( response1.iter_content(chunk_size=524288) ):
				f.write(data)


	def playLocalSong( self , filePATH ):

		mixer.init()
		mixer.music.load(filePATH)
		mixer.music.play()

		time.sleep(3)
		mixer.music.stop()

		# enter into Raspi-Input / Containment Loop
		# For now , just emulate by waiting for song to be over
		while mixer.music.get_busy() == True:
			continue


	def analyzePlaylist( self , workingPlaylist ):

		workingPlaylistOBJ = {}
		workingPlaylistOBJ['playistGenre'] 	= ""
		workingPlaylistOBJ['playlistName'] 	= ""
		workingPlaylistOBJ['playlistID'] 	= ""
		workingPlaylistOBJ['songIDS'] 	 	= []
		workingPlaylistOBJ['trackName']  	= []
		workingPlaylistOBJ['artistName'] 	= []
		workingPlaylistOBJ['albumID'] 	 	= []
		workingPlaylistOBJ['artURL'] 	 	= []	

		workingPlaylistOBJ['playlistGenre'] = workingPlaylist[0]['genre']
		for x in workingPlaylist:

			workingPlaylistOBJ['songIDS'].append( x['nid'] )
			workingPlaylistOBJ['trackName'].append( x['title'] )
			workingPlaylistOBJ['artistName'].append( x['artist'] )
			workingPlaylistOBJ['albumID'].append( x['albumId'] )
			workingPlaylistOBJ['artURL'].append( x['albumArtRef'][0]['url'] )


		# DEBUG INFO
		workingPlaylistLEN = len(workingPlaylistOBJ['trackName'])
		print("Filled workingPlaylist with " + str(workingPlaylistLEN) + " songs" )
		# DEBUG INFO

		return workingPlaylistOBJ


