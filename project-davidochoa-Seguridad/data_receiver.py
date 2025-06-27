#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
from datetime import datetime
from flask import Flask, request, jsonify

class DataReceiver:
    # servidor simple para recibir datos cifrados desde la vm
    
    def __init__(self, port=8080, save_dir="received_data"):
        # configuro el servidor flask y directorio de guardado
        self.app = Flask(__name__)
        self.port = port
        self.save_dir = save_dir
        self.received_count = 0
        
        # creo el directorio si no existe
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        
        # configuro las rutas
        self.setup_routes()
    
    def setup_routes(self):
        # defino las rutas del servidor
        
        @self.app.route('/receive_data', methods=['POST'])
        def receive_data():
            try:
                # obtengo los datos json del request
                data = request.get_json()
                
                if not data or 'encrypted_data' not in data:
                    return jsonify({'error': 'datos inválidos'}), 400
                
                # extraigo la información
                timestamp = data.get('timestamp', datetime.now().isoformat())
                encrypted_content = data.get('encrypted_data', '')
                source = data.get('source', 'unknown')
                
                # genero nombre de archivo único
                self.received_count += 1
                filename = f"encrypted_data_{self.received_count}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.enc"
                filepath = os.path.join(self.save_dir, filename)
                
                # guardo el contenido cifrado
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(encrypted_content)
                
                # log del servidor
                print(f"📡 datos recibidos #{self.received_count}")
                print(f"   - fuente: {source}")
                print(f"   - timestamp: {timestamp}")
                print(f"   - guardado en: {filepath}")
                print(f"   - tamaño: {len(encrypted_content)} caracteres")
                
                return jsonify({
                    'status': 'éxito',
                    'filename': filename,
                    'received_count': self.received_count
                })
                
            except Exception as e:
                print(f"❌ error procesando datos: {e}")
                return jsonify({'error': str(e)}), 500
        
        @self.app.route('/status', methods=['GET'])
        def status():
            # endpoint para verificar el estado del servidor
            return jsonify({
                'status': 'activo',
                'received_count': self.received_count,
                'save_directory': self.save_dir
            })
    
    def start_server(self):
        # inicio el servidor
        print(f"🚀 servidor receptor iniciado")
        print(f"📡 escuchando en puerto {self.port}")
        print(f"📁 guardando en: {os.path.abspath(self.save_dir)}")
        print(f"🔗 endpoint: http://localhost:{self.port}/receive_data")
        print(f"🚨 presiona ctrl+c para detener\n")
        
        try:
            # inicio flask (host='0.0.0.0' permite conexiones externas)
            self.app.run(host='0.0.0.0', port=self.port, debug=False)
        except KeyboardInterrupt:
            print("\n🛑 servidor detenido")

def main():
    # uso: python data_receiver.py
    print("📡 RECEPTOR DE DATOS CIFRADOS")
    print("=" * 40)
    
    # creo y arranco el servidor
    receiver = DataReceiver(port=8080, save_dir="received_data")
    receiver.start_server()

if __name__ == "__main__":
    main()
