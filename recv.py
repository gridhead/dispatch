from flask import Flask, request

main = Flask(__name__)

@main.route("/recvarch/", methods=["GET"])
def sendarch():
    if request.method == "GET":
        jsondata = request.get_json()
        filename = jsondata["filename"]
        actifile = jsondata["actifile"]
        print(filename, len(actifile))
        retndata = {
            "notecode": "File " + filename + " has been successfully received!",
        }
        return retndata

if __name__ == "__main__":
    main.run(port=9696, host="0.0.0.0")
