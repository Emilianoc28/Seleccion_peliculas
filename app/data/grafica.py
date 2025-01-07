import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
import pandas as pd

# Cargar datos combinados
movies_part_1 = pd.read_csv(r"D:\Soy Henry\Labs\MVP Peliculas\app\MVP-MOVIE-V2\app\data\movies_parte_1.csv")
movies_part_2 = pd.read_csv(r"D:\Soy Henry\Labs\MVP Peliculas\app\MVP-MOVIE-V2\app\data\movies_parte_2.csv")
movies_part_3 = pd.read_csv(r"D:\Soy Henry\Labs\MVP Peliculas\app\MVP-MOVIE-V2\app\data\movies_parte_3.csv")

# Unir los datasets
movies = pd.concat([movies_part_1, movies_part_2, movies_part_3])

# Convertir release_year a numérico
movies['release_year'] = pd.to_numeric(movies['release_year'], errors='coerce')

# Filtrar datos con años válidos
movies = movies[movies['release_year'].notna()]

# Ordenar por año y popularidad
movies = movies.sort_values(by=['release_year', 'popularity'], ascending=[True, False])

# Seleccionar columnas necesarias
movies_trimmed = movies[['title', 'release_year', 'popularity']]

# Crear la animación
fig, ax = plt.subplots(figsize=(12, 8))

def update(frame):
    ax.clear()
    year = frame
    data = movies_trimmed[movies_trimmed['release_year'] == year].head(10)
    ax.barh(data['title'], data['popularity'], color='skyblue')
    ax.set_title(f"Popularidad de Películas - Año {year}")
    ax.set_xlabel("Popularidad")
    ax.set_ylabel("Películas")
    ax.invert_yaxis()

years = sorted(movies_trimmed['release_year'].unique())
ani = FuncAnimation(fig, update, frames=years, repeat=False, interval=1000)

# Guardar la animación como GIF
ani = FuncAnimation(fig, update, frames=years, repeat=False, interval=100)  # 300 ms por cuadro
ani.save('popularidad_peliculas.gif', writer=PillowWriter(fps=1))

# Mostrar la animación
from IPython.display import Image
Image(filename='popularidad_peliculas.gif')

