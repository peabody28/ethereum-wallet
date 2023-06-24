import requests

def sendRequest(url, data):
    resp = requests.post(url, json=data)
    return resp
