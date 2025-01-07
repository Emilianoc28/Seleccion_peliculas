from fastapi import FastAPI
import pandas as pd

app = FastAPI()

# Rutas de los archivos CSV divididos
CSV_PART_1 = "app/data/movies_parte_1.csv"
CSV_PART_2 = "app/data/movies_parte_2.csv"
CSV_PART_3 = "app/data/movies_parte_3.csv"

# Cargar los datos de los tres archivos CSV al iniciar la aplicación
try:
    movies_part_1 = pd.read_csv(CSV_PART_1, encoding='latin1')
    movies_part_2 = pd.read_csv(CSV_PART_2, encoding='latin1')
    movies_part_3 = pd.read_csv(CSV_PART_3, encoding='latin1')
except Exception as e:
    print(f"Error al cargar los archivos CSV: {e}")
    movies_part_1 = movies_part_2 = movies_part_3 = pd.DataFrame()  # DataFrame vacío si falla la carga

@app.get("/")
def read_root():
    return {"message": "¡API funcionando!"}

@app.get("/cantidad_filmaciones_anio/{anio}")
def cantidad_filmaciones_anio(anio: int):
    """
    Endpoint para calcular la cantidad de películas estrenadas en un año específico.
    """
    # Filtrar las películas cuyo año de estreno coincida con el año proporcionado en las tres partes
    peliculas_anio_part_1 = movies_part_1[movies_part_1['release_year'] == anio]
    peliculas_anio_part_2 = movies_part_2[movies_part_2['release_year'] == anio]
    peliculas_anio_part_3 = movies_part_3[movies_part_3['release_year'] == anio]
    
    # Concatenar los resultados de las tres partes
    peliculas_anio = pd.concat([peliculas_anio_part_1, peliculas_anio_part_2, peliculas_anio_part_3])
    
    # Contar la cantidad de películas
    cantidad = peliculas_anio.shape[0]
    
    # Retornar la respuesta en formato JSON
    return {"anio": anio, "cantidad": cantidad}

@app.get("/primeras_filas/")
def obtener_primeras_filas():
    """
    Endpoint para obtener las primeras 5 filas combinadas de los tres archivos CSV.
    """
    # Obtener las primeras 5 filas de cada parte y combinarlas
    primeras_filas_part_1 = movies_part_1.head()
    primeras_filas_part_2 = movies_part_2.head()
    primeras_filas_part_3 = movies_part_3.head()
    
    # Concatenar las primeras filas
    primeras_filas = pd.concat([primeras_filas_part_1, primeras_filas_part_2, primeras_filas_part_3])
    
    # Convertir a diccionario para la respuesta JSON
    return primeras_filas.to_dict(orient="records")

@app.get("/promedio_votos_anio/{anio}")
def promedio_votos_anio(anio: int):
    """
    Endpoint para calcular el promedio de votos de películas de un año específico.
    """
    peliculas_anio_part_1 = movies_part_1[movies_part_1['release_year'] == anio]
    peliculas_anio_part_2 = movies_part_2[movies_part_2['release_year'] == anio]
    peliculas_anio_part_3 = movies_part_3[movies_part_3['release_year'] == anio]
    
    # Concatenar los resultados de las tres partes
    peliculas_anio = pd.concat([peliculas_anio_part_1, peliculas_anio_part_2, peliculas_anio_part_3])
    
    if peliculas_anio.empty:
        return {"mensaje": "No hay películas para este año"}
    
    promedio = peliculas_anio['vote_average'].mean()
    return {"anio": anio, "promedio_votos": promedio}

@app.get("/peliculas_populares")
def peliculas_populares():
    """
    Endpoint para obtener las 5 películas más populares.
    """
    # Concatenar todas las partes de películas y luego obtener las 5 más populares
    todas_las_peliculas = pd.concat([movies_part_1, movies_part_2, movies_part_3])
    peliculas_populares = todas_las_peliculas.nlargest(5, 'popularity')
    
    return peliculas_populares[['title', 'popularity']].to_dict(orient="records")

@app.get("/peliculas_por_idioma/{idioma}")
def peliculas_por_idioma(idioma: str):
    """
    Endpoint para obtener películas que están disponibles en un idioma específico.
    """
    # Concatenar todas las partes de películas y luego filtrar por idioma
    todas_las_peliculas = pd.concat([movies_part_1, movies_part_2, movies_part_3])
    peliculas_idioma = todas_las_peliculas[todas_las_peliculas['languages'].str.contains(idioma, case=False, na=False)]
    
    if peliculas_idioma.empty:
        return {"mensaje": "No se encontraron películas en este idioma"}
    
    return peliculas_idioma[['title', 'languages']].to_dict(orient="records")

@app.get("/peliculas_por_voto/{min_voto}/{max_voto}")
def peliculas_por_voto(min_voto: float, max_voto: float):
    """
    Endpoint para obtener películas cuyo promedio de votos esté en un rango específico.
    """
    # Concatenar todas las partes de películas y luego filtrar por el rango de votos
    todas_las_peliculas = pd.concat([movies_part_1, movies_part_2, movies_part_3])
    peliculas_rango_voto = todas_las_peliculas[(todas_las_peliculas['vote_average'] >= min_voto) & 
                                               (todas_las_peliculas['vote_average'] <= max_voto)]
    
    if peliculas_rango_voto.empty:
        return {"mensaje": "No se encontraron películas en este rango de votos"}
    
    return peliculas_rango_voto[['title', 'vote_average']].to_dict(orient="records")
