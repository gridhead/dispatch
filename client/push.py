import json
from Crypto.PublicKey import RSA
from base64 import b64encode
from click import echo, style


class PushingFilesToServer(object):
    def __init__(self, pushdata):
        self.pushdata = pushdata
        self.hostname = None

    def check_if_host_data_is_available(self):
        try:
            with open("hostdata.b64e", "r") as fileobjc:
                hostdata = fileobjc.read()
            hostname = json.loads(hostdata)["hostname"]
            print(hostname)
            return True
        except json.decoder.JSONDecodeError:
            echo(style("      Error occurred : Invalid hostdata detected", fg="red"))
        except FileNotFoundError:
            echo(style("      Error occurred : Hostdata was not exported", fg="red"))
        except Exception as expt:
            echo(style("      Error occurred : " + str(expt), fg="red"))
            return False

    def check_if_host_name_is_reachable(self):
        pass

    def check_if_file_exists(self):
        pass

    def check_file_size(self):
        pass

    def request_public_key(self):
        pass

    def encrypt_file(self):
        pass

    def interface_provision(self):
        if self.check_if_host_data_is_available():
            print("Yey")
