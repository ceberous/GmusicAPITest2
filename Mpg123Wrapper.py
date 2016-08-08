import os , subprocess , signal , select , tty , sys , termios , psutil ,time 

homeDIR = os.path.expanduser("~") 
libDIR = homeDIR + "/GMusicLocalLibrary/"

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

def handleInput(nowPlaying):

	with NonBlockingConsole() as nbc:
		while True:
			c = nbc.get_data()
			if c:
				try:
					print(c)
					if c == '\x1b': # escape key
						#nowPlaying.killPlayerPROC()
						os.kill(nowPlaying.pid , signal.SIGKILL )
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
					if psutil.pid_exists(nowPlaying.pid):
						print("mplayer process must of closed")
						os.kill(nowPlaying.pid , signal.SIGKILL )
						return	
					else:
						print("unknown problem ... still continuing")
						pass


def launchMPG123Player( filePATH ):
	dest = os.path.join( os.getcwd() , "mpg123OUT.txt"  )
	mpg123OUT = open( dest , 'r+')
	mPlayer = subprocess.Popen( [ "/usr/bin/mpg123" , filePATH ] , stdin=subprocess.PIPE , stdout=mpg123OUT , stderr=subprocess.PIPE )
	print(mPlayer.pid)
	handleInput(mPlayer)


#test1 = '/home/morpheous/GMusicLocalLibrary/EDM/Tduhofo3sqnkmlag6i5uldj5oui.mp3'
#launchMPG123Player( test1 )