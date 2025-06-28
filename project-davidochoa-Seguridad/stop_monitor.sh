#!/bin/bash
# Script para detener el monitoreo del sistema

INSTALL_DIR="/tmp/.sys_tools"
PID_FILE="$INSTALL_DIR/.monitor_pid"

stop_monitor() {
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if kill -0 "$PID" 2>/dev/null; then
            echo "🔴 Deteniendo monitoreo (PID: $PID)..."
            kill "$PID" 2>/dev/null
            sleep 2
            
            # Verificar si sigue corriendo
            if kill -0 "$PID" 2>/dev/null; then
                echo "⚠️  Forzando detención..."
                kill -9 "$PID" 2>/dev/null
            fi
            
            rm -f "$PID_FILE"
            echo "✅ Monitoreo detenido"
        else
            echo "⚠️  El proceso ya no está ejecutándose"
            rm -f "$PID_FILE"
        fi
    else
        echo "⚠️  No se encontró archivo PID"
        # Intentar matar todos los procesos python que contengan system_monitor
        pkill -f "system_monitor.py" 2>/dev/null && echo "✅ Procesos relacionados detenidos" || echo "ℹ️  No se encontraron procesos activos"
    fi
}

cleanup_files() {
    echo "🧹 Limpiando archivos temporales..."
    rm -rf "$INSTALL_DIR" 2>/dev/null || true
    echo "✅ Limpieza completada"
}

# Función principal
main() {
    echo "🛑 Script de detención del monitoreo del sistema"
    stop_monitor
    
    if [[ "$*" == *"--cleanup"* ]]; then
        cleanup_files
    fi
    
    echo "🏁 Proceso completado"
}

main "$@"
