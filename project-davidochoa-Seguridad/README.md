# Keylogger con Cifrado y Transmisión Remota

Este es mi proyecto educativo de seguridad informática que desarrollé para aprender sobre monitoreo de teclas, cifrado de datos y comunicación entre máquinas virtuales.

## ¿Qué hace?

Creé un keylogger completo que:
- Captura todas las teclas presionadas en tiempo real
- Reconstruye el texto automáticamente cada 3 segundos
- Cifra el contenido usando XOR + Base64
- Envía los datos cifrados a una máquina atacante remota
- Permite descifrar los datos capturados

## Archivos principales

### Para la máquina víctima:
- `unified_keylogger.py` - El keylogger principal con todas las funcionalidades
- `reconstructor.py` - Convierte las teclas capturadas en texto legible  
- `keylogger_auto.sh` - Ejecutable que instala todo y ejecuta con un solo clic

### Para la máquina atacante:
- `data_receiver.py` - Servidor que recibe los datos cifrados
- `decryptor.py` - Descifra los archivos recibidos

## Cómo usar

### Máquina atacante (IP: 10.0.2.15):
```bash
python data_receiver.py
```

### Máquina víctima:
```bash
chmod +x keylogger_auto.sh
./keylogger_auto.sh
```

### Descifrar datos capturados:
```bash
python decryptor.py archivo.enc ClaveSecreta2025-CyberSeguridad
```

## Tecnologías utilizadas

- **Python** - Lenguaje principal
- **pynput** - Captura de teclas
- **requests** - Comunicación HTTP
- **flask** - Servidor receptor
- **XOR + Base64** - Cifrado simétrico
- **Threading** - Procesamiento concurrente

## Propósito educativo

Desarrollé este proyecto en un entorno de laboratorio controlado con máquinas virtuales aisladas para aprender sobre:
- Técnicas de monitoreo
- Algoritmos de cifrado
- Comunicación cliente-servidor
- Manejo de hilos en Python
- Seguridad informática ética  
