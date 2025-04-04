import RSA_keys
import AES

private_RSA_key = RSA_keys.create_private_key()
print(private_RSA_key)
private_key_bytes = RSA_keys.convert_PEM_private(private_RSA_key)
print(private_key_bytes)
iv, key, decrypt_key = AES.encrypt_aes(1234, private_key_bytes)
print(decrypt_key)
print(AES.decrypt_aes(decrypt_key, iv, 1234))