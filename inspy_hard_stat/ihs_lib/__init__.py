import requests
from requests.auth import HTTPBasicAuth
from inspy_hard_stat.ihs_lib.libre_hw_monitor.config import CONFIG
from inspy_hard_stat.config.utils import is_default_value
from prompt_toolkit.shortcuts.dialogs import input_dialog


HOST = CONFIG.host


def authentication_dialog():
    user_name = input_dialog(
        title="Authentication",
        text="Enter your username",
    ).run()

    password = input_dialog(
        title="Authentication",
        text="Enter your password",
        password=True
    ).run()

    return HTTPBasicAuth(user_name, password)


def authenticate_user(config=CONFIG):
    if is_default_value(config.user_name) or is_default_value(config.password):
        http_auth = authentication_dialog()
        config.user_name = http_auth.username
        config.password = http_auth.password
        config.save()
    else:
        from inspy_hard_stat.ihs_lib.libre_hw_monitor import authentication
        http_auth = authentication

    return http_auth




def request_data(url=HOST, port=CONFIG.port):
    url = f'{url}:{port}/data.json'

    http_auth = authentication_dialog()

    try:
        res = requests.get(url, auth=http_auth, timeout=5)
        res.raise_for_status()
    except requests.exceptions.ReadTimeout:
        print('Timeout error')

    return res
