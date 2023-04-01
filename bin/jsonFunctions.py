import json
import myCipher

accountsPath = "data/accounts.json"
optionsPath = "data/options.json"
settingsPath = "data/settings.json"

def openOptionsData():
	f = open(optionsPath)
	j = json.load(f)
	f.close()
	return j

def openSettingsData():
	f = open(settingsPath)
	j = json.load(f)
	f.close()
	return j

def updateSettingsData(data):
	f = open(settingsPath, "w")
	json.dump(data, f)
	f.close()

def openAccountsData():
	f = open(accountsPath)
	j = json.load(f)
	f.close()
	return j

def createAccountsData(k):
	data = {"key":k,"accountDetails":[]}
	f = open(accountsPath, "w")
	json.dump(data, f)
	f.close()

def updateAccountsData(data):
	f = open(accountsPath, "w")
	json.dump(data, f)
	f.close()

def updateKey(oldKey, newKey):
	data = openAccountsData()
	for a in data["accountDetails"]:
		psw = myCipher.decrypt(a["password"], oldKey)
		method = a["password"].split("$")[1]
		a["password"] = myCipher.encryptMethod(psw, newKey, method)
	data["key"] = myCipher.pbkdf2(newKey)
	updateAccountsData(data)

def updatePswEncMethod(a, key):
	psw = myCipher.decrypt(a["password"], key)
	a["password"] = encrypt(psw, key)
	updateAccount(a)

def addAccount(a):
	data = openAccountsData()
	data["accountDetails"].append(a)
	updateAccountsData(data)

def updateAccount(a):
	data = openAccountsData()
	for i in range(0,len(data["accountDetails"])):
		if data["accountDetails"][i]["id"] == a["id"]:
			data["accountDetails"][i] = a
			updateAccountsData(data)
			return

def deleteAccount(a):
	data = openAccountsData()
	data["accountDetails"].remove(a)
	updateAccountsData(data)