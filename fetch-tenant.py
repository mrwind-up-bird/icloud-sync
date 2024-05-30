import requests
import os
from dotenv import load_dotenv

print ('### Fetch Tenant (icloud-sync)')

tenant = os.getenv('TENANT')
client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')
scope = 'https://graph.microsoft.com/.default'
token_url = f'https://login.microsoftonline.com/{tenant}/oauth2/v2.0/token'

load_dotenv()

print(f"Client ID: {client_id}")
print(f"Client Secret: {client_secret}")

data = {
    'grant_type': 'client_credentials',
    'client_id': client_id,
    'client_secret': client_secret,
    'scope': scope
}

response = requests.post(token_url, data=data)

if response.status_code == 200:

    print (f'Responste Token Call: {response.json}')

    response.raise_for_status()
    tokens = response.json()
    access_token = tokens['access_token']

    url = f'https://graph.microsoft.com/v1.0/users/{tenant}'
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        response.raise_for_status()
        organization = response.json()
        tenant_id = organization['value'][0]['id']
        print(f'Tenant ID: {tenant_id}')
    else:
        response.raise_for_status()
        print(f'Status: {response}')
        print(response.json())
else:
    response.raise_for_status()
    print (f'Response: {response}')