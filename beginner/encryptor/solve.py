from base64 import b64decode

from Crypto.Cipher import Blowfish
from Crypto.Util.Padding import unpad

key = b"encryptorencryptor"
encoded_data = (
    b"OIkZTMehxXAvICdQSusoDP6Hn56nDiwfGxt7w/Oia4oxWJE3NVByYnOMbqTuhXKcgg50DmVpudg="
)

encrypted_data = b64decode(encoded_data)
cipher = Blowfish.new(key, Blowfish.MODE_ECB)

decrypted_data = unpad(cipher.decrypt(encrypted_data), Blowfish.block_size)
print(decrypted_data.decode("utf-8")) # CSCTF{3ncrypt0r_15nt_s4Fe_w1th_4n_h4Rdc0d3D_k3y!}