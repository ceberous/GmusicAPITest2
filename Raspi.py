import sys , select , tty , termios

import psutil

import os
import subprocess
import threading
import time

# Raspi Input Setup
# ==============================================================
#import Rpi.GPIO as GPIO

#GPIO.setmode( GPIO.BCM )
#GPIO.setup( 23 , GPIO.IN , pull_up_down=GPIO.PUD_UP )
#GPIO.setup( 24 , GPIO.IN , pull_up_down=GPIO.PUD_DOWN )

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
