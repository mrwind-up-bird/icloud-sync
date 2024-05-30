## icloud sync
## author: mrwindup-bird <oliver.baer@gmail.com>

import requests
import logging
import os
from dotenv import load_dotenv

load_dotenv()

print ('"\33[38;5;41m"### Refresh Token (icloud-sync)')

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True


client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET_VALUE')
refresh_token = os.getenv('CLIENT_REFRESH_TOKEN')
tenant = os.getenv('TENANT','consumers')

token_url = f'https://login.microsoftonline.com/{tenant}/oauth2/v2.0/token'

scopes = ["https://graph.microsoft.com/.default"]

token_data = {
    'grant_type': 'client_credentials',
    'client_id': client_id,
    'client_secret': client_secret,
    'scope': ' '.join(scopes),
}

token_r = requests.post(token_url, data=token_data)
token = token_r.json().get('access_token')

print (f'"\33[38;5;120m"Token: {token}')

data = {
    'grant_type': 'refresh_token',
    'client_id': client_id,
    'client_secret': client_secret,
    'refresh_token': refresh_token,
    'scope': 'https://graph.microsoft.com/.default'
}

print (f'"\33[38;5;86m"Data Array: ClientID: {client_id}, ClientSecret: {client_secret}, RefreshToken: {refresh_token}, Tenant: {tenant}')

response = requests.post(token_url, data=data)
response.raise_for_status()

if response.status_code == 200:
    tokens = response.json()
    new_access_token = tokens['access_token']
    print(f'New access token: {new_access_token}')
else:
    print(f'Token request failed with status code {response.status_code}')
    print(response.text)
