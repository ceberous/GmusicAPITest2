from tqdm import tqdm
import requests

from pygame import mixer
import os


class LocalGManager:

	def __init__(self):

		self.a = None
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

		# enter into Raspi-Input / Containment Loop
		# For now , just emulate by waiting for song to be over
		while mixer.music.get_busy() == True:
			continue



