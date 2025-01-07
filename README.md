# 🎬 Sistema de Recomendación de Películas 🎥

Este proyecto utiliza Machine Learning para recomendar películas basándose en géneros seleccionados por los usuarios,
con un dashboard interactivo que muestra información clave de las películas.

---

## Características ✨

- 🔍 Recomendación de películas por género y año.
- 📊 Dashboard interactivo para explorar datos.
- 🕒 Animación de popularidad a lo largo del tiempo.
- 🌐 API accesible y bien documentada.

---

## Tecnologías Utilizadas

- Python 3.9
- FastAPI
- Streamlit
- Matplotlib y Seaborn para visualizaciones
- Pandas y NumPy para procesamiento de datos
- Scikit-learn para modelos de Machine Learning

---

## Instalación:

1. Clona este repositorio:
   ```bash
   git clone https://github.com/Emilianoc28/MVP-MOVIE-V2
   ```
2. Navega al directorio del proyecto:
   ```bash
   cd repo
   ```
3. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```
4. Ejecuta la API:
   ```bash
   uvicorn app.main:app --reload
   ```
5. Ejecuta el dashboard:

   ```bash
   streamlit run dashboard.py

   ```

---

## Uso

1. Accede a la API en `http://127.0.0.1:8000/docs` para ver los endpoints disponibles.
2. Abre el dashboard interactivo en tu navegador y selecciona un género para obtener recomendaciones.

## Estructura del proyecto

├── app/
│ ├── data/ # Dataset dividido en partes
├── main.py # Código de la API
├── dashboard.py # Código del dashboard interactivo
├── requirements.txt # Dependencias del proyecto
├── README.md # Este archivo
├── popularidad_peliculas.gif # Grafica con la popularidad de las peliculas a lo largo del tiempo
├── EDA.ipynb # Análisis Exploratorio de Datos (EDA)
├── ML.ipynb # Modelo de ML

---

## Autor

- Caldera Emiliano Exequiel - [GitHub Profile](https://github.com/Emilianoc28)

---
