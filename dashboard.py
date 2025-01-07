import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Cargar el dataset sin caché para asegurarnos de que se actualice correctamente
def load_data():
    # Combinar las partes del dataset
    movies_part_1 = pd.read_csv(r"D:\Soy Henry\Labs\MVP Peliculas\app\MVP-MOVIE-V2\app\data\movies_parte_1.csv")
    movies_part_2 = pd.read_csv(r"D:\Soy Henry\Labs\MVP Peliculas\app\MVP-MOVIE-V2\app\data\movies_parte_2.csv")
    movies_part_3 = pd.read_csv(r"D:\Soy Henry\Labs\MVP Peliculas\app\MVP-MOVIE-V2\app\data\movies_parte_3.csv")
    movies = pd.concat([movies_part_1, movies_part_2, movies_part_3], ignore_index=True)
    movies['title'] = movies['title'].fillna('')
    movies['genres'] = movies['genres'].fillna('')
    # Filtrar las 1000 películas más populares
    movies = movies.sort_values(by="popularity", ascending=False).head(1000)
    return movies

movies = load_data()

# Crear matriz TF-IDF solo para las 1000 películas más populares
def compute_tfidf_matrix(movies):
    tfidf = TfidfVectorizer(stop_words='english')
    return tfidf.fit_transform(movies['title'])

tfidf_matrix = compute_tfidf_matrix(movies)
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

# Función de recomendación basada en género
def recomendar_peliculas_por_genero(genero, n=5):
    # Filtrar las películas por género
    genre_movies = movies[movies['genres'].str.contains(genero, case=False, na=False)]

    if genre_movies.empty:
        st.error(f"No se encontraron películas con el género '{genero}'.")
        return []

    # Crear una nueva matriz de similitud solo para las películas filtradas por género
    tfidf_matrix_genre = compute_tfidf_matrix(genre_movies)
    cosine_sim_genre = cosine_similarity(tfidf_matrix_genre, tfidf_matrix_genre)

    # Ordenar las puntuaciones de similitud y obtener los índices de las películas más similares
    sim_scores = list(enumerate(cosine_sim_genre[0]))  # Empezamos con la primera película del género
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Obtener los índices de las películas recomendadas dentro del mismo género
    movie_indices = [i[0] for i in sim_scores[1:n+1]]  # Excluimos la película seleccionada (índice 0)

    # Asegurarse de que las recomendaciones estén dentro de las 1000 películas populares
    movie_indices = [i for i in movie_indices if i < len(movies)]  # Eliminar índices fuera de rango

    # Filtrar las recomendaciones para que solo estén entre las 1000 más populares
    recommended_titles = genre_movies['title'].iloc[movie_indices].tolist()

    return recommended_titles

# Interfaz del dashboard
st.title("Sistema de Recomendación de Películas")
st.markdown("### Explora y encuentra películas similares según el género")

# Entrada del usuario - Limitar el selectbox a los géneros únicos disponibles en las 1000 películas más populares
# Extraer géneros únicos de las películas
generos_disponibles = set()
for genres_list in movies['genres']:
    generos_disponibles.update(genres_list.split('|'))  # Agregar los géneros de cada película
generos_disponibles = sorted(generos_disponibles)  # Ordenar los géneros alfabéticamente

# Seleccionar un género
selected_genre = st.selectbox("Selecciona un género", generos_disponibles)

# Botón para generar recomendaciones
if st.button("Recomendar"):
    if selected_genre:
        recomendaciones = recomendar_peliculas_por_genero(selected_genre)
        if len(recomendaciones) == 0:
            st.error("No se encontraron recomendaciones.")
        else:
            st.write("### Películas recomendadas:")
            for i, rec in enumerate(recomendaciones, start=1):
                st.write(f"{i}. {rec}")
    else:
        st.error("Por favor, selecciona un género.")

st.sidebar.markdown("### Opciones")
st.sidebar.markdown("Este tablero interactivo utiliza Streamlit para visualizar recomendaciones basadas en géneros.")




#streamlit run dashboard.py

