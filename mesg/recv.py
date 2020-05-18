from flask import Flask, request

main = Flask(__name__)

@main.route("/recvmesg/", methods=["GET"])
def recvmesg():
    if request.method == "GET":
        jsondata = request.get_json()
        sendernm = jsondata["sendernm"]
        subjtext = jsondata["subjtext"]
        conttext = jsondata["conttext"]
        print("[MESSAGE RECEIVED]" + "\n" + \
              "SENDER NAME : " + str(sendernm) + "\n" + \
              "SUBJECT     : " + str(subjtext) + "\n" + \
              "CONTENT     : " + str(conttext))
        respdata = {
            "code": 69420,
            "mesg": "Message sent successfully"
        }
        return respdata

if __name__ == "__main__":
    main.run(port=9696, host="::")