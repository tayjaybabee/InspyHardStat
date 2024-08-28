from inspy_hard_stat.ihs_lib.libre_hw_monitor.config import Config
import requests
from requests.auth import HTTPBasicAuth
from requests import ReadTimeout

CONFIG = Config()


def authentication():

    user_name = CONFIG.user_name
    password = CONFIG.password

    return HTTPBasicAuth(user_name, password)

def request_data(url=None):

    if not url:
        url = f'{CONFIG.url}/data.json'


    try:

        res = requests.get(url, auth=authentication(), timeout=5)

        res.raise_for_status()
    except requests.exceptions.ReadTimeout:
        print('Timeout error')


    return res.json()
