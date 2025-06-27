import base64
import hashlib
import os
import sys

class SimpleDecryptor:
    # descifrador simple usando XOR+Base64
    
    def __init__(self, password):
        # arranco con la contraseña y genero mi clave
        self.key = self._generate_key(password)
    
    def _generate_key(self, password):
        # creo una clave desde la contraseña usando SHA256
        hash_object = hashlib.sha256(password.encode())
        hex_dig = hash_object.hexdigest()
        
        # convierto hex a bytes para las operaciones XOR
        key = []
        for i in range(0, len(hex_dig), 2):
            key.append(int(hex_dig[i:i+2], 16))
        
        return key
    
    def decrypt(self, encrypted_text):
        # descifro el texto encriptado con base64+XOR
        try:
            if not encrypted_text:
                return ""
            
            # decodifico desde base64 primero
            encrypted_bytes = base64.b64decode(encrypted_text.encode('utf-8'))
            
            # aplico XOR con mi clave (XOR es simétrico, misma operación que encriptar)
            decrypted_bytes = bytearray()
            for i, byte in enumerate(encrypted_bytes):
                key_byte = self.key[i % len(self.key)]
                decrypted_bytes.append(byte ^ key_byte)
            
            # convierto de vuelta a texto legible
            return decrypted_bytes.decode('utf-8')
            
        except Exception as e:
            return None

def main():
    # uso simple: python decryptor.py archivo.enc clave
    if len(sys.argv) != 3:
        print("Uso: python decryptor.py <archivo_cifrado> <clave>")
        return
    
    file_path = sys.argv[1]
    password = sys.argv[2]
    
    # verifico si existe el archivo cifrado
    if not os.path.exists(file_path):
        return
    
    # leo el contenido cifrado
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            encrypted_content = f.read().strip()
    except Exception as e:
        return
    
    # descifro y muestro el resultado
    decryptor = SimpleDecryptor(password)
    decrypted_text = decryptor.decrypt(encrypted_content)
    
    if decrypted_text is not None:
        # solo imprimo el texto descifrado, nada más
        print(decrypted_text)

if __name__ == "__main__":
    main()
