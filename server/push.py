import json

import falcon

from hashlib import sha256


class CheckReachability(object):
    def on_post(self, rqst, resp):
        retnjson = {
            "retnmesg": "connconf",
            "timehash": sha256(rqst.media["timestmp"].encode()).hexdigest()
        }
        resp.body = json.dumps(retnjson, ensure_ascii=False)
        resp.status = falcon.HTTP_200
