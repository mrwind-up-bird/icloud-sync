## icloud sync
## author: mrwindup-bird <oliver.baer@gmail.com>

import os
import logging
import http.client as http_client
import requests
from classes.color import color
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

http_client.HTTPConnection.debuglevel = 1

print(f'{color.OKGREEN}### iCloud Sync (icloud-sync){color.ENDC}')

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True

load_dotenv()

client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')
client_secret_value = os.getenv('CLIENT_SECRET_VALUE')
tenant = os.getenv('TENANT', 'common')
user_id = os.getenv('USER_ID')  # The user ID for the OneDrive user
scope = 'https://graph.microsoft.com/.default'

authority_url = f'https://login.microsoftonline.com/{tenant}'
token_url = f'https://login.microsoftonline.com/{tenant}/oauth2/v2.0/token'
onedrive_api_url = f'https://graph.microsoft.com/v1.0/users/{user_id}/drive/root/children'

print(f'{color.OKCYAN}Client ID: {client_id}')
print(f"Client Secret: {client_secret}")
print(f'Authority URL: {authority_url}')
print(f'Token URL: {token_url}')
print(f'Scope: {scope}')
print(f'OneDrive API URL: {onedrive_api_url}{color.ENDC}')

if not client_id or not client_secret or not user_id:
    raise ValueError("Client ID, Client Secret, and User ID must be provided.")

icloud_folder = os.path.expanduser('~/iCloud')

auth = HTTPBasicAuth(client_id, client_secret_value)
data = {
    'grant_type': 'client_credentials',
    'scope': scope
}
response = requests.post(token_url, data=data, auth=auth)

if response.status_code != 200:
    print(f"Error fetching token: {response.text}")
    exit(1)

token = response.json()
access_token = token['access_token']
print(f'{color.OKGREEN}Access Token: {access_token}{color.ENDC}')

headers = {
    'Authorization': f'Bearer {access_token}',
    'Accept': 'application/json'
}

response = requests.get(onedrive_api_url, headers=headers)
print(f'{color.FAIL}OneDrive Response: {response.content}{color.ENDC}')

try:
    response.raise_for_status()
except requests.exceptions.HTTPError as e:
    print(f"Error: {e}")
    if response.status_code == 401:
        print("Unauthorized: Check your credentials and token scopes.")
    elif response.status_code == 400:
        print("Bad Request: Check the endpoint and permissions.")
    exit(1)

files = response.json().get('value', [])

for file in files:
    download_url = file['@microsoft.graph.downloadUrl']
    file_name = file['name']
    file_path = os.path.join(icloud_folder, file_name)

    file_response = requests.get(download_url)

    with open(file_path, 'wb') as f:
        f.write(file_response.content)

    print(f'{file_name} successfully copied in {icloud_folder}.')
