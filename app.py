import streamlit as st
import requests
import os
from dotenv import load_dotenv
import re

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

st.set_page_config(page_title="LinkedIn Scraper", page_icon="🔎")

# --- Traducciones ---
T = {
    "es": {
        "title": "LinkedIn Sales Navigator Scraper",
        "subtitle": "Conexión a tu cuenta de LinkedIn",
        "auth_method": "Elegí cómo obtener tu cookie de LinkedIn",
        "auto": "Recuperación automática",
        "manual": "Ingreso manual",
        "cookie": "Pegá tu cookie de sesión de LinkedIn aquí",
        "url": "URL de búsqueda de Sales Navigator",
        "count": "Cantidad de leads",
        "email": "Dirección de email",
        "start": "Iniciar scraping",
        "welcome": "Bienvenido",
        "error_email": "Por favor, ingresa un correo electrónico válido.",
        "error": "Por favor completá todos los campos requeridos.",
        "login_error": "Usuario o contraseña incorrectos.",
        "logout": "Cerrar sesión"
    },
    "en": {
        "title": "LinkedIn Sales Navigator Scraper",
        "subtitle": "LinkedIn Account Connection",
        "auth_method": "Choose LinkedIn Cookie Retrieval Method",
        "auto": "Automatic Retrieval",
        "manual": "Manual Input",
        "cookie": "Paste your LinkedIn session cookie here",
        "url": "Sales Navigator Search URL",
        "count": "Number of Leads",
        "email": "Email Address",
        "start": "Start Scraping",
        "welcome": "Welcome",
        "error_email": "Please enter a valid email address.",
        "error": "Please fill in all required fields.",
        "login_error": "Incorrect username or password.",
        "logout": "Logout"
    }
}

# --- Estado inicial ---
if "lang" not in st.session_state:
    st.session_state.lang = "en"
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False  # Iniciar sesión en False
if "username" not in st.session_state:
    st.session_state.username = ""
if "password" not in st.session_state:
    st.session_state.password = ""

if "scrape_attempted" not in st.session_state:
    st.session_state["scrape_attempted"] = False

lang = st.session_state.lang
text = T[lang]
subtitle = text['subtitle']

# --- Función de validación de correo ---
def is_valid_email(email):
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zAZ0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_regex, email) is not None

# --- Login ---
if not st.session_state.logged_in:
    st.header("Login")

    # Crear campos de entrada para el formulario de login
    username_input = st.text_input("Username", key="username_input")
    password_input = st.text_input("Password", type="password", key="password_input")

    # Cargar las credenciales desde el archivo .env
    user_nico = os.getenv("USER_NICO")
    pass_nico = os.getenv("PASS_NICO")
    user_mati = os.getenv("USER_MATI")
    pass_mati = os.getenv("PASS_MATI")

    # Lógica del login
    if username_input and password_input:  # Si ambos campos tienen texto, ejecuta el login
        # Validación de usuario y contraseña
        if (username_input == user_nico and password_input == pass_nico) or \
           (username_input == user_mati and password_input == pass_mati):
            st.session_state.logged_in = True
            st.session_state.username = username_input
            st.session_state.password = password_input
            st.success("Login successful!")
            st.rerun()  # Recargar la página para mostrar el contenido principal
        else:
            st.error(text["login_error"])

    # Botón de login (para casos donde el usuario haga clic)
    login_button = st.button("Login")
    if login_button:  # Si se hace clic en el botón, ejecutar la misma lógica de login
        if (username_input == user_nico and password_input == pass_nico) or \
           (username_input == user_mati and password_input == pass_mati):
            st.session_state.logged_in = True
            st.session_state.username = username_input
            st.session_state.password = password_input
            st.success("Login successful!")
            st.rerun()  # Recargar la página para mostrar el contenido principal
        else:
            st.error(text["login_error"])
else:
    # --- Mensaje de bienvenida ---
    capitalized_user = st.session_state.username.capitalize()
    st.markdown(f"<div class='welcome'>⚡ {text['welcome']}, <b>{capitalized_user}</b></div>", unsafe_allow_html=True)

    # --- Contenido principal ---
    st.markdown(f"<h1 style='margin-top: 1em'>{text['title']}</h1>", unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    st.markdown(f"<h4 style='margin-bottom: 0.2em; color: white'>{subtitle}</h4>", unsafe_allow_html=True)

    # --- Selector método de autenticación ---
    st.radio(text["auth_method"], options=["auto", "manual"], index=1,
            format_func=lambda x: text["auto"] if x == "auto" else text["manual"],
            key="auth_method")

    # --- Campos del formulario ---
    cookie = ""
    if st.session_state.auth_method == "manual":
        cookie = st.text_input(text["cookie"], type="password", key="cookie")

    search_url = st.text_input(text["url"], key="search_url")
    cols = st.columns(2)
    lead_count = cols[0].number_input(text["count"], min_value=1, max_value=500, value=100, key="lead_count")
    notify_email = cols[1].text_input(text["email"], key="notify_email")

    # Validar email
    if notify_email and not is_valid_email(notify_email):
        st.error(text["error_email"])

    st.markdown("<br>", unsafe_allow_html=True)

    # --- Botón de enviar ---
    center = st.columns([0.3, 0.4, 0.3])
    with center[1]:
        st.markdown(f"""
            <style>
                .custom-start-btn {{
                    background-color: #ef4444;
                    border: 1px solid #f87171;
                    border-radius: 8px;
                    color: white;
                    width: 100%;
                    font-weight: bold;
                    padding: 0.75em 0;
                    transition: background-color 0.3s ease;
                    text-align: center;
                    cursor: pointer;
                    font-size: 1rem;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                }}
                .custom-start-btn:hover {{
                    background-color: #dc2626;
                }}
                .custom-start-btn span {{
                    margin-right: 10px;
                }}
            </style>
        """, unsafe_allow_html=True)

    # Usamos el emoji directamente en lugar del <span>
    if st.button(f"🚀 {text['start']}", key="start_scraping", help=text["start"], 
                 use_container_width=True, on_click=None):
        if search_url and notify_email and is_valid_email(notify_email) and (cookie or st.session_state.auth_method == "auto"):
            payload = {
                "cookie": cookie,
                "search_url": search_url,
                "lead_count": lead_count,
                "notify_email": notify_email
            }
            try:
                res = requests.post(
                    "https://n8n2.bgroup.com.ar/webhook-test/af7e35c5-164d-480a-9c17-4641afea11f2",
                    json=payload
                )
                if res.status_code == 200:
                    st.toast(text["success"], icon="✅")
                    st.session_state["scrape_attempted"] = False
                else:
                    st.toast(f"❌ Error {res.status_code}", icon="❌")
            except Exception as e:
                st.toast(f"❌ {str(e)}", icon="❌")
        else:
            st.session_state["scrape_attempted"] = True

    if st.session_state.get("scrape_attempted"):
        st.toast(text["error"], icon="⚠️")

    # --- Botón de cerrar sesión (aparece a la derecha y un poco más abajo) ---
    logout_button = st.button(f"🚪 {text['logout']}", key="logout_button")
    if logout_button:
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.password = ""
        st.success("Logout successful!")
        st.rerun()  # Recargar la página para reflejar el estado de desconexión

    # Aplicar estilo para cambiar el color del botón y hacerlo igual al de "Start Scraping"
    st.markdown("""
        <style>
            .stButton > button {
                position: fixed;
                right: 20px;
                bottom: 30px;
                font-size: 16px;
                font-weight: bold;
                background-color: transparent; /* Fondo transparente */
                color: #ffffff; /* Texto blanco */
                border: 2px solid #ef4444; /* Borde rojo */
                border-radius: 8px;
                padding: 0.75em 2em;
                transition: background-color 0.3s ease;
            }
            .stButton > button:hover {
                background-color: #f0f0f0; /* Fondo gris claro al pasar el ratón */
            }
        </style>
    """, unsafe_allow_html=True)
