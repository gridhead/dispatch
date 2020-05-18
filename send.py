import requests

targetpc = "localhost:9696"

def sendfile(filename):
    actifile = open(filename,"rb")
    data = {
        "filename": filename,
        "actifile": actifile,
    }
    rqst = requests.get(targetpc, json=data)
    print(rqst.json())