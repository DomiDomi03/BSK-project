from RSA_keys import *
from AES import *

private_key = create_private_key()
public_key = create_public_key(private_key)

print("🔑 Klucz prywatny:\n", convert_PEM_private(private_key).decode("utf-8"))
print("🔓 Klucz publiczny:\n", convert_PEM_public(public_key).decode("utf-8"))

private_RSA_key = create_private_key()
print(private_RSA_key)
private_key_bytes = convert_PEM_private(private_RSA_key)
print(private_key_bytes)
iv, decrypt_key = encrypt_aes(1234, private_key_bytes)
print(decrypt_key)
print(decrypt_aes(decrypt_key, iv, 1234))