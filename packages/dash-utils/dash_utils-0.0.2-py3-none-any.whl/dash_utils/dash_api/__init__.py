import logging
import requests
import numpy as np
import google.auth.transport.requests
import google.oauth2.id_token

def gfunction_post(fn_url, params):
    auth_req = google.auth.transport.requests.Request()
    id_token = google.oauth2.id_token.fetch_id_token(auth_req, fn_url)
    response = requests.post(fn_url, headers={'Authorization': f'Bearer {id_token}'}, json=params)
    return response

def fn_api(url, params):
    response = gfunction_post(url, params)

    if response.status_code != 200:
        logging.error(f'bad response ({response.status_code}) from {url}')
        return 'populate error, see logs', response.status_code

    return 'populate complete', 200
