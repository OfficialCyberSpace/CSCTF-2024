from Crypto.PublicKey import ECC

# Generate ECC key pair
key = ECC.generate(curve='P-256')

# Write the public key to a file
with open('pubkey.pem', 'wb') as f:
    f.write(key.public_key().export_key(format='PEM').encode('utf-8'))

# Write the private key to a file
with open('privkey.pem', 'wb') as f:
    f.write(key.export_key(format='PEM').encode('utf-8'))
