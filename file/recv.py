from flask import Flask, request
import requests, hashlib, os, logging, click, json, base64


main = Flask(__name__)
loge = logging.getLogger("werkzeug")
loge.disabled = True


@main.route("/recvfile/", methods=["POST"])
def recvfile():
    try:
        if request.method == "POST":
            f = request.files["files"]
            click.echo(click.style(" * Transfer cached buffer to storage", fg="green"))
            f.save(f.filename+".bak")
            return {"respcode": "donesend"}
    except Exception as expt:
        return {"respcode": str(expt)}


@main.route("/connsend/", methods=["GET"])
def connsend():
    try:
        if request.method == "GET":
            click.echo(click.style(" * Identity proven to a sender", fg="green"))
            return {"passhash": hashlib.sha512(request.get_json()["password"].encode("utf8")).hexdigest()}
    except Exception as expt:
        return {"passhash": str(expt)}


@main.route("/filechek/", methods=["GET"])
def filechek():
    try:
        if request.method == "GET":
            if hashlib.sha512(open(request.get_json()["filename"], "rb").read()).hexdigest() == request.get_json()["filehash"]:
                os.system("mv " + request.get_json()["filename"] + " " + request.get_json()["filename"][:-4])
                click.echo(click.style(" * Cache integrity verified \n * Transfer complete", fg="green"))
                return {"respcode": "verified"}
            os.system("rm " + request.get_json()["filename"])
            return {"respcode": "verifail"}
    except Exception as expt:
        return {"respcode": str(expt)}


@click.command()
@click.option("-u", "--username", "username", help="Set the username to recognize with", required=True)
@click.option("-p", "--portrecv", "portrecv", help="Set the port value for the receiver end", required=True)
@click.version_option(version="21092020", prog_name="Dispatch RECV")
def mainfunc(username:str, portrecv:int):
    try:
        click.clear()
        ipv6addr = requests.get("https://ipv6.icanhazip.com/").text[:-1]
        click.echo(click.style(" * Welcome " + username + "!"))
        click.echo(click.style(" * Your IPv6 address is " + ipv6addr, fg="cyan"))
        click.echo(click.style(" * Your active port for receiving is " + str(portrecv), fg="cyan"))
        genrcode = base64.b64encode(json.dumps({"username": username, "ipv6addr": ipv6addr, "portrecv": portrecv}).encode("ascii")).decode("ascii")
        click.echo(" * Share this code to allow a sender to join " + "\n * " + click.style(genrcode, fg="cyan"))
        main.run(port=portrecv, host="::")
    except Exception as expt:
        click.echo(" * Receiver had to exit due to the following exception" + "\n * " + str(expt))


if __name__ == "__main__":
    mainfunc()