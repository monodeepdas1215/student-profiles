import datetime
import json

import flask as flask
from flask import Response


class CustomJSONEncoder(flask.json.JSONEncoder):

    def default(self, o):
        if isinstance(o, (datetime.datetime, datetime.date)):
            return o.isoformat()
        elif isinstance(o, bytes):
            return o.decode("utf-8")
        return super().default(o)


def jsonify(*args, **kwargs):
    """ jsonify with support for bytes
    """
    return Response(json.dumps(dict(*args, **kwargs), cls=CustomJSONEncoder), mimetype='application/json')