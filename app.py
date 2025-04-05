import streamlit as st
import requests
import os
from dotenv import load_dotenv

st.set_page_config(page_title="AI Lead Gen UI", page_icon="🧠")

# Cargar variables desde .env o desde secrets en Streamlit Cloud
load_dotenv()

# Usuarios autorizados desde entorno
USERS = {
    os.getenv("USER_NICO"): os.getenv("PASS_NICO"),
    os.getenv("USER_MATI"): os.getenv("PASS_MATI"),
}

# Traducciones
T = {
    "es": {
        "welcome": "Bienvenido,",
        "title": "🔍 AI-Powered Lead Generator",
        "subtitle": "📥 Parámetros de búsqueda de leads",
        "cookie": "🔐 Cookie de sesión de LinkedIn Sales Navigator",
        "url": "🔗 URL de búsqueda de LinkedIn Sales Navigator",
        "count": "📊 Cantidad de leads a scrapear",
        "email": "📧 Email para recibir los leads",
        "start": "🚀 Iniciar scraping",
        "logout": "🔒 Cerrar sesión",
        "login_title": "🔐 Inicia sesión",
        "user": "Usuario",
        "pass": "Contraseña",
        "login_btn": "Ingresar",
        "login_error": "❌ Usuario o contraseña incorrectos.",
        "fields_warning": "Por favor, completá todos los campos.",
        "sending": "Enviando datos al webhook de n8n...",
        "success": "✅ Scraping iniciado correctamente. Vas a recibir un mail cuando termine.",
        "fail": "❌ Falló la conexión:"
    },
    "en": {
        "welcome": "Welcome,",
        "title": "🔍 AI-Powered Lead Generator",
        "subtitle": "📥 Lead search parameters",
        "cookie": "🔐 LinkedIn Sales Navigator session cookie",
        "url": "🔗 LinkedIn Sales Navigator search URL",
        "count": "📊 Number of leads to scrape",
        "email": "📧 Email to receive the leads",
        "start": "🚀 Start scraping",
        "logout": "🔒 Log out",
        "login_title": "🔐 Log in",
        "user": "Username",
        "pass": "Password",
        "login_btn": "Log in",
        "login_error": "❌ Invalid username or password.",
        "fields_warning": "Please complete all fields.",
        "sending": "Sending data to n8n webhook...",
        "success": "✅ Scraping started successfully. You’ll get an email once it’s done.",
        "fail": "❌ Connection failed:"
    }
}

# Idioma por defecto
if "lang" not in st.session_state:
    st.session_state.lang = "es"

# Banderas sin bordes con HTML usando <a href> en lugar de onclick
st.markdown("""
    <style>
    .lang-container {
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 1em;
    }
    .lang-flag {
        font-size: 24px;
        text-decoration: none;
        cursor: pointer;
        transition: transform 0.2s ease;
    }
    .lang-flag:hover {
        transform: scale(1.2);
    }
    </style>
    <div class="lang-container">
        <a class="lang-flag" href="?lang=es">🇪🇸</a>
        <a class="lang-flag" href="?lang=en">🇬🇧</a>
    </div>
""", unsafe_allow_html=True)

if "lang" in st.query_params:
    st.session_state.lang = st.query_params["lang"]
    st.query_params.clear()
    st.rerun()

lang = st.session_state.lang

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

if not st.session_state.logged_in:
    st.title(T[lang]["login_title"])

    with st.form("login_form", clear_on_submit=False):
        username = st.text_input(T[lang]["user"])
        password = st.text_input(T[lang]["pass"], type="password")
        submitted = st.form_submit_button(T[lang]["login_btn"])

    if submitted:
        if username in USERS and USERS[username] == password:
            st.session_state.username = username
            st.session_state.set_login = True
        else:
            st.error(T[lang]["login_error"])

    if st.session_state.get("set_login"):
        st.session_state.logged_in = True
        st.session_state.set_login = False
        st.rerun()

if st.session_state.logged_in:
    capitalized_user = st.session_state.username.capitalize()

    st.markdown(f"""
    <style>
    @keyframes fadeIn {{
      from {{ opacity: 0; transform: translateY(-10px); }}
      to {{ opacity: 1; transform: translateY(0); }}
    }}

    @keyframes pulse {{
      0% {{ transform: scale(1); }}
      50% {{ transform: scale(1.15); }}
      100% {{ transform: scale(1); }}
    }}

    .welcome {{
        animation: fadeIn 1s ease-out forwards;
        text-align: right;
        font-size: 1em;
        font-weight: 500;
        margin-bottom: 1em;
        color: #facc15;
    }}

    .welcome .icon {{
        display: inline-block;
        animation: pulse 1.5s infinite;
        margin-right: 4px;
    }}
    </style>

    <div class="welcome">
        <span class="icon">⚡</span>{T[lang]["welcome"]} <b>{capitalized_user}</b>
    </div>
    """, unsafe_allow_html=True)

    st.title(T[lang]["title"])
    st.subheader(T[lang]["subtitle"])
    st.markdown("<br>", unsafe_allow_html=True)

    session_cookie = st.text_input(T[lang]["cookie"], type="password")
    search_url = st.text_input(T[lang]["url"])
    lead_count = st.number_input(T[lang]["count"], min_value=1, max_value=500, value=50)
    notify_email = st.text_input(T[lang]["email"])

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(
        """
        <style>
        div.stButton > button {
            width: 100%;
        }
        </style>
    """, unsafe_allow_html=True)

    if st.button(T[lang]["start"]):
        if session_cookie and search_url and notify_email:
            st.info(T[lang]["sending"])

            payload = {
                "cookie": session_cookie,
                "search_url": search_url,
                "lead_count": lead_count,
                "notify_email": notify_email
            }

            try:
                response = requests.post("https://TU_WEBHOOK_N8N.com/webhook/lead-scraper", json=payload)
                if response.status_code == 200:
                    st.success(T[lang]["success"])
                else:
                    st.error(f"❌ Error: {response.status_code}")
            except Exception as e:
                st.error(f"{T[lang]['fail']} {e}")
        else:
            st.warning(T[lang]["fields_warning"])

    st.markdown("---", unsafe_allow_html=True)
    st.markdown(f"""
        <div style="text-align: right; margin-top: 2em;">
            <form action="?logout=true" method="get">
                <button type="submit" style="
                    background-color: #1f1f1f;
                    color: white;
                    border: 1px solid #444;
                    padding: 8px 20px;
                    font-size: 16px;
                    border-radius: 6px;
                    cursor: pointer;
                ">
                    {T[lang]["logout"]}
                </button>
            </form>
        </div>
    """, unsafe_allow_html=True)

    if st.query_params.get("logout") == "true":
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.rerun()
