import re
import os
from typing import Optional
from datetime import datetime

class TextReconstructor:
    """
    Esta clase convierte el chaos de un keylogger en texto legible.
    Es como un traductor que lee las teclas capturadas y las vuelve a juntar.
    """

    def __init__(self):
        # Diccionario que traduce las teclas raras del keylogger a caracteres normales
        # Por ejemplo: cuando el keylogger pone '[space]', nosotros sabemos que es un espacio ' '
        self.special_keys = {
            '[space]': ' ',      # Espacios en blanco
            '[enter]': '\n',     # Salto de línea (cuando presionas Enter)
            '[tab]': '\t',       # Tabulación
            '[shift]': '',       # Shift - lo ignoramos porque no imprime nada
            '[shift_l]': '',     # Shift izquierdo - también ignorado
            '[shift_r]': '',     # Shift derecho - también ignorado
            '[ctrl]': '',        # Control - no imprime nada visible
            '[ctrl_l]': '',      # Control izquierdo
            '[ctrl_r]': '',      # Control derecho
            '[alt]': '',         # Alt - tampoco imprime
            '[alt_l]': '',       # Alt izquierdo
            '[alt_r]': '',       # Alt derecho
            '[caps_lock]': '',   # Bloq Mayús - no imprime
            '[escape]': '',      # Escape - no imprime
            '[delete]': '',      # Delete - borra pero no imprime
            '[home]': '',        # Inicio - no imprime
            '[end]': '',         # Fin - no imprime
            '[page_up]': '',     # Re Pág - no imprime
            '[page_down]': '',   # Av Pág - no imprime
            '[insert]': '',      # Insert - no imprime
            '[f1]': '',          # Teclas F1-F12 no imprimen nada
            '[f2]': '',
            '[f3]': '',
            '[f4]': '',
            '[f5]': '',
            '[f6]': '',
            '[f7]': '',
            '[f8]': '',
            '[f9]': '',
            '[f10]': '',
            '[f11]': '',
            '[f12]': '',
            '[left]': '',        # Flechas - no imprimen
            '[right]': '',
            '[up]': '',
            '[down]': '',
            '[num_lock]': ''     # Bloq Num - no imprime
        }
    
    def clean_and_parse_line(self, line: str) -> list:
        """
        Esta función es como un detective que examina cada línea del log.
        El problema es que el keylogger escribe de forma desordenada:
        - A veces pone [space][enter] al inicio sin timestamp
        - Otras veces pone timestamp: letra
        
        Nosotros necesitamos separar y entender cada pieza.
        """
        line = line.strip()  # Quitamos espacios en blanco al inicio y final
        if not line:  # Si la línea está vacía, no hay nada que hacer
            return []
        
        keys = []  # Aquí guardaremos todas las teclas que encontremos
        current_line = line  # Trabajamos con una copia
        
        # PASO 1: Buscar teclas especiales que aparecen pegadas al inicio
        # Por ejemplo: "[space][enter]2025-06-22 22:02:46: e"
        while True:
            found_special = False  # Bandera para saber si encontramos algo
            
            # Lista de teclas especiales que buscamos
            for special_key in ['[backspace]', '[space]', '[enter]', '[shift_r]', '[shift_l]', 
                               '[ctrl]', '[alt]', '[tab]', '[caps_lock]', '[escape]']:
                # ¿La línea actual empieza con esta tecla especial?
                if current_line.startswith(special_key):
                    keys.append(special_key)  # La guardamos
                    current_line = current_line[len(special_key):]  # La quitamos de la línea
                    found_special = True
                    break  # Salimos del for para buscar la siguiente
            
            # Si no encontramos más teclas especiales, paramos
            if not found_special:
                break
        
        # PASO 2: Si sobró algo después de quitar las teclas especiales,
        # debe ser un timestamp con un carácter normal
        if current_line:
            # Buscamos el patrón: "2025-06-22 22:02:46: x" (donde x es cualquier carácter)
            match = re.search(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}: (.)', current_line)
            if match:
                keys.append(match.group(1))  # guardamos solo el carácter, no el timestamp
        
        return keys  # devolvemos todas las teclas que encontramos
    
    def parse_log_line(self, line: str) -> list:
        """
        Esta es la función principal que lee cada línea del archivo de log.
        Es como un escáner que va carácter por carácter buscando pistas.
        
        Devuelve una lista con todas las teclas que encuentra en esa línea.
        """
        line = line.strip()  # Limpiamos la línea
        if not line:  # Si está vacía, nos vamos
            return []
        
        keys = []  # Lista donde guardaremos las teclas encontradas
        current_pos = 0  # Posición actual en la línea (empezamos desde el principio)
        
        # Vamos recorriendo la línea carácter por carácter
        while current_pos < len(line):
            found = False  # ¿Encontramos algo en esta posición?
            
            # PASO 1: ¿Hay una tecla especial aquí?
            # Checamos si en la posición actual empieza alguna tecla especial
            for special_key in ['[backspace]', '[space]', '[enter]', '[shift_r]', '[shift_l]', 
                               '[ctrl]', '[alt]', '[tab]', '[caps_lock]', '[escape]']:
                if line[current_pos:].startswith(special_key):
                    keys.append(special_key)  # ¡La encontramos! La guardamos
                    current_pos += len(special_key)  # Saltamos toda la tecla especial
                    found = True
                    break  # Ya encontramos algo, no seguimos buscando
            
            # PASO 2: Si no era tecla especial, ¿será un timestamp con carácter?
            if not found:
                # Buscamos algo como: "2025-06-22 22:02:46: a"
                match = re.search(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}: (.))', line[current_pos:])
                if match:
                    keys.append(match.group(2))  # Guardamos solo la letra 'a', no todo el timestamp
                    current_pos += len(match.group(1))  # Saltamos todo el timestamp
                    found = True
                
                # PASO 3: Si tampoco era eso, avanzamos una posición
                if not found:
                    current_pos += 1  # Nos movemos al siguiente carácter
        
        return keys  # Devolvemos todas las teclas que encontramos
    
    def process_key(self, key: str) -> str:
        """
        Esta función decide qué hacer con cada tecla individual.
        Es como un traductor: recibe una tecla y devuelve lo que debe escribirse.
        """
        if not key:  # Si no hay tecla, no hacemos nada
            return ''
            
        # ¿Es una tecla especial que conocemos?
        if key in self.special_keys:
            return self.special_keys[key]  # Usamos nuestra tabla de traducción
            
        # ¿Es un carácter normal (letra, número, símbolo)?
        if len(key) == 1:
            return key  # Lo devolvemos tal como está
            
        # ¿Es ese carácter raro que a veces sale por problemas de encoding?
        if key == '�':  # Carácter problemático que aparece a veces
            return 'a'  # Lo reemplazamos por 'a' 
            
        return ''  # Si no sabemos qué es, lo ignoramos
    
    def reconstruir_texto(self, log_path: str, output_path: Optional[str] = None, 
                         handle_backspace: bool = True, preserve_formatting: bool = True) -> str:
        """
        ¡Esta es la función estrella! Toma el archivo de log y lo convierte en texto legible.
        
        Parámetros que puedes ajustar:
        - log_path: ¿Dónde está el archivo de log?
        - output_path: ¿Dónde guardar el resultado? (opcional)
        - handle_backspace: ¿Queremos que cuando encuentre [backspace] borre el último carácter?
        - preserve_formatting: ¿Mantenemos los espacios y saltos de línea?
        
        Devuelve: El texto reconstruido como string
        """
        # Primero verificamos que el archivo exista
        if not os.path.exists(log_path):
            raise FileNotFoundError(f"No hay archivo: {log_path}")
        
        texto = ""  # Aquí iremos construyendo el texto final
        lines_processed = 0  # Contador de líneas que procesamos exitosamente
        errors = 0  # Contador de errores que encontremos
        
        try:
            # Abrimos el archivo del keylogger
            # 'errors="replace"' significa: si hay caracteres raros, reemplázalos en vez de fallar
            with open(log_path, "r", encoding="utf-8", errors="replace") as f:
                
                # Procesamos línea por línea
                for line_num, line in enumerate(f, 1):  # enumerate nos da el número de línea
                    try:
                        # Extraemos todas las teclas de esta línea
                        keys = self.parse_log_line(line)
                        if not keys:  # Si no hay teclas válidas, saltamos esta línea
                            continue
                            
                        lines_processed += 1  # Contamos esta línea como procesada
                        
                        # Ahora procesamos cada tecla individual que encontramos
                        for key in keys:
                            # CASO ESPECIAL: ¿Es un backspace?
                            if key == '[backspace]' and handle_backspace:
                                if texto:  # Solo si hay algo que borrar
                                    texto = texto[:-1]  # Quitamos el último carácter
                                continue  # Siguiente tecla, no agregar nada al texto
                            
                            # CASO NORMAL: Convertir la tecla a su carácter correspondiente
                            char = self.process_key(key)
                            
                            # ¿Debemos agregar este carácter?
                            if preserve_formatting or (char not in ['\n', '\t'] if not preserve_formatting else True):
                                texto += char  # Lo agregamos al texto final
                            
                    except Exception as e:
                        # Si algo sale mal con esta línea, la contamos como error pero seguimos
                        errors += 1
                        print(f"Error procesando línea {line_num}: {e}")
                        continue  # Siguiente línea
        
        except Exception as e:
            # Si el archivo no se puede leer para nada, es un error grave
            raise Exception(f"Error leyendo el archivo: {e}")
        
        # guardar el resultado en un archivo
        if output_path:
            try:
                with open(output_path, "w", encoding="utf-8") as out:
                    out.write(texto)
                print(f"✅ Texto reconstruido guardado en: {output_path}")
            except Exception as e:
                print(f"❌ Error guardando archivo: {e}")
                raise Exception(f"Error guardando el archivo de salida: {e}")
        
        return texto  # Devolvemos el texto final
    
    def get_statistics(self, log_path: str) -> dict:
        """
        Función curiosa que analiza el archivo de log y te dice datos interesantes.
        ¿Cuántas líneas tiene? ¿Cuántas teclas? ¿En qué fechas se grabó?
        """
        # Diccionario donde guardaremos todas las estadísticas
        stats = {
            'total_lines': 0,      # Total de líneas en el archivo
            'valid_keys': 0,       # Cuántas teclas válidas encontramos
            'special_keys': 0,     # Cuántas eran teclas especiales (space, enter, etc.)
            'characters': 0,       # Cuántas eran caracteres normales (a, b, 1, 2, etc.)
            'date_range': {'start': None, 'end': None}  # Primera y última fecha del log
        }
        
        # Si el archivo no existe, devolvemos estadísticas vacías
        if not os.path.exists(log_path):
            return stats
            
        try:
            with open(log_path, "r", encoding="utf-8", errors="replace") as f:
                for line in f:
                    stats['total_lines'] += 1  # Contamos esta línea
                    
                    # ¿Hay una fecha en esta línea?
                    date_match = re.search(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})', line)
                    if date_match:
                        date_str = date_match.group(1)
                        # Si es la primera fecha que vemos, la guardamos como inicio
                        if stats['date_range']['start'] is None:
                            stats['date_range']['start'] = date_str
                        # Siempre actualizamos la fecha final (así tendremos la última)
                        stats['date_range']['end'] = date_str
                    
                    # Analizar las teclas de esta línea
                    key = self.parse_log_line(line)
                    if key:
                        stats['valid_keys'] += len(key)  # Contamos cuántas teclas encontramos
                        for k in key:
                            if k in self.special_keys:
                                stats['special_keys'] += 1  # Es una tecla especial
                            elif len(k) == 1:
                                stats['characters'] += 1  # Es un carácter normal
        except Exception as e:
            print(f"Error obteniendo estadísticas: {e}")
            
        return stats

def main():

    #  reconstructor
    reconstructor = TextReconstructor()
    
    # Obtenemos la ruta del directorio donde está este script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Definimos los archivos que vamos a usar
    log_file = os.path.join(script_dir, "key_log.txt")      
    output_file = os.path.join(script_dir, "texto_concatenado.txt")  
    
    try:
        # Estadísticas curiosas del archivo
        print("🔍 === ESTADÍSTICAS DEL LOG ===")
        stats = reconstructor.get_statistics(log_file)
        print(f"📄 Total de líneas: {stats['total_lines']}")
        print(f"⌨️  Teclas válidas: {stats['valid_keys']}")
        print(f"🎯 Teclas especiales: {stats['special_keys']}")
        print(f"🔤 Caracteres: {stats['characters']}")
        if stats['date_range']['start']:
            print(f"📅 Rango de fechas: {stats['date_range']['start']} ➜ {stats['date_range']['end']}")
        print()
        
        # Reconstruir el texto
        print("🔄 === RECONSTRUYENDO TEXTO ===")
        resultado = reconstructor.reconstruir_texto(
            log_path=log_file,           # De dónde leer
            output_path=output_file,     # Dónde guardar
            handle_backspace=True,       # Sí, manejar backspaces
            preserve_formatting=True     # Sí, mantener espacios y saltos de línea
        )
        
        # Preview de lo que obtuvimos
        print("\n👁️ === PREVIEW DEL TEXTO RECONSTRUIDO ===")
        # Si el texto es muy largo, solo mostramos los primeros 200 caracteres
        preview = resultado[:200] + "..." if len(resultado) > 200 else resultado
        print(repr(preview))  # repr() nos muestra los \n y espacios claramente
        
    except Exception as e:
        print(f"💥 Error: {e}")

if __name__ == "__main__":

    main()