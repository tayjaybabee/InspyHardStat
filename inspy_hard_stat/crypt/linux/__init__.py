from nacl import secret, utils
from nacl.encoding import Base64Encoder

# Generate a key (this should be stored securely and reused)
key = utils.random(secret.SecretBox.KEY_SIZE)
box = secret.SecretBox(key)

# Encrypt the data
def encrypt_data(data):
    encrypted = box.encrypt(data.encode('utf-8'), encoder=Base64Encoder)
    return encrypted.decode('utf-8')

# Decrypt the data
def decrypt_data(encrypted_data):
    decrypted = box.decrypt(encrypted_data.encode('utf-8'), encoder=Base64Encoder)
    return decrypted.decode('utf-8')
