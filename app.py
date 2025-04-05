import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Cargar variables desde .env o desde secrets en Streamlit Cloud
load_dotenv()

# Usuarios autorizados desde entorno
USERS = {
    os.getenv("USER_NICO"): os.getenv("PASS_NICO"),
    os.getenv("USER_MATI"): os.getenv("PASS_MATI"),
}

st.set_page_config(page_title="AI Lead Gen UI", page_icon="🧠")

# Inicializar estado de sesión si es necesario
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# --- LOGIN ---
if not st.session_state.logged_in:
    st.title("🔐 Iniciá sesión")
    username = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")

    if st.button("Ingresar"):
        if username in USERS and USERS[username] == password:
            st.session_state.username = username
            st.session_state.set_login = True  # bandera para hacer rerun seguro
        else:
            st.error("❌ Usuario o contraseña incorrectos.")

    # Si la bandera de login está activada, hacemos login + rerun
    if st.session_state.get("set_login"):
        st.session_state.logged_in = True
        st.session_state.set_login = False
        st.experimental_rerun()

# --- APP PRINCIPAL ---
if st.session_state.logged_in:
    st.title("🔍 AI-Powered Lead Generator")
    st.caption(f"Sesión activa como: {st.session_state.username}")

    st.subheader("📥 Parámetros de búsqueda de leads")

    session_cookie = st.text_input("🔐 Cookie de sesión de LinkedIn Sales Navigator", type="password")
    search_url = st.text_input("🔗 URL de búsqueda de LinkedIn Sales Navigator")
    lead_count = st.number_input("📊 Cantidad de leads a scrapear", min_value=1, max_value=500, value=50)
    notify_email = st.text_input("📧 Email para recibir los leads")

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
                # ⚠️ Reemplazá esta URL por tu webhook real
                response = requests.post("https://TU_WEBHOOK_N8N.com/webhook/lead-scraper", json=payload)
                if response.status_code == 200:
                    st.success("✅ Scraping iniciado correctamente. Vas a recibir un mail cuando termine.")
                else:
                    st.error(f"❌ Error al llamar al webhook. Código {response.status_code}")
            except Exception as e:
                st.error(f"❌ Falló la conexión: {e}")
        else:
            st.warning("Por favor, completá todos los campos.")
