import requests, hashlib


class connclss():
    def __init__(self, filename:str, targetpc:str, recvport:str, password:str):
        self.filename = filename
        self.targetpc = targetpc
        self.recvport = recvport
        self.password = password
        self.filehash = hashlib.sha512(open(self.filename, "rb").read()).hexdigest()
        self.passhash = hashlib.sha512(password.encode("utf8")).hexdigest()

    def sendhash(self):
        try:
            respobjc = requests.get("http://[" + self.targetpc + "]:"  + self.recvport + "/filechek/", json={"filename": self.filename + ".bak", "filehash": self.filehash})
            if respobjc.status_code == 200 and respobjc.json()["respcode"] == "verified":
                return 0
            else:
                return 1
        except Exception as expt:
            print("[ ! ] " + str(expt))
            return -1

    def sendfile(self):
        try:
            respobjc = requests.post("http://[" + self.targetpc + "]:" + self.recvport + "/recvfile/", files={"files": open(self.filename, "rb")})
            if respobjc.status_code == 200 and respobjc.json()["respcode"] == "donesend":
                return 0
            else:
                return 1
        except Exception as expt:
            print("[ ! ] " + str(expt))
            return -1

    def connrecv(self):
        try:
            respobjc = requests.get("http://[" + self.targetpc + "]:" + self.recvport + "/connsend/", json={"password": self.password})
            if respobjc.status_code == 200 and respobjc.json()["passhash"] == self.passhash:
                return 0
            else:
                return 1
        except Exception as expt:
            print("[ ! ] " + str(expt))
            return -1


if __name__ == "__main__":
    connobjc = connclss("file.pkg", "2409:4042:483:f09e:9aa1:cac5:64cc:3984", "9696", "password")
    if connobjc.connrecv() == 0:
        print("[1/3] Receiver legitimacy verified! Transferring file...")
        if connobjc.sendfile() == 0:
            print("[2/3] File transfer complete! Sending file hash...")
            if connobjc.sendhash() == 0:
                print("[3/3] File integrity verified at receiver's end!")
            else:
                print("[ ! ] File integrity verification failed")
        else:
            print("[ ! ] File transfer failed")
    else:
        print("[ ! ] Receiver legitimacy could not be verified")