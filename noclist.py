import pdb
import sys
import requests
import hashlib
import json
from collections import namedtuple

BASE_URL = "http://localhost:8888"


def retry(request_function):
    # TODO: logging, error handiling, test cases for anything but 200
    def retry_wrapper(*args, **kwargs):
        attempts_threshold = 2
        attempts = 0
        while attempts <= attempts_threshold:
            attempts += 1
            print("attempt:", attempts)
            try:
                print(f"trying {request_function.__name__} function")
                response = request_function(*args, **kwargs)
            except Exception as e:
                print("BIG PROBLEM", e)
                # TODO: better error handiling, exponential backoff
                continue
            else:
                if response.status_code == 200:
                    return response
                else:
                    continue
        else:
            print("maximum retries exceeded")
            exit(1)

    return retry_wrapper


@retry
def get_auth_token():
    response = requests.head(f"{BASE_URL}/auth")
    return response


@retry
def get_users_list(auth_token):
    """
    gets the list of users. requires a valid checksum to be passed in the header
    at the moment the auth token is passed here where checksum is called
    TODO: clean this up, think about seperation of concerns
    """
    headers = {"X-Request-Checksum": calculate_checksum(auth_token, "/users")}
    response = requests.get("http://localhost:8888/users", headers=headers)
    return response


def calculate_checksum(auth_token, request_path):
    """
    used by get_users_list
    """
    return hashlib.sha256(auth_token.encode() + request_path.encode()).hexdigest()


def main():
    """
    retrive a list of users from the server
    a valid auth token is required, which is combined with the endpoint to create a checksum
    the list is returned as a list of 64-bit user ids which need to be split out onto their own lines
    """
    # TODO: this seemingly dosen't always generate a new token
    auth_token = get_auth_token().headers["Badsec-Authentication-Token"]
    parsed_users_list = json.dumps(get_users_list(auth_token).text.split("\n"))

    if auth_token and parsed_users_list:
        print(parsed_users_list)
        pdb.set_trace()
        exit(0)
    else:
        print("error occured", file=sys.stderr)
        exit(1)


if __name__ == "__main__":
    main()
