from os import environ
from base64 import b64encode
from requests import post, get

def get_auth(r):
    api_key = environ.get("API_KEY")
    api_key_secret = environ.get("API_KEY_SECRET")

    keys = api_key + ':' + api_key_secret
    keys = keys.encode('ascii')
    
    auth = b64encode(keys).decode('ascii')

    r.headers["Host"] = "api.twitter.com"
    r.headers["Authorization"] = f"Basic {auth}"
    r.headers["Content-type"]  = "application/x-www-form-urlencoded;charset=UTF-8"
    return r

def get_bearer_token():
    response = post('https://api.twitter.com/oauth2/token', auth=get_auth,data={'grant_type':'client_credentials'})
    return response.json()['access_token']

def app_only_auth(r):
    bearer_token = get_bearer_token()
    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "Search-bot v1.0"
    return r

def connect_to_endpoint(url, params):
    response = get(url, auth=app_only_auth, params=params)
    if response.status_code != 200:
        # logging.error(response.text)
        raise Exception(response.status_code, response.text)
    return response.json()


