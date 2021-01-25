import json
from Crypto.PublicKey import RSA
from base64 import b64encode
from click import echo, style


class HandlingHostData(object):
    def __init__(self, hostdata):
        echo(style("      Handling host data", fg="bright_magenta"))
        self.hostencd = b64encode(hostdata.encode()).decode()
        echo("(1/4) Generating a 2048-bit RSA keypair")
        self.keyepair = RSA.generate(2048)
        echo("(2/4) Exporting public key")
        self.pblcbyte = self.keyepair.publickey().export_key()
        self.pblcstrg = b64encode(self.pblcbyte).decode()
        echo("(3/4) Exporting private key")
        self.prvtbyte = self.keyepair.export_key()
        self.prvtstrg = b64encode(self.prvtbyte).decode()

    def save_host_data(self):
        hostjson = json.dumps(
            {
                "hostname": self.hostencd,
                "prvtkeye": self.prvtstrg,
                "pblckeye": self.pblcstrg,
            }
        )
        with open("hostdata.b64e", "w") as fileobjc:
            fileobjc.write(hostjson)

    def interface_provision(self):
        try:
            echo("(4/4) Saving host data to local storage")
            self.save_host_data()
            echo(style("      Hostname was saved successfully!", fg="green"))
        except:
            echo(style(" > Hostname could not be saved!", fg="red"))
