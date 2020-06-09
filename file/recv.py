from flask import Flask, request

main = Flask(__name__)

@main.route("/recvarch/", methods=["POST"])
def recvarch():
    if request.method == "POST":
        f = request.files["files"]
        print(f)
        respjson = {
            "respcode": "donesend"
        }
        return respjson

if __name__ == "__main__":
    main.run(port=9696, host="::")