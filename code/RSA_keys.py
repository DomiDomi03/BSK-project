##
#	@file RSA_keys.py
#	@details File to generate a pair of RSA keys (public and private)
#	@date 10-04-2025
##

from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
import random

## Function that generates private key
def create_private_key():
    return rsa.generate_private_key(
    public_exponent=65537,  # tak ma być
    key_size=4096 ) # rozmiar klucza


## Function that generates public key
# @param private_key is a generated private key
# @return public key based on generated private key
def create_public_key(private_key):
    return private_key.public_key()

## This function takes a private key and converts it into its PEM-encoded byte representation.
# @param key is a private key
def convert_PEM_private(key):
    return (key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.TraditionalOpenSSL,
    encryption_algorithm=serialization.NoEncryption())
)

## This function takes a public key and converts it into its PEM-encoded byte representation.
# @param key is a public key
def convert_PEM_public(key):
    return (key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo)
)

## Function that generates user pin
# @return random integer from 0 to 99999999 (generation of user pin)
def generate_pin():
    return random.randint(0, 99999999)
