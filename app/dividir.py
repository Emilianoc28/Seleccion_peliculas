import os

# Ruta del archivo CSV
CSV_FILE_PATH = "data/movies_dataset_cleaned.csv"

# Función para dividir el archivo CSV en tres partes de tamaño aproximado
def dividir_csv_tamano():
    # Obtener el tamaño total del archivo en bytes
    archivo_tamano = os.path.getsize(CSV_FILE_PATH)  # Tamaño en bytes
    tamano_parte = archivo_tamano // 3  # Dividir entre 3 para obtener tamaño de cada parte
    
    # Inicializar variables para las partes
    parte_1 = []
    parte_2 = []
    parte_3 = []
    
    # Leer el archivo por partes basándonos en el tamaño
    with open(CSV_FILE_PATH, 'r', encoding='latin1') as archivo:
        # Leer la primera parte
        parte_1_size = 0
        for line in archivo:
            parte_1_size += len(line.encode('latin1'))  # Obtener tamaño en bytes de cada línea
            parte_1.append(line)
            if parte_1_size >= tamano_parte:
                break
        
        # Leer la segunda parte
        parte_2_size = 0
        for line in archivo:
            parte_2_size += len(line.encode('latin1'))
            parte_2.append(line)
            if parte_2_size >= tamano_parte:
                break
        
        # Leer la tercera parte
        parte_3 = archivo.readlines()  # Resto del archivo

    # Guardar las tres partes en nuevos archivos CSV
    with open("data/movies_parte_1.csv", 'w', encoding='utf-8') as f:
        f.writelines(parte_1)
        
    with open("data/movies_parte_2.csv", 'w', encoding='utf-8') as f:
        f.writelines(parte_2)

    with open("data/movies_parte_3.csv", 'w', encoding='utf-8') as f:
        f.writelines(parte_3)

    print("El archivo CSV ha sido dividido en tres partes.")

# Llamar a la función para dividir el CSV
dividir_csv_tamano()
