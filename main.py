from gmusicapi import Mobileclient

import sys , select , tty , termios

import psutil

import os
import subprocess
import threading
import time

import gMusicLogin

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




# USER DATA 
# ==============================================================

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
	print(x['artist'] + " |=| " + x['title'])
	workingPLAYLISTSongIDs.append(x['nid'])


workingPlaylistLEN = len(workingPLAYLISTSongIDs)
print("Filled workingPlaylist with " + str(workingPlaylistLEN) + " songs" )




class RaspiInputHandler(object):

	def __init__(self , nowPlayingOBJ ):

		self.nowPlaying = nowPlayingOBJ

		self.p2 = None

		self.__thread = threading.Thread( target = self.readButtonStateHelperTest , args=() )
		self.__thread.start()
		self.playing = True
		self.__thread.join()
		self.playing = False
		

	def readMPlayerOutput(self):

		output = self.nowPlaying.PlayerPROC.stdout
		tmp = str(output)
		for x in tmp:
			for y in x:
				print(y)

		return


	def readButtonStateHelperTest(self):

		print( "[RASPI-EMULATION] == Started Waiting Around for GPIO Interrupt" )

		self.playing = self.nowPlaying.PlayerPROC.returncode
		print(self.playing)

		with NonBlockingConsole() as nbc:
			while True:
				c = nbc.get_data()
				if c:
					try:
						print(c)
						if c == '\x1b': # escape key
							break
						if c == 's':
							self.nowPlaying.killPlayerPROC()
							break
						if c == 'v':
							self.nowPlaying.toggleProgressBar()
						if c == 'p':
							self.nowPlaying.pause()
						if c == '1':

							self.nowPlaying.seek( "b" , 1 )
						
							#self.p2 = threading.Thread( target = self.readMPlayerOutput , args=() )
							#self.p2.start()
							#self.p2.join()

						if c == '2':
							self.nowPlaying.seek( "b" , 2 )
						if c == '3':
							self.nowPlaying.seek( "b" , 3 )
						if c == '4':
							self.nowPlaying.seek( "f" , 1 )
						if c == '5':
							self.nowPlaying.seek( "f" , 2 )
						if c == '6':
							self.nowPlaying.seek( "f" , 3 )

					except:
						if psutil.pid_exists(self.nowPlaying.PlayerPROC.pid):
							print("mplayer process must of closed")
							os.kill(self.nowPlaying.PlayerPROC.pid , 1)
							return	
						else:
							print("unknown problem ... still continuing")
							pass



	def readButtonStateHelper(self):

		try:

			#GPIO.wait_for_edge( 23 , GPIO.FALLING )
			print( "Falling Edge Detected" )
			print( str( threading.current_thread() ) )

		except KeyboardInterrupt:

			#GPIO.cleanup()
			print("error")

		#GPIO.cleanup()


class mplayerHandler:

	def __init__(self):
		self.PlayerPROC = None
		
	def startPlayerPROC( self , url):
		with open( os.devnull , 'w' ) as temp:
			self.PlayerPROC = subprocess.Popen( [ "/usr/bin/mplayer" , url ] , stdin=subprocess.PIPE , stdout=subprocess.PIPE , stderr=temp )
		#self.PlayerPROC.stdout.close()
		print( "Started mplayer. PID = " + str(self.PlayerPROC.pid) )	

	def killPlayerPROC( self ):
		self.PlayerPROC.terminate()
		print("Process Terminated!!!!")

	def toggleProgressBar( self ):
		s1 = bytes( 'P' , 'UTF-8' )  
		self.PlayerPROC.stdin.write(s1)
		self.PlayerPROC.stdin.flush()
		print("Toggled ProgressBar!!!!")		

	def pause( self ):
		s1 = bytes( ' ' ,  'UTF-8' )  
		self.PlayerPROC.stdin.write(s1)
		self.PlayerPROC.stdin.flush()
		print("Paused!!!!")

	def seek( self , direction , size ):
		
		# mplayer only has 3 sizes 
		# LEFT | RIGHT 	= 10 seconds
		# UP   | DOWN 	= 1 minute
		# PGUP | PGDWN 	= 10 minute

		k_LEFT 	= bytes( '\x1b[D' , 'UTF-8' )
		k_RIGHT = bytes( '\x1b[C' , 'UTF-8' )
		k_UP	= bytes( '\x1b[A' , 'UTF-8' )
		k_DOWN	= bytes( '\x1b[B' , 'UTF-8' )
		k_PGUP	= bytes( '\x1b[5~' , 'UTF-8' )
		k_PGDWN	= bytes( '\x1b[6~' , 'UTF-8' )

		if direction == "f":
			if size == 1:
				self.PlayerPROC.stdin.write(k_RIGHT)
				self.PlayerPROC.stdin.flush()
				print("Jumped-Forward --> 10 seconds")
			elif size == 2:
				self.PlayerPROC.stdin.write(k_UP)
				self.PlayerPROC.stdin.flush()
				print("Jumped-Forward --> 1 minute")
			elif size == 3:
				self.PlayerPROC.stdin.write(k_PGUP)
				self.PlayerPROC.stdin.flush()
				print("Jumped-Forward --> 10 minutes")

		elif direction == "b":
			if size == 1:
				self.PlayerPROC.stdin.write(k_LEFT)
				self.PlayerPROC.stdin.flush()
				print("Jumped-Backward --> 10 seconds")
			elif size == 2:
				self.PlayerPROC.stdin.write(k_DOWN)
				self.PlayerPROC.stdin.flush()
				print("Jumped-Backward --> 1 minute")
			elif size == 3:
				self.PlayerPROC.stdin.write(k_PGDWN)
				self.PlayerPROC.stdin.flush()
				print("Jumped-Backward --> 10 minutes")



pI = 0
while pI < workingPlaylistLEN:
	wURL = api.get_stream_url( workingPLAYLISTSongIDs[pI] , api.android_id , 'hi' )
	nowPlaying = mplayerHandler();
	nowPlaying.startPlayerPROC(wURL)
	inputHandler = RaspiInputHandler(nowPlaying)
	print("done with song")
	pI = pI + 1



