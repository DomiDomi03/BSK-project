##
#	@file AES.py
#	@details File to encrypt RSA keys by using AES algorithm
#	@date 10-04-2025
##

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import padding
import os

## Function that encrypts the user's private key by using AES algorithm.
# @param private_key is the private key of user
# @param pin is the pin given by the user in order to encrypt the private key
# @return iv initialization vector used in encryption of the private key and encrypted private key of user
def encrypt_aes(pin, private_key):
    hash = hashes.Hash(hashes.SHA256())
    hash.update(str(pin).encode())
    key = hash.finalize()
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    # padded_key = private_key.ljust(len(private_key) + (16 - len(private_key) % 16), b' ')

    print(f"Private key length before padding: {len(private_key)} bytes")

    # dopełnianie - 128 bitowe bloki
    padder = padding.PKCS7(128).padder()
    padded_key = padder.update(private_key) + padder.finalize()

    print(f"Private key length after padding: {len(padded_key)} bytes")

    encrypted_private_key = encryptor.update(padded_key) + encryptor.finalize()
    return iv, encrypted_private_key

## Function that decrypts the user's private key by using AES algorithm.
# @param decrypt_key is the decrypted private key
# @param iv is an initialization vector used in encryption of the private key
# @param pin is a pin given by the user in order to use private key
# @return decrypted private key of user
def decrypt_aes(decrypt_key, iv, pin):
    hash = hashes.Hash(hashes.SHA256())
    hash.update(str(pin).encode())
    key = hash.finalize()
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_private_key = decryptor.update(decrypt_key) + decryptor.finalize()

    unpadder = padding.PKCS7(128).unpadder()
    decrypted_private_key = unpadder.update(decrypted_private_key) + unpadder.finalize()

    #decrypted_private_key = decrypted_private_key.rstrip(b' ')
    return decrypted_private_key



