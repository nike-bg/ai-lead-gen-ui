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

# Inicializar sesión
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

# --- LOGIN ---
if not st.session_state.logged_in:
    st.title("🔐 Inicia sesión")

    with st.form("login_form", clear_on_submit=False):
        username = st.text_input("Usuario")
        password = st.text_input("Contraseña", type="password")
        submitted = st.form_submit_button("Ingresar")  # Enter también lo activa

    if submitted:
        if username in USERS and USERS[username] == password:
            st.session_state.username = username
            st.session_state.set_login = True
        else:
            st.error("❌ Usuario o contraseña incorrectos.")

    if st.session_state.get("set_login"):
        st.session_state.logged_in = True
        st.session_state.set_login = False
        st.rerun()

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
                # ⚠️ Reemplazá con tu webhook real
                response = requests.post("https://TU_WEBHOOK_N8N.com/webhook/lead-scraper", json=payload)
                if response.status_code == 200:
                    st.success("✅ Scraping iniciado correctamente. Vas a recibir un mail cuando termine.")
                else:
                    st.error(f"❌ Error al llamar al webhook. Código {response.status_code}")
            except Exception as e:
                st.error(f"❌ Falló la conexión: {e}")
        else:
            st.warning("Por favor, completá todos los campos.")

    # --- Botón de logout abajo a la derecha ---
    st.markdown("---")
    logout_col1, logout_col2, logout_col3 = st.columns([6, 1, 1])
    with logout_col3:
        if st.button("Cerrar sesión 🔒"):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.rerun()
