import streamlit as st
import requests
import os
from dotenv import load_dotenv

st.set_page_config(page_title="LinkedIn Scraper", page_icon="🔎")
load_dotenv()

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
        "success": "✅ Scraping iniciado correctamente. Recibirás un mail con los resultados.",
        "error": "❌ Por favor completá todos los campos requeridos."
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
        "success": "✅ Scraping started successfully. You'll receive an email with the results.",
        "error": "❌ Please fill in all required fields."
    }
}

# --- Estado inicial ---
if "lang" not in st.session_state:
    st.session_state.lang = "en"
if "logged_in" not in st.session_state:
    st.session_state.logged_in = True  # For demo purposes
if "username" not in st.session_state:
    st.session_state.username = "nico"


lang = st.session_state.lang
text = T[lang]
subtitle = text['subtitle']

# --- Estilos ---
st.markdown("""
    <style>
    .flag-btn button {
        border: none !important;
        background: transparent !important;
        box-shadow: none !important;
        padding: 0 6px 0 0 !important;
    }
    .welcome {
        text-align: right;
        font-size: 1em;
        color: #facc15;
        margin-top: 1em;
    }
    .custom-start-btn {
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
    }
    .custom-start-btn:hover {
        background-color: #dc2626;
    }
</style>
""", unsafe_allow_html=True)

# --- Selector de idioma ---
col1, col2, col3 = st.columns([0.05, 0.05, 0.9])
with col1:
    with st.container():
        st.markdown('<div class="flag-btn">', unsafe_allow_html=True)
        if st.button("🇪🇸", key="lang_es"):
            st.session_state.lang = "es"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
with col2:
    with st.container():
        st.markdown('<div class="flag-btn">', unsafe_allow_html=True)
        if st.button("🇬🇧", key="lang_en"):
            st.session_state.lang = "en"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

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
            }}
            .custom-start-btn:hover {{
                background-color: #dc2626;
            }}
        </style>
    """, unsafe_allow_html=True)

    if st.button(text["start"]):
        st.session_state["scrape_attempted"] = True
        if search_url and notify_email and (cookie or st.session_state.auth_method == "auto"):
            payload = {
                "cookie": cookie,
                "search_url": search_url,
                "lead_count": lead_count,
                "notify_email": notify_email
            }
            try:
                res = requests.post("https://n8n2.bgroup.com.ar/webhook-test/af7e35c5-164d-480a-9c17-4641afea11f2", json=payload)
                if res.status_code == 200:
                    st.toast(text["success"], icon="✅")
                else:
                    st.toast(f"❌ Error {res.status_code}", icon="❌")
            except Exception as e:
                st.error(f"❌ {str(e)}")
        else:
            if st.session_state.get("scrape_attempted"):
            st.toast(text["error"], icon="⚠️")
    if search_url and notify_email and (cookie or st.session_state.auth_method == "auto"):
        payload = {
            "cookie": cookie,
            "search_url": search_url,
            "lead_count": lead_count,
            "notify_email": notify_email
        }
        try:
            res = requests.post("https://n8n2.bgroup.com.ar/webhook-test/af7e35c5-164d-480a-9c17-4641afea11f2", json=payload)
            if res.status_code == 200:
                st.success(text["success"])
            else:
                st.error(f"❌ Error {res.status_code}")
        except Exception as e:
            st.error(f"❌ {str(e)}")
    else:
        st.warning(text["error"])
