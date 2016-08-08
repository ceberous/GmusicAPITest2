import os
import subprocess


class mplayerHandler:

	def __init__(self):
		self.PlayerPROC = None
		
	def startPlayerPROC( self , url ):
		#print(url)
		#self.PlayerPROC = subprocess.Popen( [ "/usr/bin/mplayer" , url ] , stdin=subprocess.PIPE , stdout=subprocess.PIPE , stderr=subprocess.PIPE )
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
