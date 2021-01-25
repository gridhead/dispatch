"""
##########################################################################
*
*   Copyright © 2019-2021 Akashdeep Dhar <t0xic0der@fedoraproject.org>
*
*   This program is free software: you can redistribute it and/or modify
*   it under the terms of the GNU General Public License as published by
*   the Free Software Foundation, either version 3 of the License, or
*   (at your option) any later version.
*
*   This program is distributed in the hope that it will be useful,
*   but WITHOUT ANY WARRANTY; without even the implied warranty of
*   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
*   GNU General Public License for more details.
*
*   You should have received a copy of the GNU General Public License
*   along with this program.  If not, see <https://www.gnu.org/licenses/>.
*
##########################################################################
"""

import json

from base64 import b64encode, b64decode

import click
import falcon
from falcon import __version__ as flcnvers
from werkzeug import __version__ as wkzgvers
from werkzeug import serving
from Crypto.PublicKey import RSA


class LiveUpdatingEndpoint(object):
    def __init__(self, passcode):
        self.passcode = passcode

    def on_post(self, rqst, resp):
        print(rqst.media)
        retnjson = {"retnmesg": "deny"}
        resp.body = json.dumps(retnjson, ensure_ascii=False)
        resp.status = falcon.HTTP_200


class PullPublicKeyFromClient(object):
    def on_post(self, rqst, resp):
        print(rqst.media)


class PushPublicKeyFromServer(object):
    def __init__(self, pairsize=2048):
        self.keyepair = RSA.generate(pairsize)

    def on_post(self, rqst, resp):
        pblcbyte = self.keyepair.publickey().export_key()
        pblcstrg = b64encode(pblcbyte).decode()
        retnjson = {"pblckeye": pblcstrg}
        resp.body = json.dumps(retnjson, ensure_ascii=False)
        resp.status = falcon.HTTP_200


main = falcon.API()


@click.command()
@click.option("-p", "--portdata", "portdata", help="Set the port value [0-65536].", default="6969")
@click.option("-6", "--ipprotv6", "netprotc", flag_value="ipprotv6", help="Start the server on an IPv6 address.")
@click.option("-4", "--ipprotv4", "netprotc", flag_value="ipprotv4", help="Start the server on an IPv4 address.")
@click.version_option(version="0.0.storage synonyms1", prog_name=click.style("Dispatch Server", fg="magenta"))
def mainfunc(portdata, netprotc):
    try:
        click.echo(" * " + click.style("Dispatch Server v0.0.1", fg="green"))
        netpdata = ""
        passcode = "12345678"
        if netprotc == "ipprotv6":
            click.echo(" * " + click.style("IP version       ", fg="magenta") + ": " + "6")
            netpdata = "::"
        elif netprotc == "ipprotv4":
            click.echo(" * " + click.style("IP version       ", fg="magenta") + ": " + "4")
            netpdata = "0.0.0.0"
        click.echo(" * " + click.style("Passcode         ", fg="magenta") + ": " + passcode + "\n" +
                   " * " + click.style("Reference URI    ", fg="magenta") + ": " + "http://" + netpdata + ":" + portdata + "/" + "\n" +
                   " * " + click.style("Endpoint service ", fg="magenta") + ": " + "Falcon v" + flcnvers + "\n" +
                   " * " + click.style("HTTP server      ", fg="magenta") + ": " + "Werkzeug v" + wkzgvers)
        livesync = LiveUpdatingEndpoint(passcode)
        putpbkey = PushPublicKeyFromServer(2048)
        getpbkey = PullPublicKeyFromClient()
        main.add_route("/livesync/", livesync)
        main.add_route("/putpbkey/", putpbkey)
        main.add_route("/getpbkey/", getpbkey)
        serving.run_simple(netpdata, int(portdata), main)
    except Exception as expt:
        click.echo(" * " + click.style("Error occurred   : " + str(expt), fg="red"))


if __name__ == "__main__":
    mainfunc()
