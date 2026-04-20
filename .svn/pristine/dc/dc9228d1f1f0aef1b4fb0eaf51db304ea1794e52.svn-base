# -*- coding: utf-8 -*-

import base64
import string
class Helper_crypt:
    def __init__(self):
        pass
    # Méthode pour encoder une chaîne en Base64
    def encode_base64(self, data):
        """Encode une chaîne en base64."""
        return base64.b64encode(data.encode('utf-8'))

    # Méthode pour décoder une chaîne Base64
    def decode_base64(self, encoded_data):
        """Décode une chaîne base64."""
        return base64.b64decode(encoded_data).decode('utf-8')

    def caesar_cipher_encrypt(self, text, shift):
        hex_text = ''.join([hex(ord(char))[2:].zfill(2) for char in text])
        result = ''
        for i in range(0, len(hex_text), 2):
            hex_char = hex_text[i:i + 2]
            int_val = int(hex_char, 16)
            shifted_val = (int_val + shift) % 256
            result += hex(shifted_val)[2:].zfill(2)
        base64_encoded = base64.b64encode(result.encode('utf-8')).decode('utf-8')
        return base64_encoded

    def caesar_cipher_decrypt(self, base64_encoded_text, shift):
        decoded_base64 = base64.b64decode(base64_encoded_text).decode('utf-8')
        result = ''
        for i in range(0, len(decoded_base64), 2):
            hex_char = decoded_base64[i:i + 2]
            int_val = int(hex_char, 16)
            shifted_val = (int_val - shift) % 256
            result += chr(shifted_val)
        return result


