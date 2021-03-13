import sys
import requests
import hashlib
import json

def get_auth_token():
    response = requests.head('http://localhost:8888/auth')
    return response.headers['Badsec-Authentication-Token']

def calculate_checksum(auth_token, request_path):
    return hashlib.sha256(auth_token.encode() + request_path.encode()).hexdigest()

def get_users_list(auth_token):
    headers = {'X-Request-Checksum': calculate_checksum(auth_token, '/users')}
    response = requests.get('http://localhost:8888/users', headers= headers)
    return response


def main():
    auth_token = get_auth_token()
    users_list = json.dumps(get_users_list(auth_token).text.split('\n'))
    print(users_list)
    exit(0)

if __name__ == "__main__":
    main()