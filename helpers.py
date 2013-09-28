from flask import Response
import json

def json_response(jsonable):
    return Response(json.dumps(jsonable), mimetype='application/json')
