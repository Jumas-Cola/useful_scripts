from easyencrypt import newKeyPair, encrypt, decrypt
import pickle
from datetime import datetime
import os
import glob
import sys


class Session:
    def __init__(self, *, new=False):
        if new:
            pub, self.priv = newKeyPair()
            now = datetime.now().strftime("%Y%m%d_%H%M%S")
            path = 'my_pub'

            if not os.path.isdir(path):
                os.mkdir(path)

            with open(os.path.join(path, 'pub_{}.pickle'.format(now)), 'wb') as f:
                pickle.dump(pub, f)

            with open('priv_{}.pickle'.format(now), 'wb') as f:
                pickle.dump(self.priv, f)
        else:
            self.read_private_key()

    # Чтение приватного ключа из файла
    def read_private_key(self, priv_path=glob.glob('priv_[0-9]*_[0-9]*.pickle')[0]):
        if not os.path.isfile(priv_path):
            raise Exception('No file exists')

        with open(priv_path, 'rb') as f:
            self.priv = pickle.load(f)

    # Чтение ключа из файла в объект
    @staticmethod
    def read_key_obj(key_path):
        if not os.path.isfile(key_path):
            raise Exception('No file exists')

        with open(key_path, 'rb') as f:
            return pickle.load(f)

    # Зашифровать сообщение публичным ключом
    def encrypt_message(self, message, pub_path):
        pub = self.read_key_obj(pub_path)
        return encrypt(message.encode(encoding='utf8'), pub)

    # Расшифровать сообщение приватным ключом
    def decrypt_message(self, ciphertext):
        return decrypt(eval(ciphertext), self.priv)
        

if __name__ == '__main__':
    cmd = input('session_type> ')
    if cmd == 'new':
        session = Session(new=True)
    elif cmd == 'load':
        session = Session()
    while 1:
        cmd = input('command> ')
        if cmd == 'exit':
            sys.exit()
        elif cmd == 'encrypt':
            message = input('Message:\n')
            pub_path = input('Path to public key:\n')
            try:
                print()
                print(session.encrypt_message(message, pub_path))
            except Exception as e:
                print(str(e))
        elif cmd == 'decrypt':
            ciphertext = input('Ciphertext:\n')
            try:
                print()
                print(session.decrypt_message(ciphertext))
            except Exception as e:
                print(str(e))
        else:
            print('Command not found')
       
