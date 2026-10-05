import streamlit as st
import pandas as pd
from textblob import TextBlob

# Configuración ampliada de la página
st.set_page_config(page_title="App de Sentimiento Avanzada", layout="wide")

st.title("📊 Análisis de Sentimiento Avanzado")
st.markdown("Esta aplicación evalúa comentarios clasificando su **Sentimiento (5 niveles)** y su **Subjetividad (Opinión vs Hecho)**.")

opcion = st.radio("Selecciona el origen de los comentarios:", ("Datos internos", "Subir archivo CSV"))

comentarios = []

if opcion == "Datos internos":
    st.subheader("Comentarios de prueba (Inglés)")
    comentarios = [
        "I absolutely love this product, it is the most amazing thing ever!", # Extremadamente positivo
        "This product is good and helpful.", # Positivo
        "The package arrived on Tuesday.", # Neutral / Objetivo
        "I don't like this, it is frustrating.", # Negativo
        "This is the worst experience of my life, absolutely terrible and disgusting!", # Extremadamente negativo
    ]
    df_input = pd.DataFrame(comentarios, columns=["Comentario"])
    st.dataframe(df_input, use_container_width=True)

else:
    archivo_subido = st.file_uploader("Sube tu archivo CSV (Debe tener una columna llamada 'Comentario')", type=["csv"])
    if archivo_subido is not None:
        df_input = pd.read_csv(archivo_subido)
        if "Comentario" in df_input.columns:
            comentarios = df_input["Comentario"].tolist()
            st.dataframe(df_input.head(), use_container_width=True)
        else:
            st.error("El archivo CSV debe contener una columna llamada 'Comentario'.")

if st.button("Ejecutar Análisis Profundo") and len(comentarios) > 0:
    resultados = []
    
    for texto in comentarios:
        analisis = TextBlob(texto)
        polaridad = analisis.sentiment.polarity
        subjetividad = analisis.sentiment.subjectivity # Nueva métrica añadida
        
        # 1. LÓGICA DE 5 NIVELES DE SENTIMIENTO
        if polaridad >= 0.6:
            sentimiento = "Extremadamente Positivo"
        elif 0.1 < polaridad < 0.6:
            sentimiento = "Positivo"
        elif -0.1 <= polaridad <= 0.1:
            sentimiento = "Neutral"
        elif -0.6 < polaridad < -0.1:
            sentimiento = "Negativo"
        else:
            sentimiento = "Extremadamente Negativo"
            
        # 2. LÓGICA DE SUBJETIVIDAD (Mayor efectividad/información)
        if subjetividad >= 0.5:
            tipo_texto = "Subjetivo (Opinión)"
        else:
            tipo_texto = "Objetivo (Hecho real)"
            
        resultados.append({
            "Comentario": texto, 
            "Polaridad (Valor)": round(polaridad, 2), 
            "Clasificación": sentimiento,
            "Subjetividad (Valor)": round(subjetividad, 2),
            "Naturaleza": tipo_texto
        })
    
    df_resultados = pd.DataFrame(resultados)
    
    st.divider()
    st.subheader("Resultados del Análisis Detallado")
    
    # Mostramos la tabla mejorada
    st.dataframe(df_resultados, use_container_width=True)
    
    # Generamos columnas para mostrar dos gráficos y darle un aspecto más profesional
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Distribución de Sentimientos (5 Niveles)**")
        conteo_sentimientos = df_resultados["Clasificación"].value_counts()
        st.bar_chart(conteo_sentimientos, color="#4CAF50")
        
    with col2:
        st.write("**Distribución de Naturaleza del Texto**")
        conteo_naturaleza = df_resultados["Naturaleza"].value_counts()
        st.bar_chart(conteo_naturaleza, color="#2196F3")