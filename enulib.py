import requests
import hashlib
import hmac
import time
import json
import collections

test_mode = 'false'
enu_api_base_url = 'https://enu.io'
enu_api_test_base_url = 'http://localhost:8080'

def get_base_url():
    if test_mode == 'true':
        return enu_api_test_base_url
    else:
        return enu_api_base_url


def hmac_sha512(secret, data):
    digest = hmac.new(str(secret), msg=str(data), digestmod=hashlib.sha512).digest()
    signature = digest.encode("hex")
    return signature


def do_enu_api(url, method, post_data):
    enu_result = collections.namedtuple('enu_result', ['result', 'status_code'])

    with open('enu_key.json') as json_config_file:
        config = json.load(json_config_file)

    jsonData = json.dumps(post_data)

    authorization = hmac_sha512(config['secret'], jsonData)

    headers = {
        'accessKey': config['key'],
        'signature': authorization,
        'nonce': int(time.time() * 1000),
        'Content-Type': 'application/json'
    }

    if method == "POST":
        r = requests.post(url, data=jsonData, headers=headers, verify=False)
    elif method == "GET":
        r = requests.get(url, data=jsonData, headers=headers, verify=False)
    else:
        return enu_result(None, -1000)

    # print "Response code: " + str(r.status_code)
    # print "Response content: " + r.text

    if r.status_code != 200 and r.status_code != 201:
        result = enu_result(json.loads(r.text), r.status_code)
    else:
        result = enu_result(json.loads(r.text), 0)
    return result


def post_enu_api(url, post_data):
    return do_enu_api(url, "POST", post_data)


def get_enu_api(url, post_data):
    return do_enu_api(url, "GET", post_data)


def create_payment(destinationAddress, amount, asset, paymentId, txFee):
    data = {
        'destinationAddress': destinationAddress,
        'amount': amount,
        'asset': asset,
        'paymentId': paymentId,
        'txFee': txFee
    }

    result = post_enu_api(get_base_url() + '/payment', data)

    return result


def get_payment(paymentId):
    result = get_enu_api(get_base_url() + '/payment/' + paymentId, {})

    return result

def create_wallet():
    result = post_enu_api(get_base_url() + '/wallet', {})

    return result