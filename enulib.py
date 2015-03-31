import requests
import hashlib
import hmac
import time
import json


def hmac_sha512(secret, data):
    digest = hmac.new(str(secret), msg=str(data), digestmod=hashlib.sha512).digest()
    signature = digest.encode("hex")
    return signature


def create_payment(destinationAddress, amount, asset, paymentId, txFee):
    with open('enu_key.json') as json_config_file:
        config = json.load(json_config_file)
    # print(config)

    data = {
        'destinationAddress': destinationAddress,
        'amount': amount,
        'asset': asset,
        'paymentId': paymentId,
        'txFee': txFee
    }

    jsonData = json.dumps(data)

    authorization = hmac_sha512(config['secret'], jsonData)

    headers = {
        'accessKey': config['key'],
        'signature': authorization,
        'nonce': int(time.time() * 1000),
        'Content-Type': 'application/json'
    }

    r = requests.post('https://enu.io/payment', data=jsonData, headers=headers, verify=False)
    # print "Response code: " + str(r.status_code)
    # print "Response content: " + r.text

    return json.loads(r.text)


def get_payment(paymentId):
    with open('enu_key.json') as json_config_file:
        config = json.load(json_config_file)

    data = {}
    jsonData = json.dumps(data)

    authorization = hmac_sha512(config['secret'], jsonData)

    headers = {
        'accessKey': config['key'],
        'signature': authorization,
        'nonce': int(time.time() * 1000),
        'Content-Type': 'application/json'
    }

    r = requests.get('https://enu.io/payment/' + paymentId, data=jsonData, headers=headers, verify=False)
    # r = requests.get('http://localhost:8080/payment/' + paymentId, data=jsonData, headers=headers, verify=False)
    # print "Response code: " + str(r.status_code)
    # print "Response content: " + r.text

    return json.loads(r.text)