import streamlit as st
import pandas as pd
import sqlite3

# Configuración de la apariencia de la aplicación
st.set_page_config(page_title="Plataforma de Vacantes para Personas con Discapacidad", layout="wide")

# Colores personalizados
color_titulo = "#003366"  # Azul oscuro para el título
color_primario = "#004d99"  # Azul marino
color_secundario = "#003366"  # Azul oscuro
color_terciario = "#2F4F4F"  # Azul acero (Steel Blue)
color_fondo_formulario = "#004d99"  # Fondo azul para el formulario
color_texto_formulario = "#FFFFFF"  # Color de texto blanco para el fondo azul

# Colores oscuros para mensajes
color_fondo_exito = "#005f00"  # Verde oscuro para éxito
color_fondo_advertencia = "#8B0000"  # Rojo oscuro para advertencias

# Título de la aplicación con estilo mejorado
st.markdown(
    f"""
    <h1 style='text-align: center; color: {color_titulo}; font-family: "Helvetica Neue", sans-serif; font-weight: bold;'>Plataforma de Vacantes para Personas con Discapacidad</h1>
    """,
    unsafe_allow_html=True
)

# Cargar la data de Vacantes
ruta_archivo = "C:\\Estadística UNMSM\\PROYECTO ETL\\DISCAPACITADOS\\DD_VACANTES.xlsx"
data = pd.read_excel(ruta_archivo)

# Subtítulo para filtrar vacantes
st.markdown(f"<h2 style='color: {color_secundario}; font-weight: bold;'>Filtrar Vacantes</h2>", unsafe_allow_html=True)

# Crear columnas para la búsqueda y los resultados
col1, col2 = st.columns(2)  # Ambas columnas del mismo tamaño

# Sección de búsqueda
with col1:
    # Obtener los sectores, departamentos y experiencia únicos
    sectores = data['SECTOR'].unique()
    departamentos = data['DEPARTAMENTO'].unique()
    experiencia = ["", "SI", "NO", "NO PRECISA"]

    # Etiquetas personalizadas para cada selección
    st.markdown(f"<h3 style='color: {color_secundario}; font-size: 20px; font-weight: bold;'>Selecciona un sector:</h3>", unsafe_allow_html=True)
    sector_seleccionado = st.selectbox("", [""] + list(sectores), key="sector", label_visibility="collapsed")

    st.markdown(f"<h3 style='color: {color_secundario}; font-size: 20px; font-weight: bold;'>Selecciona un departamento:</h3>", unsafe_allow_html=True)
    departamento_seleccionado = st.selectbox("", [""] + list(departamentos), key="departamento", label_visibility="collapsed")

    st.markdown(f"<h3 style='color: {color_secundario}; font-size: 20px; font-weight: bold;'>¿Se necesita experiencia?</h3>", unsafe_allow_html=True)
    experiencia_necesaria = st.selectbox("", experiencia, key="experiencia", label_visibility="collapsed")

    # Botón para mostrar vacantes filtradas
    if st.button("Buscar Vacantes"):
        # Filtrar el DataFrame según las selecciones
        filtrado = data.copy()
        if sector_seleccionado:
            filtrado = filtrado[filtrado['SECTOR'] == sector_seleccionado]
        if departamento_seleccionado:
            filtrado = filtrado[filtrado['DEPARTAMENTO'] == departamento_seleccionado]
        if experiencia_necesaria:
            filtrado = filtrado[filtrado['SINEXPERIENCIA'] == experiencia_necesaria]

        # Almacenar el DataFrame filtrado en el estado de la aplicación
        st.session_state.filtrado = filtrado

# Sección de resultados
with col2:
    st.markdown(f"<h2 style='color: {color_secundario}; font-weight: bold;'>Vacantes Disponibles</h2>", unsafe_allow_html=True)
    
    # Mostrar los resultados filtrados
    if 'filtrado' in st.session_state:
        if not st.session_state.filtrado.empty:
            # Agrega las columnas 'PROVINCIA' y 'DISTRITO' al conjunto de columnas que deseas mostrar
            st.dataframe(st.session_state.filtrado[['SECTOR', 'VACANTES', 'DEPARTAMENTO', 'PROVINCIA', 'DISTRITO', 'POSTULANTES']].style.set_table_attributes('style="font-size: 16px; text-align: left;"'))
        else:
            st.markdown(f"<p style='color: {color_primario}; font-size: 16px;'>No se encontraron vacantes que coincidan con los criterios seleccionados.</p>", unsafe_allow_html=True)

# Función para conectar a la base de datos SQLite y crear la tabla si no existe
def conectar_sqlite():
    connection = sqlite3.connect("contactos.db")
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS contactos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telefono TEXT,
            correo TEXT,
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    connection.commit()
    return connection

# Función para guardar el contacto en SQLite
def guardar_contacto(telefono, correo):
    connection = conectar_sqlite()
    cursor = connection.cursor()
    try:
        cursor.execute("INSERT INTO contactos (telefono, correo) VALUES (?, ?)", (telefono, correo))
        connection.commit()
        return True
    except Exception as e:
        st.error("Error al guardar la información de contacto: " + str(e))
        return False
    finally:
        cursor.close()
        connection.close()

# Sección "Contáctanos"
st.markdown("<h2 style='text-align: center; color: #003366;'>Contáctanos</h2>", unsafe_allow_html=True)

with st.form("contact_form"):
    # Campos de teléfono y correo electrónico
    st.markdown(
        f"<div style='background-color: {color_fondo_formulario}; padding: 10px; border-radius: 5px; display: inline-block;'><p style='color: {color_texto_formulario}; font-size: 18px; margin: 0;'>¿Te interesa una vacante? Completa el formulario y nos pondremos en contacto contigo.</p></div>",
        unsafe_allow_html=True
    )
    
    # Espacio entre elementos
    st.markdown("<br>", unsafe_allow_html=True)

    # Número de celular
    st.markdown(
        f"<div style='background-color: {color_fondo_formulario}; padding: 5px; border-radius: 5px; display: inline-block;'><p style='color: {color_texto_formulario}; font-size: 16px; margin: 0;'>Número de Celular</p></div>",
        unsafe_allow_html=True
    )
    telefono = st.text_input("", placeholder="Ingrese su número de celular")
    
    # Espacio entre elementos
    st.markdown("<br>", unsafe_allow_html=True)

    # Correo electrónico
    st.markdown(
        f"<div style='background-color: {color_fondo_formulario}; padding: 5px; border-radius: 5px; display: inline-block;'><p style='color: {color_texto_formulario}; font-size: 16px; margin: 0;'>Correo Electrónico</p></div>",
        unsafe_allow_html=True
    )
    correo = st.text_input("", placeholder="Ingrese su correo electrónico")

    # Botón de envío
    submit_button = st.form_submit_button("Enviar")

    if submit_button:
        # Validar que ambos campos no estén vacíos
        if telefono and correo:
            if guardar_contacto(telefono, correo):
                # Mostrar el mensaje de éxito con formato personalizado
                st.markdown(
                    f"<div style='background-color: {color_fondo_exito}; padding: 10px; border-radius: 5px;'><p style='color: #FFFFFF; font-size: 16px;'>¡Gracias por tu interés! Nos pondremos en contacto contigo pronto.</p></div>",
                    unsafe_allow_html=True
                )
        else:
            # Mostrar el mensaje de advertencia con formato personalizado
            st.markdown(
                f"<div style='background-color: {color_fondo_advertencia}; padding: 10px; border-radius: 5px;'><p style='color: #FFFFFF; font-size: 16px;'>Por favor, completa ambos campos para que podamos contactarte.</p></div>",
                unsafe_allow_html=True
            )
    
# Estilo CSS avanzado y ocultación de elementos no deseados
st.markdown(
    f"""
    <style>
    /* Fondo de la aplicación */
    .stApp {{
        background-color: #E2E8F0;
    }}

    /* Estilos personalizados para los selectboxes */
    .stSelectbox {{
        background-color: {color_primario};
        color: white;
    }}

    /* Estilo para el botón de buscar vacantes */
    .stButton[data-baseweb="button"] {{
        background-color: {color_terciario};  /* Cambia el color aquí según lo desees */
        color: white;  /* Color del texto */
        border-radius: 5px;  /* Bordes redondeados */
        padding: 10px 20px;  /* Espaciado interno */
        font-size: 16px;  /* Tamaño de fuente */
    }}

    /* Cambiar el color del botón al pasar el mouse */
    .stButton[data-baseweb="button"]:hover {{
        background-color: {color_primario};  /* Color al pasar el mouse */
    }}

    /* Estilos para el dataframe */
    .stDataFrame {{
        font-size: 16px;
    }}
    
    /* Estilo de texto del título */
    h1, h2, h3 {{
        font-family: "Helvetica Neue", sans-serif;
    }}

    /* Otros estilos personalizados */
    </style>
    """,
    unsafe_allow_html=True
)