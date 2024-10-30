import streamlit as st
import pandas as pd
import numpy as np

# Configuración inicial de Streamlit
st.set_page_config(page_title="Análisis de Inmuebles en pisos.com", page_icon="🏠", layout="wide")

# Título de la aplicación
st.title("Análisis de Inmuebles en pisos.com")

# Función para cargar y limpiar datos desde archivos CSV
@st.cache_data
def cargar_datos(tipo):
    if tipo == "Alquiler":
        data_path = "alquiler_inmuebles_limpio.csv"
    else:
        data_path = "venta_inmuebles_limpio.csv"
    data = pd.read_csv(data_path)
    data.columns = data.columns.str.lower()  # Convertir nombres de columnas a minúsculas

    # Limpiar y convertir columnas numéricas
    if "precio" in data.columns:
        data["precio"] = pd.to_numeric(data["precio"], errors='coerce')
    if "superficie construida" in data.columns:
        data["superficie construida"] = pd.to_numeric(data["superficie construida"], errors='coerce')
    if "habitaciones" in data.columns:
        data["habitaciones"] = pd.to_numeric(data["habitaciones"], errors='coerce')  # Convertir a número y forzar NaN en caso de error
    if "baños" in data.columns:
        data["baños"] = pd.to_numeric(data["baños"], errors='coerce')  # Convertir a número y forzar NaN en caso de error

    # Ajustar nombres de columna para que se mantengan consistentes después de limpieza
    data.columns = [col.capitalize() for col in data.columns]  # Capitalizar para que "Habitaciones" esté bien
    return data

# Selección entre datos de Alquiler o Venta
tipo_datos = st.sidebar.radio("Selecciona el tipo de datos a visualizar", ["Alquiler", "Venta"])

# Cargar y limpiar los datos según la selección
data = cargar_datos(tipo_datos)

# Filtros básicos
st.sidebar.header("Filtros de búsqueda")
if "Precio" in data.columns:
    if tipo_datos == "Alquiler":
        precio_min = st.sidebar.slider("Precio mínimo (€)", 500, 20000, 1000, step=500)
        precio_max = st.sidebar.slider("Precio máximo (€)", 500, 20000, 3000, step=500)
    else:
        precio_min = st.sidebar.slider("Precio mínimo (€)", 50000, 1000000, 200000, step=50000)
        precio_max = st.sidebar.slider("Precio máximo (€)", 50000, 1000000, 500000, step=50000)

    data = data[(data["Precio"] >= precio_min) & (data["Precio"] <= precio_max)]

# Filtro de superficie construida
if "Superficie construida" in data.columns:
    superficie_min = st.sidebar.slider("Superficie mínima (m²)", 10, 1000, 50, step=10)
    superficie_max = st.sidebar.slider("Superficie máxima (m²)", 10, 1000, 200, step=10)
    data = data[(data["Superficie construida"] >= superficie_min) & (data["Superficie construida"] <= superficie_max)]

# Mostrar datos filtrados
st.subheader(f"Resultados Filtrados - {tipo_datos}")
st.write(data)

# Comparador de Alquiler vs Venta
st.subheader("Comparador Alquiler vs Venta")

# Cargar ambos datasets para la comparación y limpiar
alquiler_data = cargar_datos("Alquiler")
venta_data = cargar_datos("Venta")

# Verificar la existencia de columnas clave en ambos datasets
comparacion = pd.DataFrame({"Tipo": ["Alquiler", "Venta"]})

if "Precio" in alquiler_data.columns and "Precio" in venta_data.columns:
    comparacion["Precio Promedio (€)"] = [alquiler_data["Precio"].mean(), venta_data["Precio"].mean()]
else:
    st.warning("La columna 'Precio' no está disponible en uno de los conjuntos de datos.")

if "Superficie construida" in alquiler_data.columns and "Superficie construida" in venta_data.columns:
    comparacion["Superficie Promedio Construida (m²)"] = [
        alquiler_data["Superficie construida"].mean(),
        venta_data["Superficie construida"].mean()
    ]
else:
    st.warning("La columna 'Superficie construida' no está disponible en uno de los conjuntos de datos.")

if "Habitaciones" in alquiler_data.columns and "Habitaciones" in venta_data.columns:
    comparacion["Número Promedio de Habitaciones"] = [
        alquiler_data["Habitaciones"].mean(),
        venta_data["Habitaciones"].mean()
    ]
else:
    st.warning("La columna 'Habitaciones' no está disponible en uno de los conjuntos de datos.")

if "Baños" in alquiler_data.columns and "Baños" in venta_data.columns:
    comparacion["Número Promedio de Baños"] = [
        alquiler_data["Baños"].mean(),
        venta_data["Baños"].mean()
    ]
else:
    st.warning("La columna 'Baños' no está disponible en uno de los conjuntos de datos.")

st.write(comparacion)

# Gráficos comparativos (solo mostrar gráficos si las columnas existen en ambos datasets)
if "Precio Promedio (€)" in comparacion.columns:
    st.write("Comparación de Precio Promedio entre Alquiler y Venta")
    st.bar_chart(comparacion.set_index("Tipo")[["Precio Promedio (€)"]])

if "Superficie Promedio Construida (m²)" in comparacion.columns:
    st.write("Comparación de Superficie Construida Promedio entre Alquiler y Venta")
    st.bar_chart(comparacion.set_index("Tipo")[["Superficie Promedio Construida (m²)"]])

if "Número Promedio de Habitaciones" in comparacion.columns:
    st.write("Comparación de Número Promedio de Habitaciones entre Alquiler y Venta")
    st.bar_chart(comparacion.set_index("Tipo")[["Número Promedio de Habitaciones"]])

# Mostrar mapa de ubicaciones si hay coordenadas
if "Latitude" in data.columns and "Longitude" in data.columns:
    st.subheader("Mapa de Ubicaciones")
    st.map(data[["Latitude", "Longitude"]])




