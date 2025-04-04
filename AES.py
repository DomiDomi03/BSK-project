from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
import os

# zaszyfrowanie klucza RSA AES'em
def encrypt_aes(pin, private_key):
    key = hashes.Hash(hashes.SHA256())
    key.update(str(pin).encode())
    hashed_key = key.finalize()
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(hashed_key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    padded_key = private_key.ljust(len(private_key) + (16 - len(private_key) % 16), b' ')
    encrypted_private_key = encryptor.update(padded_key) + encryptor.finalize()
    return iv, encrypted_private_key

# odszyfrowanie klucza RSA AES'em
def decrypt_aes(decrypt_key, iv, pin):
    key = hashes.Hash(hashes.SHA256())
    key.update(str(pin).encode())
    hashed_key = key.finalize()
    cipher = Cipher(algorithms.AES(hashed_key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_private_key = decryptor.update(decrypt_key) + decryptor.finalize()
    decrypted_private_key = decrypted_private_key.rstrip(b' ')
    return decrypted_private_key



