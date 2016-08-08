from tqdm import tqdm
import requests , tty , sys , select , termios , psutil ,time 

from pygame import mixer
import os

import time

# Utility Functions
# ==============================================================
class NonBlockingConsole(object):
    def __enter__(self):
        self.old_settings = termios.tcgetattr(sys.stdin)
        tty.setcbreak(sys.stdin.fileno())
        return self

    def __exit__(self, type, value, traceback):
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.old_settings)

    def get_data(self):
        try:
            if select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], []):
                return sys.stdin.read(1)
        except:
            return '[CTRL-C]'
        return False

# ==============================================================


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

		#time.sleep(3)
		#mixer.music.stop()

		# enter into Raspi-Input / Containment Loop
		# For now , just emulate by waiting for song to be over
		while mixer.music.get_busy() == True:
			with NonBlockingConsole() as nbc:
				while True:
					c = nbc.get_data()
					if c:
						try:
							print(c)
							if c == '\x1b': # escape key
								#os.kill(nowPlaying.pid , signal.SIGKILL )
								mixer.music.stop()
								break
							if c == 's':
								nowPlaying.killPlayerPROC()
								break
							if c == 'v':
								nowPlaying.toggleProgressBar()
							if c == 'p':
								nowPlaying.pause()
							if c == '1':
								nowPlaying.seek( "b" , 1 )
							if c == '2':
								nowPlaying.seek( "b" , 2 )
							if c == '3':
								nowPlaying.seek( "b" , 3 )
							if c == '4':
								nowPlaying.seek( "f" , 1 )
							if c == '5':
								nowPlaying.seek( "f" , 2 )
							if c == '6':
								nowPlaying.seek( "f" , 3 )

						except:
							print("mplayer process must of closed")
							
								
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


