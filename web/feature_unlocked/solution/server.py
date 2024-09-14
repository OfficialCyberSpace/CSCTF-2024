from flask import Flask, jsonify
import time
from Crypto.Hash import SHA256
from Crypto.PublicKey import ECC
from Crypto.Signature import DSS

app = Flask(__name__)


def load_private_key():
    with open('privkey', 'rb') as f:
        return ECC.import_key(f.read())


key = load_private_key()


def generate_date_and_sign(date):
    h = SHA256.new(date.encode('utf-8'))
    signer = DSS.new(key, 'fips-186-3')
    signature = signer.sign(h)
    return date, signature.hex()


@app.route('/pubkey', methods=['GET'])
def get_pubkey():
    return key.public_key().export_key(format='PEM'), 200, {'Content-Type': 'text/plain; charset=utf-8'}


@app.route('/', methods=['GET'])
def generate_signed_date():
    date = int(time.time()) + 14 * 24 * 60 * 60

    date, signature = generate_date_and_sign(str(date))

    return jsonify({
        'date': date,
        'signature': signature
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000)
