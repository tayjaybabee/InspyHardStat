from inspy_hard_stat.ihs_lib.libre_hw_monitor.config import Config
import requests
from requests.auth import HTTPBasicAuth
from requests import ReadTimeout

CONFIG = Config()


def authentication(user_name, password):
    """
    Authenticate with the HTTP server using the given username and password.

    Parameters:
        user_name (str):
            The username to authenticate with.

        password:
            The password to authenticate with.

    Returns:
        HTTPBasicAuth:
            An object that can be used to authenticate with the HTTP server.`
    """
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
