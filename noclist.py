import sys
import requests

def get_auth_token():
    response = requests.get('http://localhost:8888/auth')
    import pdb; pdb.set_trace()
    return response.headers['Badsec-Authentication-Token']


def main():
    get_auth_token()
    exit(0)

if __name__ == "__main__":
    main()