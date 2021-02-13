import base64
from Crypto.Cipher import AES
from Crypto import Random

BS = AES.block_size
pad = (lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS))
unpad = (lambda s: s[:-ord(s[len(s)-1:])])

def decryptMessage(encmsg, key, iv) :
	obj = AES.new(pad(key), AES.MODE_CBC, iv)
	return unpad(obj.decrypt(encmsg))

def encryptMessage(msg, key, iv) :
	obj = AES.new(pad(key), AES.MODE_CBC, iv)
	return obj.encrypt(pad(msg))

def createRandomIV() :
	return Random.new().read(AES.block_size)

def loadConfig(filepath, key=None, iv=None) :
	ret = []
	with open(filepath, 'r') as f:
		lines = f.readlines()

	for msg in lines :
		enc = base64.b64decode(msg)
		if key is not None and iv is not None :
			dec = decryptMessage(enc, key, iv)
		else :
			dec = enc
		ret.append(dec.decode('utf-8'))

	return ret

def saveConfig(filepath, array_message, key=None, iv=None) :
	ret = []
	for msg in array_message :
		if key is not None and  iv is not None :
			enc = encryptMessage(msg, key, iv)
		else :
			enc = msg.encode()
		ret.append(base64.b64encode(enc).decode() + "\n")
	with open(filepath, 'w') as f:
		f.writelines(ret)


if __name__ == '__main__':
	key = 'MyKey'
	iv = createRandomIV()
	print(iv)
	saveConfig('sample.cfg', ['hello', 'my', 'world'], key, iv)
	saveConfig('sample.dat', [base64.b64encode(iv).decode(), ])

	ivPrev = base64.b64decode(loadConfig('sample.dat')[0])
	myConfig = loadConfig('sample.cfg', key, ivPrev)
	
	print(myConfig)