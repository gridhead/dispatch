import requests

targetpc = "http://localhost:9696/recvarch/"

targetpc = "http://[2409:4042:2396:2f42:9387:22e4:aa39:af0e]:9696/recvarch/"

def sendarch(filename):
    files = {'files': open(filename, 'rb')}
    r = requests.post(targetpc, files=files)
    print(r.text)

if __name__ == "__main__":
    filename = str(input("Enter the filename "))
    sendarch(filename)