#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Servidor Receptor de Datos Empresariales
Para recibir y descifrar reportes del sistema de monitoreo
"""

import http.server
import socketserver
import json
import base64
import hashlib
import datetime
import os
import argparse
import threading
import time

class DataDecryptor:
    """Módulo de descifrado de datos empresariales"""
    
    def __init__(self, key="SystemMonitor2025-AccessControl"):
        self._k = key
        self._m = self._gen_matrix(self._k)
    
    def _gen_matrix(self, key):
        """Genera matriz de descifrado"""
        h = hashlib.sha256(key.encode()).hexdigest()
        return [int(h[i:i+2], 16) for i in range(0, len(h), 2)]
    
    def decrypt(self, encrypted_data):
        """Descifra datos protegidos"""
        try:
            # Decodificar de base64
            encrypted_bytes = base64.b64decode(encrypted_data)
            
            # Aplicar descifrado XOR
            decrypted = bytearray()
            for i, byte in enumerate(encrypted_bytes):
                decrypted.append(byte ^ self._m[i % len(self._m)])
            
            return decrypted.decode('utf-8')
        except Exception as e:
            print(f"❌ Error al descifrar: {e}")
            return None

class DataReceiver(http.server.BaseHTTPRequestHandler):
    """Manejador HTTP para recibir datos del monitoreo"""
    
    def __init__(self, *args, decryptor=None, output_dir="received_data", **kwargs):
        self.decryptor = decryptor
        self.output_dir = output_dir
        super().__init__(*args, **kwargs)
    
    def do_POST(self):
        """Maneja las peticiones POST con datos del monitoreo"""
        if self.path == '/receive_data':
            try:
                # Leer datos del POST
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                
                # Parsear JSON
                data = json.loads(post_data.decode('utf-8'))
                
                # Extraer información
                timestamp = data.get('timestamp', datetime.datetime.now().isoformat())
                encrypted_data = data.get('data', '')
                source = data.get('source', 'unknown')
                version = data.get('version', 'unknown')
                
                print(f"📨 Datos recibidos de {source} (v{version}) - {timestamp}")
                
                # Descifrar datos
                if self.decryptor and encrypted_data:
                    decrypted_text = self.decryptor.decrypt(encrypted_data)
                    
                    if decrypted_text:
                        # Guardar datos descifrados
                        self._save_decrypted_data(decrypted_text, timestamp, source)
                        print(f"✅ Datos descifrados y guardados")
                        
                        # Mostrar preview del contenido
                        preview = decrypted_text[:100].replace('\n', '\\n')
                        if len(decrypted_text) > 100:
                            preview += "..."
                        print(f"📝 Preview: {preview}")
                    else:
                        print(f"❌ Error al descifrar los datos")
                
                # Responder con éxito
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = {"status": "success", "message": "Data received"}
                self.wfile.write(json.dumps(response).encode())
                
            except Exception as e:
                print(f"❌ Error procesando datos: {e}")
                self.send_response(500)
                self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()
    
    def _save_decrypted_data(self, decrypted_text, timestamp, source):
        """Guarda los datos descifrados en archivos organizados"""
        try:
            # Crear directorio si no existe
            os.makedirs(self.output_dir, exist_ok=True)
            
            # Nombre del archivo basado en timestamp
            clean_timestamp = timestamp.replace(':', '-').replace('.', '-')
            filename = f"{source}_{clean_timestamp}.txt"
            filepath = os.path.join(self.output_dir, filename)
            
            # Guardar archivo
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(f"Timestamp: {timestamp}\n")
                f.write(f"Source: {source}\n")
                f.write("=" * 50 + "\n")
                f.write(decrypted_text)
            
            print(f"💾 Guardado en: {filepath}")
            
        except Exception as e:
            print(f"❌ Error guardando archivo: {e}")
    
    def log_message(self, format, *args):
        """Suprimir logs HTTP innecesarios"""
        pass

def start_server(port=8080, output_dir="received_data"):
    """Inicia el servidor receptor"""
    
    print("🚀 Servidor Receptor de Datos Empresariales")
    print("=" * 50)
    print(f"🌐 Puerto: {port}")
    print(f"📁 Directorio de salida: {output_dir}")
    print(f"🔐 Descifrado: Activado")
    print("=" * 50)
    
    # Crear directorio de salida
    os.makedirs(output_dir, exist_ok=True)
    
    # Inicializar descifrador
    decryptor = DataDecryptor()
    
    # Crear handler con configuración personalizada
    def handler_factory(*args, **kwargs):
        return DataReceiver(*args, decryptor=decryptor, output_dir=output_dir, **kwargs)
    
    # Configurar servidor
    with socketserver.TCPServer(("", port), handler_factory) as httpd:
        print(f"✅ Servidor iniciado en http://0.0.0.0:{port}")
        print("📡 Esperando datos del monitoreo...")
        print("⚠️  Presiona Ctrl+C para detener")
        print()
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🔴 Deteniendo servidor...")
            httpd.shutdown()
            print("✅ Servidor detenido")

def main():
    parser = argparse.ArgumentParser(description='Servidor Receptor de Datos de Monitoreo')
    parser.add_argument('--port', '-p', type=int, default=8080, 
                       help='Puerto del servidor (default: 8080)')
    parser.add_argument('--output', '-o', default='received_data',
                       help='Directorio para guardar datos (default: received_data)')
    
    args = parser.parse_args()
    
    start_server(port=args.port, output_dir=args.output)

if __name__ == "__main__":
    main()
