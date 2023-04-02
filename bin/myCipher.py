from passlib.hash import pbkdf2_sha256
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from base64 import b64encode, b64decode
import hashlib
import jsonFunctions

def encryptAES_CBC(string, key):
	string = string.encode()
	key = hashlib.sha256(key.encode()).digest()
	cipher = AES.new(key, AES.MODE_CBC)
	ct_bytes = cipher.encrypt(pad(string, AES.block_size))
	ct = b64encode(ct_bytes).decode()
	iv = b64encode(cipher.iv).decode()
	return "$aes-cbc$" + iv + "$" + ct

def decryptAES_CBC(string, key):
	try:
		s = string.split("$")
		iv = b64decode(s[-2])
		ct = b64decode(s[-1])
		key = hashlib.sha256(key.encode()).digest()
		cipher = AES.new(key, AES.MODE_CBC, iv)
		pt = unpad(cipher.decrypt(ct), AES.block_size)
		return pt.decode()
	except:
		return None

def encryptAES_GCM(string, key):
	string = string.encode()
	key = hashlib.sha256(key.encode()).digest()
	encobj = AES.new(key, AES.MODE_GCM)
	ciphertext, authTag = encobj.encrypt_and_digest(string)
	ciphertext = b64encode(ciphertext).decode()
	authTag = b64encode(authTag).decode()
	nonce= b64encode(encobj.nonce).decode()
	return "$aes-gcm$" + nonce + "$" + authTag + "$" + ciphertext

def decryptAES_GCM(string, key):
	key = hashlib.sha256(key.encode()).digest()
	s = string.split("$")
	cipher = b64decode(s[-1])
	authTag = b64decode(s[-2])
	nonce = b64decode(s[-3])
	encobj = AES.new(key,  AES.MODE_GCM, nonce)
	return encobj.decrypt_and_verify(cipher, authTag).decode()

def encryptMethod(string, key, encMethod):
	if encMethod == "aes-gcm":
		return encryptAES_GCM(string, key)
	elif encMethod == "aes-cbc":
		return encryptAES_CBC(string, key)
	else:
		return "Error. Encryption method not found :("

def encrypt(string, key):
	encMethod = jsonFunctions.openSettingsData()["security"]["encryptionMethodUsed"]
	if encMethod == "aes-gcm":
		return encryptAES_GCM(string, key)
	elif encMethod == "aes-cbc":
		return encryptAES_CBC(string, key)
	else:
		return "Error. Encryption method not found :("	

def decrypt(string, key):
	s = string.split("$")
	if s[1] == "aes-gcm":
		return decryptAES_GCM(string, key)
	elif s[1] == "aes-cbc":
		return decryptAES_CBC(string, key)
	else:
		return "ERROR"

def pbkdf2(string):
	pbkdf2 = pbkdf2_sha256.using(rounds=310000)
	return pbkdf2.hash(string)

def pbkdf2_verify(psw, hash):
	pbkdf2 = pbkdf2_sha256.using(rounds=310000)
	return pbkdf2.verify(psw, hash)

def identityCheck(psw):
	j = jsonFunctions.openAccountsData()
	h = j["key"]
	return pbkdf2_verify(psw, h)

def decryptAll(psw):
	j = jsonFunctions.openAccountsData()
	accounts = j["accountDetails"]
	for a in accounts:
		a["password"] = decrypt(a["password"], psw)
	return accounts
