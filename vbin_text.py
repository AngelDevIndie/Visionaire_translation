# Script para extraer texto de .po y modificar el .dat de un vbin (visionaire)


# Importamos liberías
import sys
import re

# Función para abrir el archivo .po en modo texto
def abrir_archivo(nombre_archivo):
    """Abre un archivo en modo texto y devuelve su contenido."""
    try:
        with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
            contenido = archivo.readlines()
            return contenido
    except FileNotFoundError:
        print(f"Error: El archivo '{nombre_archivo}' no se encuentra.")
        sys.exit(1)
    except IOError:
        print(f"Error: No se puede abrir el archivo '{nombre_archivo}'.")
        sys.exit(1)

# Función para abrir el archivo .dat
def abrir_archivo_binario(nombre_archivo):
    """Abre un archivo en modo binario y devuelve su contenido."""
    try:
        with open(nombre_archivo, 'rb') as archivo:
            contenido = archivo.read()  # Leer todo el contenido
            return contenido
    except FileNotFoundError:
        print(f"Error: El archivo binario '{nombre_archivo}' no se encuentra.")
        sys.exit(1)
    except IOError:
        print(f"Error: No se puede abrir el archivo binario '{nombre_archivo}'.")
        sys.exit(1)

def buscar_id_traduccion(contenido):
    """Busca la cadena '# active language:' y extrae el id de la traducción."""
    traducciones = {}
    for i, linea in enumerate(contenido):
        if "# active language:" in linea:
            # Expresión regular para encontrar la línea que contiene '# active language:'
            patron = r"# active language:.*?id:\s*(\d+)"
            coincidencia = re.search(patron, linea)
            if coincidencia:
                traducciones[i] = coincidencia.group(1)  # Almacena el id encontrado con el índice de la línea

    return traducciones

def extraer_texto_entre_comillas(linea):
    """Extrae el texto entre la primera y la última comilla doble de una línea."""
    primera_comilla = linea.find('"')
    ultima_comilla = linea.rfind('"')
    
    if primera_comilla != -1 and ultima_comilla != -1 and primera_comilla != ultima_comilla:
        return linea[primera_comilla + 1:ultima_comilla]
    return None  # Retorna None si no se encuentran comillas válidas

def buscar_ids(contenido):
    """Busca la cadena '#: id:' y extrae los números hasta el final de la línea, junto con el msgid y msgstr."""
    ids_dict = {}
    for i, linea in enumerate(contenido):
        # Verificar si la línea contiene la cadena '#: id:'
        if "#: id:" in linea:
            # Expresión regular para extraer los números
            patron = r"#:\s*id:\s*([\d\s,]+)"
            coincidencia = re.search(patron, linea)
            if coincidencia:
                # Separar los números por comas y eliminar espacios
                numeros = [num.strip() for num in coincidencia.group(1).split(',')]
                
                # Buscar la línea que contiene 'msgid'
                msgid_texto = None
                msgstr_texto = None
                
                # Buscar la primera línea después de la línea actual que contenga 'msgid'
                for j in range(i + 1, len(contenido)):
                    if 'msgid' in contenido[j]:
                        msgid_texto = extraer_texto_entre_comillas(contenido[j])
                        
                        # Ahora buscar la línea siguiente que contenga 'msgstr'
                        if j + 1 < len(contenido) and 'msgstr' in contenido[j + 1]:
                            msgstr_texto = extraer_texto_entre_comillas(contenido[j + 1])
                            break  # Salir del bucle después de encontrar msgid y msgstr

                ids_dict[i] = [numeros, msgid_texto, msgstr_texto]  # Almacena el ID, msgid y msgstr

    return ids_dict

def modificar_contenido_binario(contenido_binario):
    """Realiza modificaciones en el contenido binario y devuelve el nuevo contenido."""
    # Aquí puedes realizar las modificaciones necesarias en el contenido binario
    # Por ejemplo, simplemente retornamos el contenido sin cambios, pero puedes implementar la lógica que necesites
    return contenido_binario  # Retorna el contenido modificado

def guardar_archivo_binario(nombre_archivo, contenido):
    """Guarda el contenido en un archivo binario."""
    try:
        with open(nombre_archivo, 'wb') as archivo:
            archivo.write(contenido)  # Escribir el contenido modificado
    except IOError:
        print(f"Error: No se puede guardar el archivo binario '{nombre_archivo}'.")
        sys.exit(1)

def buscar_ids_en_contenido_binario(contenido_binario, ids_dict):
    """Busca en el contenido binario la cadena 'Id: ' seguida de cada ID del array ids_dict."""
    posiciones_encontradas = {}
    for clave, valores in ids_dict.items():
        for id in valores[0]:  # Iterar sobre los IDs
            id_bytes = f"Id: {id}".encode('utf-8')  # Convertir a bytes
            posicion = contenido_binario.find(id_bytes)  # Buscar la posición en el contenido binario
            if posicion != -1:
                posiciones_encontradas[id] = posicion  # Almacenar la posición encontrada
            else:
                posiciones_encontradas[id] = 0

    return posiciones_encontradas

# Programa principal
def main():
    # Presentación del script
    print ("\n")
    print ("Script para modificar el texto de un .dat extraido de un vbin (visionaire)      v.0.1.0\n")
    # Mostramos los argumentos que se pasan donde se espera el archivo .po y el .dat
    # Comprobar que se han pasado exactamente 2 argumentos
    if len(sys.argv) != 3:
        print("Error: Se requieren exactamente 2 argumentos.")
        print("Uso: python vbin_text.py 'archivo.po' 'archivo.dat'")
        sys.exit(1)  # Salir con un código de error

    # Obtener los argumentos
    nombre_archivo_po = sys.argv[1]
    nombre_archivo_dat = sys.argv[2]

    # Mostrar los argumentos
    # print("Argumento 1:", arg1)
    # print("Argumento 2:", arg2)

    # Inicializamos las variables
    forzarTraduccion = 0

    # Abrir el archivo
    contenido = abrir_archivo(nombre_archivo_po)
    # print("Contenido del archivo:")
    # print(contenido)

    # Buscar el id de traducción
    ids_traduccion = buscar_id_traduccion(contenido)

    if ids_traduccion:
        print("IDs de traducción encontrados:")
        for clave, valor in ids_traduccion.items():
            print(f"Línea {clave}: {valor}")

    # Buscar los IDs
    ids_dict = buscar_ids(contenido)

    if ids_dict:
        print("IDs encontrados:")
        for clave, valores in ids_dict.items():
            print(f"Línea {clave}: ID(s) {valores[0]}, msgid: '{valores[1]}', msgstr: '{valores[2]}'")
    else:
        print("No se encontraron IDs.") 

    # Abrir el archivo binario y realizar modificaciones
    contenido_binario = abrir_archivo_binario(nombre_archivo_dat)
    contenido_modificado = modificar_contenido_binario(contenido_binario)

    # Guardar el contenido modificado en un nuevo archivo binario
    guardar_archivo_binario("archivo_modificado.bin", contenido_modificado)

    # Buscar IDs en el contenido binario
    posiciones = buscar_ids_en_contenido_binario(contenido_binario, ids_dict)
    if posiciones:
        print("\nPosiciones encontradas en el contenido binario:")
        for id, posicion in posiciones.items():
            print(f"ID: {id} encontrado en la posición: {posicion:#x}")
    else:
        print("No se encontraron IDs en el contenido binario.")

if __name__ == "__main__":
    main()