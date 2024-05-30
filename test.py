## icloud sync
## author: mrwindup-bird <oliver.baer@gmail.com>

import os
import logging
import http.client as http_client
import requests
import msal
from classes.color import color
from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import BackendApplicationClient
from dotenv import load_dotenv
from var_dump import var_dump

http_client.HTTPConnection.debuglevel = 1

print (f'{color.OKGREEN}### iCloud Sync (icloud-sync){color.ENDC}')

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True

load_dotenv()

client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')
tenant = os.getenv('TENANT', 'consumers')
scope = os.getenv('SCOPE','Files.Read,Files.ReadWrite,Files.ReadAll')

token_url = f'https://login.microsoftonline.com/{tenant}/oauth2/v2.0/token'
authorize_url = f'https://login.microsoftonline.com/{tenant}'
onedrive_api_url = 'https://graph.microsoft.com/v1.0/drive/root/children'
scope_uri = [os.getenv('SCOPE_URI', 'https://graph.microsoft.com/.default')]

endpoint_uri = os.getenv('ENDPOINT_URI')

print(f'{color.OKCYAN}Client ID: {client_id}')
print(f"Client Secret: {client_secret}")
print(f'Token URL: {token_url}')
print(f'Scope URI: {scope_uri}')
print(f'Scope: {scope}{color.ENDC}')

if not client_id or not client_secret:
    raise ValueError("Neither Client ID nor Client Secret given.")

icloud_folder = os.path.expanduser('~/iCloud')

app = msal.ConfidentialClientApplication(client_id, authority=authorize_url, client_credential=client_secret)

result = None
result = app.acquire_token_silent(scope, account=None)

if not result:
    print(f'{color.WARNING}No Token found! Aquiring from Azure AD. Scope: {scope_uri}{color.ENDC}')
    result = app.acquire_token_for_client(scopes=scope_uri)

if "access_token" in result:
    response = requests.get(endpoint_uri,headers={'Authorization': 'Bearer ' + result['access_token']}, )
    graph_data = response.json()

    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print (f'{color.WARNING}Error loading GraphData: {e}{color.ENDC}')

    print(f'{color.OKGREEN}Users from graph: {str(graph_data)}{color.ENDC}')
else:
    print(result.get("error"))
    print(result.get("error_description"))
    print(result.get("correlation_id"))  # You may need this when reporting a bug





#response = requests.get(f'{authorize_url}?client_id={client_id}&scope={scope}&response_type=token&redirect_uri=http://localhost/oauth')
#print (response.content)