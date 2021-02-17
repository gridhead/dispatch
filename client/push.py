import json, time
from Crypto.PublicKey import RSA
from base64 import b64encode, b64decode
from click import echo, style
import urllib3
from hashlib import sha256


httpobjc = urllib3.PoolManager()


class PushingFilesToServer(object):
    def __init__(self, pushdata):
        self.pushdata = pushdata
        self.hostname = None
        self.prvtkeye = None
        self.pblckeye = None
        self.filecont = None
        self.filesize = None

    def check_if_host_data_is_available(self):
        try:
            with open("hostdata.b64e", "r") as fileobjc:
                hostdata = fileobjc.read()
            echo("(1/5) Reading hostname")
            self.hostname = b64decode(json.loads(hostdata)["hostname"].encode()).decode()
            echo("(2/5) Importing private key")
            self.prvtkeye = b64decode(json.loads(hostdata)["prvtkeye"].encode()).decode()
            echo("(3/5) Importing public key")
            self.pblckeye = b64decode(json.loads(hostdata)["pblckeye"].encode()).decode()
            return True
        except json.decoder.JSONDecodeError:
            echo(style("      Error occurred : Invalid hostdata detected", fg="red"))
        except FileNotFoundError:
            echo(style("      Error occurred : Hostdata was not discovered", fg="red"))
        except Exception as expt:
            echo(style("      Error occurred : " + str(expt), fg="red"))
            return False

    def check_if_host_name_is_reachable(self):
        try:
            echo("(4/5) Attempting connection to host")
            timestmp = time.ctime()
            timeobjc = json.dumps({"timestmp": timestmp}).encode()
            rqstobjc = httpobjc.request(
                "POST",
                self.hostname + "pushfunc/pushrech",
                body=timeobjc
            )
            respjson = json.loads(rqstobjc.data.decode())
            if respjson["timehash"] == sha256(timestmp.encode()).hexdigest():
                return True
            else:
                echo(style("      Error occurred : Trust model could not be verified", fg="red"))
                return False
        except Exception as expt:
            echo(style("      Error occurred : Connection could not be established", fg="red"))
            return False

    def check_if_file_exists(self):
        echo("(5/5) Reading specified file")
        if "/" in self.pushdata:
            echo(style("      Error occurred : Relative directory detected", fg="red"))
            return False
        else:
            try:
                with open(self.pushdata, "rb") as fileobjc:
                    self.filecont = fileobjc.read()
                return True
            except FileNotFoundError as expt:
                echo(style("      Error occurred : Specified file could not be found", fg="red"))
                return False

    def check_file_size(self):
        echo("(6/5) Checking file size")
        self.filesize = len(self.filecont)
        if self.filesize <= 5242880:
            return True
        else:
            echo(style("      Error occurred : Filesize is beyond the provided limit", fg="red"))
            return False

    def request_public_key(self):
        try:
            echo("(7/5) Requesting public key from the host")
            pblcrqst = json.dumps({"identity": "DEADCAFE"}).encode()
            rqstobjc = httpobjc.request(
                "POST",
                self.hostname + "pushfunc/pushpblc",
                body=pblcrqst
            )
            respjson = json.loads(rqstobjc.data.decode())
        except Exception as expt:
            pass

    def encrypt_file(self):
        pass

    def convey_encrypted_file(self):
        pass

    def interface_provision(self):
        if self.check_if_host_data_is_available():
            if self.check_if_host_name_is_reachable():
                if self.check_if_file_exists():
                    if self.check_file_size():
                        print("Yey")
