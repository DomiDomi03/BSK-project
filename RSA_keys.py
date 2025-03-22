from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

# tworzenie klucza prywatnego RSA
def create_private_key():
    return rsa.generate_private_key(
    public_exponent=65537,  # tak ma być
    key_size=4096 ) # rozmiar klucza

# tworzenie klucza publicznego RSA
def create_public_key(private_key):
    return private_key.public_key()

# konwertowanie klucza prywatnego do formatu PEM
def convert_PEM_private(key):
    return (key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.TraditionalOpenSSL,
    encryption_algorithm=serialization.NoEncryption())
)

# konwertowanie klucza publicznego do formatu PEM
def convert_PEM_public(key):
    return (key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo)
)

# private_key = create_private_key()
# public_key = create_public_key(private_key)
#
# # Wyświetlenie kluczy
# print("🔑 Klucz prywatny:\n", convert_PEM_private(private_key).decode("utf-8"))
# print("🔓 Klucz publiczny:\n", convert_PEM_public(public_key).decode("utf-8"))