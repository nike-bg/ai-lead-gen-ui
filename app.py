import streamlit as st
import requests

st.set_page_config(page_title="AI Lead Gen UI", page_icon="🧠")

st.title("🔍 AI-Powered Lead Generator")

# Sección de login (simplificada)
st.subheader("1. Iniciá sesión")
email = st.text_input("Email")
password = st.text_input("Contraseña", type="password")

# Simular login básico
if email and password:
    st.success(f"¡Bienvenido, {email}!")

    st.subheader("2. Parámetros de búsqueda de leads")

    # Inputs del usuario
    session_cookie = st.text_input("🔐 Cookie de sesión de LinkedIn Sales Navigator", type="password")
    search_url = st.text_input("🔗 URL de búsqueda de LinkedIn Sales Navigator")
    lead_count = st.number_input("📊 Cantidad de leads a scrapear", min_value=1, max_value=500, value=50)
    notify_email = st.text_input("📧 Email para recibir los leads")

    # Botón para iniciar scraping
    if st.button("🚀 Iniciar scraping"):
        if session_cookie and search_url and notify_email:
            st.info("Enviando datos al webhook de n8n...")

            payload = {
                "cookie": session_cookie,
                "search_url": search_url,
                "lead_count": lead_count,
                "notify_email": notify_email
            }

            try:
                response = requests.post("https://TU_WEBHOOK_N8N.com/webhook/lead-scraper", json=payload)
                if response.status_code == 200:
                    st.success("✅ Scraping iniciado correctamente. Vas a recibir un mail cuando termine.")
                else:
                    st.error(f"❌ Error al llamar al webhook. Código {response.status_code}")
            except Exception as e:
                st.error(f"❌ Falló la conexión: {e}")
        else:
            st.warning("Por favor, completá todos los campos.")
