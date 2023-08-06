from cryptography.fernet import Fernet
import os


class Encryptor():
    
    def key_create(self):
        key = Fernet.generate_key()
        return key

    def key_write(self, key, key_name):
        with open(key_name, 'wb') as mykey:
            mykey.write(key)

    def key_load(self, key_name):
        with open(key_name, 'rb') as mykey:
            key = mykey.read()
        return key

    def encrypt_file(self, key, file_name):
        def get_file_data(filename:str) -> bytes:
            with open(filename, 'r') as fo:
                 data = fo.read()
            return data.encode("utf-8")

        plain_text:bytes = get_file_data(file_name)
        f:"Fernet" = Fernet(key)
        cipher_text = f.encrypt(plain_text)

        with open (file_name + ".enc", 'wb') as fo:
            fo.write(cipher_text)
        os.remove(file_name)