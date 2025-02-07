import json
from flask import Response
from requests.models import Response as RequestsResponse


def flask_error_response(msg, code=500, error_type='InternalFailure'):
    result = {
        'Type': 'User' if code < 500 else 'Server',
        'message': msg,
        '__type': error_type
    }
    headers = {'x-amzn-errortype': error_type}
    # Note: don't use flask's make_response(..) or jsonify(..) here as they
    # can lead to "RuntimeError: working outside of application context".
    return Response(json.dumps(result), status=code, headers=headers)


def requests_response(content, status_code=200, headers={}):
    resp = RequestsResponse()
    content = json.dumps(content) if isinstance(content, dict) else content
    resp._content = content
    resp.status_code = status_code
    resp.headers = headers
    return resp


def flask_to_requests_response(r):
    return requests_response(r.data, status_code=r.status_code, headers=r.headers)


def requests_to_flask_response(r):
    return Response(r.content, status=r.status_code, headers=dict(r.headers))
