import pdb
import sys
import requests
import hashlib
import json
from collections import namedtuple

BASE_URL = "http://localhost:8888"


def retry(request_function):
    """
    decorator that will retry up to a given threshold
    once that threshold is exceeded, the function will call a system exit and the program will fail
    """

    def retry_wrapper(*args, **kwargs):
        attempts_threshold = 2
        attempts = 0
        while attempts <= attempts_threshold:
            attempts += 1
            print("attempt:", attempts, file=sys.stderr)
            try:
                print(f"trying {request_function.__name__} function", file=sys.stderr)
                response = request_function(*args, **kwargs)
            except Exception as e:
                print("An Exception has occured:", e, file=sys.stderr)
                # TODO: better error handiling, exponential backoff
                print("retrying request", file=sys.stderr)
                continue
            else:
                if response.status_code == 200:
                    return response
                else:
                    print("retrying request", file=sys.stderr)
                    continue
        else:
            print("maximum retries exceeded", file=sys.stderr)
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
    # TODO: this seemingly dosen't always generate a new token, but it does if I call the function again while debugging
    auth_token = get_auth_token().headers["Badsec-Authentication-Token"]
    parsed_users_list = json.dumps(get_users_list(auth_token).text.split("\n"))

    if auth_token and parsed_users_list:
        # we have both the auth token and a correctly parsed user list, so we're good
        print(parsed_users_list)
        exit(0)
    else:
        print("error occured", file=sys.stderr)
        exit(1)


if __name__ == "__main__":
    main()
