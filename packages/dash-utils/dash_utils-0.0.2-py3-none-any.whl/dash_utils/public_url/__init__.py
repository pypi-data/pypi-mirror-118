import logging
import requests

def public_url(url: str):
    response = requests.get(url)

    if response.status_code != 200:
        logging.error(f'bad response ({response.status_code}) from {url}')
        return 'bad response, see logs', 400

    return response.json()
