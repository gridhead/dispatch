import requests

targetpc = "http://localhost:9696/recvmesg/"

targetpc = "http://[2409:4042:2396:2f42:9387:22e4:aa39:af0e]:9696/recvmesg/"

def sendmesg(sendernm, subjtext, conttext):
    data = {
        "sendernm": sendernm,
        "subjtext": subjtext,
        "conttext": conttext,
    }
    rhea = requests.get(targetpc, json = data)
    print(rhea.json())

if __name__ == "__main__":
    sendernm = str(input("Enter your name                        : "))
    subjtext = str(input("Enter the subject of your conversation : "))
    conttext = str(input("Enter the content of your conversation : "))
    sendmesg(sendernm, subjtext, conttext)