import pytest
import requests

def test_get_auth_token(requests_mock):
    requests_mock.head('http://localhost:8888/auth', headers={'Badsec-Authentication-Token': 'FDE43423-362D-0DD8-C92C-BD32E6E24A6A', 'Date': 'Sat, 13 Mar 2021 07:50:09 GMT', 'Content-Length': '32', 'Content-Type': 'text/plain; charset=utf-8'})
    response = requests.head('http://localhost:8888/auth')

    assert response.headers['Badsec-Authentication-Token'] == 'FDE43423-362D-0DD8-C92C-BD32E6E24A6A'
