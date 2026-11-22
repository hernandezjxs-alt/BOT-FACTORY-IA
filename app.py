"""Panel Streamlit de BOT FACTORY AI.

El registro actual es temporal (sesión Streamlit). No guarda tokens ni secretos.
La persistencia multiempresa se incorporará con Supabase y almacenamiento seguro.
"""
from datetime import datetime, timezone

import streamlit as st
from dotenv import load_dotenv

load_dotenv()
st.set_page_config(page_title="BOT FACTORY AI", page_icon="🤖", layout="wide")

if "bot_registry" not in st.session_state:
    st.session_state.bot_registry = []

st.title("🤖 BOT FACTORY AI")
st.caption("Fábrica modular de bots, asistentes y automatizaciones para empresas.")

with st.sidebar:
    st.header("Centro de control")
    st.success("Panel inicial disponible")
    st.caption("Los registros se conservan solo durante esta sesión.")
    st.divider()
    st.markdown("**Canales**")
    st.write("🟢 Telegram · MVP técnico")
    st.write("🟡 Correo · Próxima integración")
    st.write("🟡 WhatsApp · Próxima integración")

total = len(st.session_state.bot_registry)
telegram_count = sum(1 for bot in st.session_state.bot_registry if bot["channel"] == "Telegram")
col1, col2, col3 = st.columns(3)
col1.metric("Bots registrados", total)
col2.metric("Bots Telegram", telegram_count)
col3.metric("Canales objetivo", 3)

tab_dashboard, tab_create, tab_catalog, tab_roadmap = st.tabs(
    ["📊 Resumen", "➕ Crear / registrar bot", "🧩 Plantillas", "🗺️ Roadmap"]
)

with tab_dashboard:
    st.subheader("Panel de administración")
    if not st.session_state.bot_registry:
        st.info("Todavía no hay bots registrados. Ve a «Crear / registrar bot» para comenzar.")
    else:
        for bot in st.session_state.bot_registry:
            with st.container(border=True):
                left, right = st.columns([3, 1])
                left.markdown(f"**{bot['name']}** · {bot['channel']}")
                left.caption(bot["description"] or "Sin descripción")
                left.write(f"Estado: **{bot['status']}**")
                right.caption(f"Cliente: {bot['client'] or 'Interno'}")
                right.caption(f"Alta: {bot['created_at']}")
    st.caption("La vista no representa todavía el estado de procesos desplegados.")

with tab_create:
    st.subheader("Asistente de alta")
    st.write("Registra la ficha del bot y prepara los siguientes pasos de configuración.")
    with st.form("create_bot_form", clear_on_submit=True):
        name = st.text_input("Nombre del bot", placeholder="Ej. Asistente de ventas")
        channel = st.selectbox("Canal", ["Telegram", "Correo", "WhatsApp"])
        client = st.text_input("Cliente / empresa", placeholder="Ej. Empresa Demo")
        description = st.text_area("Descripción y objetivo", placeholder="¿Qué tarea realizará este bot?")
        submitted = st.form_submit_button("Registrar bot", type="primary")
    if submitted:
        if not name.strip():
            st.error("Ingresa un nombre para el bot.")
        else:
            st.session_state.bot_registry.append({
                "id": f"BOT-{len(st.session_state.bot_registry) + 1:04d}",
                "name": name.strip(),
                "channel": channel,
                "client": client.strip(),
                "description": description.strip(),
                "status": "Pendiente de configuración",
                "created_at": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
            })
            st.success("Ficha registrada en esta sesión.")
            st.rerun()

    st.divider()
    st.subheader("Configuración inicial de Telegram")
    st.markdown(
        "1. Abre [@BotFather](https://t.me/BotFather).\n"
        "2. Ejecuta /newbot y completa el nombre y username.\n"
        "3. Guarda el token en el archivo .env de tu entorno privado.\n"
        "4. Ejecuta python run_telegram_bot.py desde la carpeta del proyecto.\n"
        "5. Envía /start al bot para validar la conexión."
    )
    st.warning(
        "No pegues tokens en este panel ni en GitHub. Esta versión no recibe ni persiste "
        "credenciales. La gestión segura de secretos se añadirá con Supabase/secret manager."
    )

with tab_catalog:
    st.subheader("Plantillas iniciales")
    templates = [
        ("Telegram · Atención inicial", "Responde consultas frecuentes y deriva solicitudes."),
        ("Telegram · Notificaciones", "Envía alertas operativas y avisos automatizados."),
        ("Correo · Clasificador", "Organiza correos por categoría y prioridad."),
        ("WhatsApp · Atención comercial", "Atiende consultas mediante integración oficial."),
    ]
    for title, detail in templates:
        with st.container(border=True):
            st.markdown(f"**{title}**")
            st.write(detail)
    st.caption("Son plantillas propuestas; los conectores de correo y WhatsApp aún no están implementados.")

with tab_roadmap:
    st.subheader("Ruta de desarrollo")
    st.markdown(
        "- [x] Fundaciones Python y Streamlit\n"
        "- [x] Worker Telegram MVP 0.1\n"
        "- [x] Panel inicial de registro de bots\n"
        "- [ ] Persistencia multiempresa con Supabase Auth y PostgreSQL/RLS\n"
        "- [ ] Gestión segura de tokens y secretos\n"
        "- [ ] Estados reales, inicio/parada y monitoreo de workers\n"
        "- [ ] Conector de correo\n"
        "- [ ] Conector oficial de WhatsApp\n"
        "- [ ] Plantillas comerciales, planes y onboarding de clientes"
    )
