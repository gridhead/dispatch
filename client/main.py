from urllib3 import PoolManager
from base64 import b64encode, b64decode
import json, click
from Crypto.PublicKey import RSA
from click import echo, style

import host, push


class Connexon():
    def __init__(self, hostaddr):
        self.httpobjc = PoolManager()
        self.hostaddr = hostaddr
        echo(" * Generating a 2048-bit RSA keypair...")
        self.keyepair = RSA.generate(2048)

    def send_rsa_public_key(self):
        echo(" * Conveying public key ...")
        pblcbyte = self.keyepair.publickey().export_key()
        pblcstrg = b64encode(pblcbyte).decode()
        retnjson = {"pblckeye": pblcstrg}
        rqstobjc = self.httpobjc.request("POST", self.hostaddr + "getpbkey", retnjson)
        pblcbyte = json.loads(rqstobjc.data.decode())["pblckeye"].encode()
        pblcstrg = b64decode(pblcbyte).decode()

    def fetch_rsa_public_key(self):
        echo(" * Receiving public key ...")
        rqstobjc = self.httpobjc.request("POST", self.hostaddr + "putpbkey")
        pblcbyte = json.loads(rqstobjc.data.decode())["pblckeye"].encode()
        pblcstrg = b64decode(pblcbyte).decode()

    def process_cycle(self):
        self.send_rsa_public_key()
        self.fetch_rsa_public_key()


class PullingFilesToClient(object):
    def __init__(self, pulldata):
        self.pulldata = pulldata

    def interface_provision(self):
        pass


@click.command()
@click.option("-h", "--host", "hostdata", help="Set the host location.", default=None)
@click.option("-s", "--push", "pushdata", help="Push a file securely to the server.", default=None)
@click.option("-r", "--pull", "pulldata", help="Pull a file securely from the server.", default=None)
@click.version_option(version="0.0.1", prog_name=click.style("Dispatch Client", fg="magenta"))
def mainfunc(hostdata, pushdata, pulldata):
    if hostdata:
        echo(style("      Dispatch Client v0.0.1", fg="cyan", bold=True))
        host.HandlingHostData(hostdata).interface_provision()
    elif pushdata:
        echo(style("      Dispatch Client v0.0.1", fg="cyan", bold=True))
        push.PushingFilesToServer(pushdata).interface_provision()
    elif pulldata:
        echo(style("      Dispatch Client v0.0.1", fg="cyan", bold=True))
        PullingFilesToClient(pulldata).interface_provision()
    else:
        echo(
            style(" .-,--.                .      .   \n" +
                  " ' |   \ . ,-. ,-. ,-. |- ,-. |-. \n" +
                  " , |   / | `-. | | ,-| |  |   | | \n" +
                  " `-^--'  ' `-' |-' `-^ `' `-' ' ' \n" +
                  "        v0.0.1 | Client           \n",
                  fg="cyan", bold=True) + "\n" +
            style("Usage: ", bold=True) + style("main.py [OPTIONS]") + "\n" + "\n" +
            style("Options:", fg="bright_magenta", bold=True) + "\n" +
            style("  -h, --host TEXT  ", fg="magenta") + "Set the host location.\n" +
            style("  -s, --push TEXT  ", fg="magenta") + "Push a file securely to the server.\n" +
            style("  -r, --pull TEXT  ", fg="magenta") + "Pull a file securely from the server.\n" +
            style("  --version        ", fg="magenta") + "Show the version and exit.\n" +
            style("  --help           ", fg="magenta") + "Show this message and exit."
        )

if __name__ == "__main__":
    #connobjc = Connexon("http://localhost:6969/")
    #connobjc.process_cycle()
    mainfunc()