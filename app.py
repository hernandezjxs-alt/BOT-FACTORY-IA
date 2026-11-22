"""Panel Streamlit de BOT FACTORY AI: bots + definiciones de agentes IA.

Los registros de esta versión viven en session_state. No se guardan tokens,
API keys ni datos persistentes. Las llamadas a modelos aún no están habilitadas.
"""
from datetime import datetime, timezone
import os

import streamlit as st
from dotenv import load_dotenv

from bot_factory.agents import create_agent_spec
from bot_factory.agents.models import AgentSpec
from bot_factory.agents.providers.gemini import GeminiProvider

load_dotenv()
st.set_page_config(page_title="BOT FACTORY AI", page_icon="🤖", layout="wide")

for key, default in (("bot_registry", []), ("agent_registry", [])):
    if key not in st.session_state:
        st.session_state[key] = default

st.title("🤖 BOT FACTORY AI")
st.caption("Fábrica modular de bots, agentes inteligentes y automatizaciones empresariales.")

with st.sidebar:
    st.header("Centro de control")
    st.success("Panel MVP disponible")
    st.caption("Los registros son temporales durante esta sesión.")
    st.divider()
    st.markdown("**Canales**")
    st.write("🟢 Telegram · Worker MVP")
    st.write("🟡 Correo · Próxima integración")
    st.write("🟡 WhatsApp · Próxima integración")
    st.divider()
    st.markdown("**Motor IA**")
    st.write("🧠 Definición de agentes disponible")
    st.write("🟢 Gemini configurable (requiere API key gratuita)")

total_bots = len(st.session_state.bot_registry)
total_agents = len(st.session_state.agent_registry)
telegram_count = sum(1 for bot in st.session_state.bot_registry if bot["channel"] == "Telegram")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Bots registrados", total_bots)
c2.metric("Agentes definidos", total_agents)
c3.metric("Bots Telegram", telegram_count)
c4.metric("Canales objetivo", 3)

tab_dashboard, tab_bots, tab_agents, tab_catalog, tab_roadmap = st.tabs(
    ["📊 Resumen", "🤖 Bots", "🧠 Agent Factory", "🧩 Plantillas", "🗺️ Roadmap"]
)

with tab_dashboard:
    st.subheader("Centro de operaciones")
    left, right = st.columns(2)
    with left:
        st.markdown("### Bots")
        if st.session_state.bot_registry:
            for bot in st.session_state.bot_registry:
                st.write(f"**{bot['name']}** · {bot['channel']} · {bot['status']}")
        else:
            st.info("Todavía no hay bots registrados.")
    with right:
        st.markdown("### Agentes IA")
        if st.session_state.agent_registry:
            for agent in st.session_state.agent_registry:
                st.write(f"**{agent['name']}** · {agent['provider']} · {agent['status']}")
        else:
            st.info("Todavía no hay agentes definidos.")
    st.caption("Los estados son de registro/configuración; no representan procesos activos ni inferencias reales.")

with tab_bots:
    st.subheader("Registro y administración de bots")
    with st.form("create_bot_form", clear_on_submit=True):
        name = st.text_input("Nombre del bot", placeholder="Ej. Asistente de ventas")
        channel = st.selectbox("Canal", ["Telegram", "Correo", "WhatsApp"])
        client = st.text_input("Cliente / empresa", placeholder="Ej. Empresa Demo")
        description = st.text_area("Descripción y objetivo")
        submitted = st.form_submit_button("Registrar bot", type="primary")
    if submitted:
        if not name.strip():
            st.error("Ingresa un nombre para el bot.")
        else:
            st.session_state.bot_registry.append({
                "id": f"BOT-{len(st.session_state.bot_registry) + 1:04d}",
                "name": name.strip(), "channel": channel, "client": client.strip(),
                "description": description.strip(),
                "status": "Pendiente de configuración",
                "created_at": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
            })
            st.success("Ficha de bot registrada en esta sesión.")
            st.rerun()

    st.divider()
    st.subheader("Bots registrados")
    if not st.session_state.bot_registry:
        st.info("El registro está vacío.")
    for bot in st.session_state.bot_registry:
        with st.container(border=True):
            st.markdown(f"**{bot['name']}** · {bot['channel']}")
            st.caption(f"Cliente: {bot['client'] or 'Interno'} · Estado: {bot['status']}")
            st.write(bot["description"] or "Sin descripción")

    st.divider()
    st.subheader("Onboarding Telegram")
    st.markdown(
        "1. Abre [@BotFather](https://t.me/BotFather).\n"
        "2. Ejecuta /newbot y completa nombre y username.\n"
        "3. Guarda el token en .env de tu entorno privado.\n"
        "4. Ejecuta python run_telegram_bot.py.\n"
        "5. Envía /start al bot para validar la conexión."
    )
    st.warning("No pegues tokens en este panel ni en GitHub. La gestión segura de credenciales todavía no está implementada.")

with tab_agents:
    st.subheader("Agent Factory Engine")
    st.write("Define la identidad, instrucciones, proveedor previsto y canal de cada agente.")
    st.info(
        "Los agentes se pueden definir y probar con Gemini cuando exista una API key en el entorno. "
        "La persistencia, memoria conversacional y herramientas ejecutables siguen pendientes."
    )
    with st.form("create_agent_form", clear_on_submit=True):
        agent_name = st.text_input("Nombre del agente", placeholder="Ej. Agente de atención al cliente")
        role = st.text_input("Especialidad / rol", placeholder="Ej. Especialista de soporte nivel 1")
        instructions = st.text_area(
            "Instrucciones principales",
            placeholder="Define objetivos, tono, límites, cuándo derivar a una persona y qué no debe hacer.",
            height=160,
        )
        a1, a2 = st.columns(2)
        with a1:
            provider = st.selectbox("Proveedor IA previsto", ["anthropic", "openai", "google", "manual"])
            model = st.text_input("Modelo (opcional)", placeholder="Nombre exacto del modelo")
        with a2:
            agent_channel = st.selectbox("Canal de publicación", ["none", "telegram", "email", "whatsapp"])
            tenant = st.text_input("Cliente / tenant", value="local-demo")
        tool_options = st.multiselect(
            "Herramientas previstas (no ejecutables todavía)",
            ["Consulta de base de conocimiento", "Búsqueda web", "Lectura de documentos",
             "Crear tickets", "Enviar notificaciones", "Consultar CRM"],
        )
        create_agent = st.form_submit_button("Crear definición de agente", type="primary")

    if create_agent:
        try:
            spec = create_agent_spec(
                name=agent_name, role=role, instructions=instructions,
                provider=provider, model=model, channel=agent_channel,
                tools=tuple(tool_options), tenant_id=tenant or "local-demo",
            )
            record = spec.to_dict()
            record["id"] = f"AGT-{len(st.session_state.agent_registry) + 1:04d}"
            record["status"] = "Definido · proveedor no conectado"
            record["created_at"] = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
            st.session_state.agent_registry.append(record)
            st.success("Agente definido correctamente en esta sesión.")
            st.rerun()
        except ValueError as exc:
            st.error(str(exc))

    st.divider()
    st.subheader("Agentes creados")
    if not st.session_state.agent_registry:
        st.info("Aún no hay agentes. Puedes crear el primero con el formulario.")
    for agent in st.session_state.agent_registry:
        with st.container(border=True):
            st.markdown(f"**{agent['name']}** · {agent['id']}")
            st.caption(f"{agent['role']} · Proveedor: {agent['provider']} · Canal: {agent['channel']}")
            st.write(agent["instructions"])
            st.write("Herramientas previstas: " + (", ".join(agent["tools"]) if agent["tools"] else "Ninguna"))
            st.caption(f"Tenant: {agent['tenant_id']} · {agent['status']}")
            with st.expander("Ver configuración"):
                st.json(agent)


    st.divider()
    st.subheader("Prueba de conversación con Gemini")
    gemini_key_ready = bool(os.getenv("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY", ""))
    st.caption("Proveedor inicial sin costo por tokens dentro de las cuotas gratuitas de Google. El uso gratuito tiene límites.")
    st.write("Estado de Gemini: " + ("API key detectada" if gemini_key_ready else "Falta configurar GEMINI_API_KEY"))
    if not gemini_key_ready:
        st.info("Crea una clave gratuita en Google AI Studio y configúrala como GEMINI_API_KEY en el archivo .env local o en los secretos del despliegue. Nunca la pegues aquí ni la subas a GitHub.")
        st.markdown("[Abrir Google AI Studio](https://aistudio.google.com/app/apikey)")
    elif not st.session_state.agent_registry:
        st.info("Primero crea un agente con proveedor google.")
    else:
        google_agents = [a for a in st.session_state.agent_registry if a.get("provider") == "google"]
        if not google_agents:
            st.info("Crea una definición de agente y selecciona google como proveedor.")
        else:
            selected_agent_name = st.selectbox("Agente para probar", options=[a["name"] for a in google_agents], key="gemini_test_agent")
            selected_agent = next(a for a in google_agents if a["name"] == selected_agent_name)
            test_message = st.text_area("Mensaje de prueba", key="gemini_test_message", placeholder="Hola, ¿en qué puedes ayudarme?")
            if st.button("Enviar prueba a Gemini", type="primary", key="run_gemini_test"):
                if not test_message.strip():
                    st.warning("Escribe un mensaje para probar.")
                else:
                    try:
                        agent_spec = AgentSpec(name=selected_agent["name"], role=selected_agent["role"], instructions=selected_agent["instructions"], provider="google", model=selected_agent.get("model") or os.getenv("GEMINI_MODEL", "gemini-2.5-flash-lite"), channel=selected_agent.get("channel", "none"), tools=tuple(selected_agent.get("tools", [])), tenant_id=selected_agent.get("tenant_id", "local-demo"))
                        with st.spinner("Consultando Gemini..."):
                            answer = GeminiProvider().generate(agent_spec, test_message.strip())
                        st.markdown("**Respuesta de Gemini**")
                        st.write(answer)
                    except Exception as exc:
                        st.error(f"No se pudo completar la prueba: {exc}")

    st.warning(
        "Claude Pro no incluye automáticamente acceso a la API de Anthropic. "
        "Para conectar Claude por API se requiere habilitar API/billing y guardar la clave "
        "en un gestor de secretos o variable de entorno, nunca en este formulario."
    )

with tab_catalog:
    st.subheader("Plantillas iniciales")
    templates = [
        ("Agente comercial", "Califica consultas, prepara respuestas y deriva oportunidades."),
        ("Agente de soporte", "Resuelve preguntas frecuentes y escala casos complejos."),
        ("Agente administrativo", "Ayuda a clasificar documentos y organizar tareas."),
        ("Telegram · Notificaciones", "Envía alertas operativas mediante un bot."),
        ("Correo · Clasificador", "Organiza correos por categoría y prioridad."),
        ("WhatsApp · Atención comercial", "Atiende consultas mediante integración oficial."),
    ]
    for title, detail in templates:
        with st.container(border=True):
            st.markdown(f"**{title}**")
            st.write(detail)

with tab_roadmap:
    st.subheader("Ruta de desarrollo")
    st.markdown(
        "- [x] Fundaciones Python y Streamlit\n"
        "- [x] Worker Telegram MVP 0.1 (pendiente de prueba real)\n"
        "- [x] Panel inicial de bots\n"
        "- [x] Modelos y validación de definiciones de agentes IA\n"
        "- [x] Contrato base para adaptadores de proveedores\n"
        "- [ ] Persistencia Supabase multiempresa y autenticación\n"
        "- [x] Adaptador inicial Gemini API y prueba desde Streamlit (pendiente de validar con clave real)\n"
        "- [ ] Conectar Anthropic y OpenAI mediante API\n"
        "- [ ] Memoria conversacional y herramientas ejecutables con permisos\n"
        "- [ ] Supervisor de workers y monitoreo real\n"
        "- [ ] Conectores de correo y WhatsApp\n"
        "- [ ] Pruebas automatizadas y despliegue"
    )
