from tqdm import tqdm
import requests

import os

class LocalGManager:

	def __init__(self):

		self.a = None

	def download( self , directoryPATH , fileName , wURL ):

		if not os.path.exists( directoryPATH ):
			os.makedirs(directoryPATH)

		response1 = requests.get( wURL , stream=True )
		
		with open( os.path.join( directoryPATH , fileName )  , 'wb' ) as f:
			for data in tqdm( response1.iter_content(chunk_size=524288) ):
				f.write(data)



