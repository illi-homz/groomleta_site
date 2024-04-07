from .sms_sender import *

def create_response(resp):
    return {
        'status': 'success' if resp.ok else 'error',
        'code': resp.status_code,
        'ok': resp.ok
    }
