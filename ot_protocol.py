# import random
# import os
# from cryptography.hazmat.primitives.ciphers.aead import AESGCM
# import hashlib
# import json

# # 2048-bit MODP Group (RFC 3526)
# PRIME = 0xFFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD129024E088A67CC74020BBEA63B139B22514A08798E3404DDEF9519B3CD3A431B302B0A6DF25F14374FE1356D6D51C245E485B576625E7EC6F44C42E9A637ED6B0BFF5CB6F406B7EDEE386BFB5A899FA5AE9F24117C4B1FE649286651ECE45B3DC2007CB8A163BF0598DA48361C55D39A69163FA8FD24CF5F83655D23DCA3AD961C62F356208552BB9ED529077096966D670C354E4ABC9804F1746C08CA18217C32905E462E36CE3BE39E772C180E86039B2783A2EC07A28FB5C55DF06F4C52C9DE2BCBF6955817183995497CEA956AE515D2261898FA051015728E5A8AACAA68FFFFFFFFFFFFFFFF
# GENERATOR = 2

# class OTSender:
#     def __init__(self):
#         self.private_key, self.public_key = self._generate_keys()
    
#     def _generate_keys(self):
#         priv = random.randint(2, PRIME-2)
#         pub = pow(GENERATOR, priv, PRIME)
#         return priv, pub
    
#     def encrypt_messages(self, pk0, pk1, message0, message1):
#         s0 = pow(pk0, self.private_key, PRIME)
#         s1 = pow(pk1, self.private_key, PRIME)
        
#         key0 = hashlib.sha256(s0.to_bytes(256, 'big')).digest()
#         key1 = hashlib.sha256(s1.to_bytes(256, 'big')).digest()
        
#         nonce0, cipher0 = self._aes_encrypt(key0, message0)
#         nonce1, cipher1 = self._aes_encrypt(key1, message1)
        
#         return json.dumps({
#             'c0': (nonce0.hex(), cipher0.hex()),
#             'c1': (nonce1.hex(), cipher1.hex())
#         })
    
#     def _aes_encrypt(self, key, plaintext):
#         aesgcm = AESGCM(key)
#         nonce = os.urandom(12)
#         ciphertext = aesgcm.encrypt(nonce, plaintext.encode('utf-8'), None)
#         return nonce, ciphertext

# class OTReceiver:
#     def __init__(self):
#         self.choice = None
#         self.k = None
    
#     def generate_pk(self, sender_pubkey, choice):
#         self.choice = choice
#         self.k = random.randint(2, PRIME-2)
        
#         if choice == 0:
#             pk0 = pow(GENERATOR, self.k, PRIME)
#             pk1 = (sender_pubkey * pow(pk0, PRIME-2, PRIME)) % PRIME
#         else:
#             pk1 = pow(GENERATOR, self.k, PRIME)
#             pk0 = (sender_pubkey * pow(pk1, PRIME-2, PRIME)) % PRIME
            
#         return json.dumps({
#             'pk0': pk0,
#             'pk1': pk1
#         })
    
#     def decrypt_message(self, sender_pubkey, ciphertext):
#         s_b = pow(sender_pubkey, self.k, PRIME)
#         key = hashlib.sha256(s_b.to_bytes(256, 'big')).digest()
#         return self._aes_decrypt(key, ciphertext)
    
#     def _aes_decrypt(self, key, ciphertext):
#         aesgcm = AESGCM(key)
#         nonce = bytes.fromhex(ciphertext[0])
#         ct = bytes.fromhex(ciphertext[1])
#         plaintext = aesgcm.decrypt(nonce, ct, None)
#         return plaintext.decode('utf-8')

import random
import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import hashlib

# 2048-bit MODP Group (RFC 3526)
PRIME = int(
    "FFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD129024E088A67CC74020BBEA63B139B22514A08798E3404DDEF"
    "9519B3CD3A431B302B0A6DF25F14374FE1356D6D51C245E485B576625E7EC6F44C42E9A637ED6B0BFF5CB6F406B7EDEE"
    "386BFB5A899FA5AE9F24117C4B1FE649286651ECE45B3DC2007CB8A163BF0598DA48361C55D39A69163FA8FD24CF5F83"
    "655D23DCA3AD961C62F356208552BB9ED529077096966D670C354E4ABC9804F1746C08CA18217C32905E462E36CE3BE3"
    "9E772C180E86039B2783A2EC07A28FB5C55DF06F4C52C9DE2BCBF6955817183995497CEA956AE515D2261898FA051015"
    "728E5A8AACAA68FFFFFFFFFFFFFFFF", 16
)
GENERATOR = 2

class NaorPinkasSender:
    def __init__(self):
        self.private_key = random.randint(2, PRIME-2)
        self.public_key = pow(GENERATOR, self.private_key, PRIME)
    
    def encrypt_messages(self, pk0, pk1, m0, m1):
        s0 = pow(pk0, self.private_key, PRIME)
        s1 = pow(pk1, self.private_key, PRIME)
        
        key0 = hashlib.sha256(s0.to_bytes(256, 'big')).digest()
        key1 = hashlib.sha256(s1.to_bytes(256, 'big')).digest()
        
        nonce0, cipher0 = self._aes_encrypt(key0, m0)
        nonce1, cipher1 = self._aes_encrypt(key1, m1)
        
        return {
            'ciphertexts': [
                (nonce0.hex(), cipher0.hex()),
                (nonce1.hex(), cipher1.hex())
            ]
        }
    
    def _aes_encrypt(self, key, plaintext):
        aesgcm = AESGCM(key)
        nonce = os.urandom(12)
        ciphertext = aesgcm.encrypt(nonce, plaintext.encode('utf-8'), None)
        return nonce, ciphertext

class NaorPinkasReceiver:
    def __init__(self, choice):
        if choice not in {0, 1}:
            raise ValueError("Choice must be 0 or 1")
        self.choice = choice
        self.k = random.randint(2, PRIME-2)
    
    def generate_public_keys(self, sender_pubkey):
        if self.choice == 0:
            pk0 = pow(GENERATOR, self.k, PRIME)
            pk1 = (sender_pubkey * pow(pk0, PRIME-2, PRIME)) % PRIME
        else:
            pk1 = pow(GENERATOR, self.k, PRIME)
            pk0 = (sender_pubkey * pow(pk1, PRIME-2, PRIME)) % PRIME
        
        return {'pk0': pk0, 'pk1': pk1}
    
    def decrypt_message(self, sender_pubkey, ciphertext):
        s_b = pow(sender_pubkey, self.k, PRIME)
        key = hashlib.sha256(s_b.to_bytes(256, 'big')).digest()
        return self._aes_decrypt(key, ciphertext)
    
    def _aes_decrypt(self, key, ciphertext):
        aesgcm = AESGCM(key)
        nonce = bytes.fromhex(ciphertext[0])
        ct = bytes.fromhex(ciphertext[1])
        return aesgcm.decrypt(nonce, ct, None).decode('utf-8')