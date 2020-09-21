import requests, hashlib, click, json, base64


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
            click.echo("[ ! ] " + str(expt))
            return -1

    def sendfile(self):
        try:
            respobjc = requests.post("http://[" + self.targetpc + "]:" + self.recvport + "/recvfile/", files={"files": open(self.filename, "rb")})
            if respobjc.status_code == 200 and respobjc.json()["respcode"] == "donesend":
                return 0
            else:
                return 1
        except Exception as expt:
            click.echo("[ ! ] " + str(expt))
            return -1

    def connrecv(self):
        try:
            respobjc = requests.get("http://[" + self.targetpc + "]:" + self.recvport + "/connsend/", json={"password": self.password})
            if respobjc.status_code == 200 and respobjc.json()["passhash"] == self.passhash:
                return 0
            else:
                return 1
        except Exception as expt:
            click.echo("[ ! ] " + str(expt))
            return -1


@click.command()
@click.option("-f", "--filename", "filename", help="Set the filename that you wish to send", required=True)
@click.option("-c", "--joincode", "joincode", help="Set the invite code for connecting to receiver", required=True)
@click.version_option(version="21092020", prog_name="Dispatch SEND")
def mainfunc(filename:str, joincode:str):
    try:
        click.clear()
        genrdict = json.loads(base64.b64decode(joincode.encode("ascii")).decode("ascii"))
        click.echo("[ ! ] You are now connecting to " + genrdict["username"] + "'s device")
        connobjc = connclss(filename, genrdict["ipv6addr"], genrdict["portrecv"], "password")
        if connobjc.connrecv() == 0:
            click.echo("[1/3] Receiver legitimacy verified! Transferring file...")
            if connobjc.sendfile() == 0:
                click.echo("[2/3] File transfer complete! Sending file hash...")
                if connobjc.sendhash() == 0:
                    click.echo("[3/3] File integrity verified at receiver's end!")
                else:
                    click.echo("[ ! ] File integrity verification failed")
            else:
                click.echo("[ ! ] File transfer failed")
        else:
            click.echo("[ ! ] Receiver legitimacy could not be verified")
    except Exception as expt:
        click.echo("Sender had to exit due to the following exception" + "\n" + str(expt))


if __name__ == "__main__":
    mainfunc()