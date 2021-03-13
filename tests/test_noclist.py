import pytest
import requests
import noclist

def test_get_auth_token(requests_mock):
    requests_mock.head('http://localhost:8888/auth', headers={'Badsec-Authentication-Token': 'FDE43423-362D-0DD8-C92C-BD32E6E24A6A', 'Date': 'Sat, 13 Mar 2021 07:50:09 GMT', 'Content-Length': '32', 'Content-Type': 'text/plain; charset=utf-8'})
    response = noclist.get_auth_token()
    assert response.headers['Badsec-Authentication-Token'] == 'FDE43423-362D-0DD8-C92C-BD32E6E24A6A'

def test_bad_get_auth_token(requests_mock):
    requests_mock.head('http://localhost:8888/auth', status_code=500)
    response = noclist.get_auth_token()
    import pdb; pdb.set_trace()
    # check that it tried three times and fails? or should that be a seperate function test
    # in which case, this should just test an exception is thrown, and a nother test function can test the wrapper


"""
Anything other than 200 should return as failure

If any call fails, retry up to 2 times

If a call to an endpoint fails, you should retry up to 2 times. If the call fails 3 times in a row, exit(1)

Avoid off by one errors! The correct sequence is: try -> fail -> retry -> fail -> retry -> exit if fail
"""