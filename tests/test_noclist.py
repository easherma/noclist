import pytest
import pdb
import requests.exceptions
import noclist
from .test_responses import users_text, auth_headers

"""
Anything other than 200 should return as failure

If any call fails, retry up to 2 times

If a call to an endpoint fails, you should retry up to 2 times. 
"""

def test_500_main_exits(requests_mock):
    with pytest.raises(SystemExit) as pytest_error:
        requests_mock.head("http://localhost:8888/auth", status_code=500)
        application = noclist.main()
    assert pytest_error.type == SystemExit
    assert pytest_error.value.code == 1


def test_main_success(requests_mock):
    with pytest.raises(SystemExit) as pytest_error:
        requests_mock.head("http://localhost:8888/auth", headers=auth_headers)
        requests_mock.get("http://localhost:8888/users", text=users_text)
        noclist.main()
    assert pytest_error.type == SystemExit
    assert pytest_error.value.code == 0


def test_get_auth_token(requests_mock):
    requests_mock.head("http://localhost:8888/auth", headers=auth_headers)
    token = noclist.get_auth_token().headers["Badsec-Authentication-Token"]
    assert token == "FDE43423-362D-0DD8-C92C-BD32E6E24A6A"


def test_bad_get_auth_token_500(requests_mock):
    with pytest.raises(SystemExit) as pytest_error:
        requests_mock.head("http://localhost:8888/auth", status_code=500)
        response = noclist.get_auth_token()
    assert pytest_error.type == SystemExit
    assert pytest_error.value.code == 1


def test_bad_get_auth_connection_error(requests_mock):
    with pytest.raises(SystemExit) as pytest_error:
        requests_mock.head(
            "http://localhost:8888/auth", exc=requests.exceptions.ConnectionError
        )
        response = noclist.get_auth_token()
    assert pytest_error.type == SystemExit
    assert pytest_error.value.code == 1


def test_bad_get_auth_http_error(requests_mock):
    with pytest.raises(SystemExit) as pytest_error:
        requests_mock.head(
            "http://localhost:8888/auth", exc=requests.exceptions.HTTPError
        )
        response = noclist.get_auth_token()
    assert pytest_error.type == SystemExit
    assert pytest_error.value.code == 1


def test_get_users_list_success_with_valid_token(requests_mock):
    requests_mock.get("http://localhost:8888/users", text=users_text)
    token = "FDE43423-362D-0DD8-C92C-BD32E6E24A6A"
    users_list = noclist.get_users_list(token)
    assert users_list.text == users_text


def test_get_users_list_httperror(requests_mock):
    with pytest.raises(SystemExit) as pytest_error:
        token = "FDE43423-362D-0DD8-C92C-BD32E6E24A6A"
        requests_mock.get(
            "http://localhost:8888/users", exc=requests.exceptions.HTTPError
        )
        users_list = noclist.get_users_list(token)
    assert pytest_error.type == SystemExit
    assert pytest_error.value.code == 1


def test_get_users_list_connection_error(requests_mock):
    with pytest.raises(SystemExit) as pytest_error:
        token = "FDE43423-362D-0DD8-C92C-BD32E6E24A6A"
        requests_mock.get(
            "http://localhost:8888/users", exc=requests.exceptions.ConnectionError
        )
        users_list = noclist.get_users_list(token)
    assert pytest_error.type == SystemExit
    assert pytest_error.value.code == 1



