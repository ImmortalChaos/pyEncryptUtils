import base64
from encutils import encfile

if __name__ == '__main__':
	key = 'MyKey'
	iv = encfile.createRandomIV()
	print(iv)
	encfile.saveConfig('sample.cfg', ['hello', 'my', 'world'], key, iv)
	encfile.saveConfig('sample.dat', [base64.b64encode(iv).decode(), ])

	ivPrev = base64.b64decode(encfile.loadConfig('sample.dat')[0])
	myConfig = encfile.loadConfig('sample.cfg', key, ivPrev)
	
	print(myConfig)