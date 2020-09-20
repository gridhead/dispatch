import requests, hashlib

targetpc = "http://localhost:9696/recvarch/"

targetpc = "http://[2409:4042:2396:2f42:9387:22e4:aa39:af0e]:9696/recvarch/"

def sendhash(filename, targetpc):
    try:
        hash = hashlib.sha512(open(filename, "rb").read()).hexdigest()
        objc = requests.get("http://[" + targetpc + "]:9696/filechek/", json={"name": filename + ".bak", "hash": hash})
        if objc.status_code == 200:
            if objc.json()["respcode"] == "verified":
                print("[3/3] File integrity verified at receiver's end!")
            else:
                print("Integrity verification failed")
        else:
            print("Receiver is facing errors")
    except Exception as expt:
        print("Exception " + str(expt) + " has taken place")


def sendarch(filename, targetpc):
    file = {"files": open(filename, "rb")}
    r = requests.post("http://[" + targetpc + "]:9696/recvarch/", files=file)
    if r.json()["respcode"] == "donesend":
        print("[2/3] File transfer complete! Sending file hash...")
        sendhash(filename, targetpc)


def connrecv(filename, targetpc):
    try:
        safetext = "password"
        objc = requests.get("http://[" + targetpc + "]:9696/connsend/", json={"password": safetext})
        if objc.status_code == 200:
            if objc.json()["hash"] == hashlib.sha512(safetext.encode("utf8")).hexdigest():
                print("[1/3] Receiver legitimacy verified! Transferring file...")
                sendarch(filename, targetpc)
            else:
                print("Verification failed")
        else:
            print("Receiver is facing errors")
    except Exception as expt:
        print("Exception " + str(expt) + " has taken place")


if __name__ == "__main__":
    connrecv(str(input("Enter the filename ")), str(input("Enter the destination PC address ")))
