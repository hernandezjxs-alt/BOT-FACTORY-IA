"""Panel visual moderno de BOT FACTORY AI.
MVP: los registros siguen siendo temporales en la sesión Streamlit.
Los selectores de rol/tema son demostrativos; no sustituyen autenticación ni permisos reales.
"""
from datetime import datetime, timezone
import os
import streamlit as st
from dotenv import load_dotenv

from bot_factory.agents import create_agent_spec
from bot_factory.agents.models import AgentSpec
from bot_factory.agents.providers.gemini import GeminiProvider

load_dotenv()
st.set_page_config(page_title="BOT FACTORY AI", page_icon="🤖", layout="wide", initial_sidebar_state="auto")

for key, default in (("bot_registry", []), ("agent_registry", [])):
    if key not in st.session_state:
        st.session_state[key] = default
if "theme_choice" not in st.session_state:
    st.session_state.theme_choice = "Oscuro"
if "role_preview" not in st.session_state:
    st.session_state.role_preview = "Administrador"

dark = st.session_state.theme_choice == "Oscuro"
bg = "#0b1020" if dark else "#f4f7fb"
panel = "#141d31" if dark else "#ffffff"
panel2 = "#1b2942" if dark else "#edf2f9"
fg = "#edf3ff" if dark else "#172033"
muted = "#9aa9c2" if dark else "#667085"
border = "#293750" if dark else "#e3e9f2"
accent = "#8b7cff"
st.markdown(f"""
<style>
:root {{ color-scheme: {'dark' if dark else 'light'}; }}
.stApp {{ background: {bg}; color: {fg}; }}
[data-testid="stHeader"] {{ background: transparent; }}
[data-testid="stSidebar"] {{ background: {panel}; border-right: 1px solid {border}; }}
.block-container {{ padding-top: 2rem; padding-bottom: 3rem; max-width: 1500px; }}
h1,h2,h3,h4,p,span,label {{ color: {fg}; }}
small,.muted {{ color: {muted}; }}
.brandbar {{ display:flex; align-items:center; gap:.85rem; padding:.35rem .15rem 1.15rem; }}
.brandmark {{ width:48px; height:48px; display:flex; align-items:center; justify-content:center; border-radius:15px; color:#fff; font-size:1.75rem; font-weight:900; background:linear-gradient(135deg,#6258e8,#24c6d7); box-shadow:0 8px 24px rgba(99,91,219,.28); }}
.brandname {{ font-size:1.15rem; font-weight:900; letter-spacing:.045em; line-height:1.15; }}
.brandtag {{ color:{muted}; font-size:.66rem; letter-spacing:.15em; font-weight:750; margin-top:.2rem; }}
.brand-spacer {{ flex:1; }}
.brand-pill {{ border:1px solid {border}; color:{muted}; border-radius:999px; padding:.42rem .72rem; font-size:.68rem; font-weight:750; letter-spacing:.08em; }}
.login-shell {{ max-width:620px; margin:1.2rem auto; }}
.login-title {{ text-align:center; font-size:1.8rem; font-weight:850; margin-bottom:.2rem; }}
.login-subtitle {{ text-align:center; color:{muted}; margin-bottom:1.2rem; }}
.landing {{ position:relative; overflow:hidden; min-height:470px; padding:clamp(1.5rem,4vw,3.5rem); border:1px solid rgba(139,124,255,.28); border-radius:30px; background:radial-gradient(circle at 78% 48%, rgba(88,74,210,.26), transparent 32%), radial-gradient(circle at 10% 100%, rgba(20,190,190,.13), transparent 36%), linear-gradient(125deg, #0b1022 0%, #121b37 55%, #101d32 100%); box-shadow:0 24px 70px rgba(18,25,55,.22); margin: .3rem 0 1.3rem; }}
.landing:before {{ content:""; position:absolute; inset:0; opacity:.2; background-image:linear-gradient(rgba(160,174,220,.12) 1px,transparent 1px),linear-gradient(90deg,rgba(160,174,220,.12) 1px,transparent 1px); background-size:34px 34px; mask-image:linear-gradient(90deg,black,transparent 95%); pointer-events:none; }}
.landing-grid {{ position:relative; z-index:2; display:grid; grid-template-columns:1.05fr .95fr; align-items:center; gap:1rem; min-height:390px; }}
.landing-copy {{ max-width:620px; }}
.landing-eyebrow {{ display:inline-flex; align-items:center; gap:.55rem; border:1px solid rgba(130,117,255,.38); border-radius:999px; padding:.48rem .8rem; color:#c5c0ff; font-size:.7rem; font-weight:800; letter-spacing:.13em; background:rgba(99,91,219,.12); }}
.live-dot {{ width:7px; height:7px; border-radius:50%; background:#4ce0b1; box-shadow:0 0 12px #4ce0b1; }}
.landing-title {{ color:#f7f8ff; font-size:clamp(2.5rem,5vw,4.6rem); font-weight:900; line-height:.99; letter-spacing:-.055em; margin:1.25rem 0 1rem; }}
.landing-title span {{ background:linear-gradient(90deg,#a69bff,#52d6e8 75%); -webkit-background-clip:text; background-clip:text; color:transparent; }}
.landing-desc {{ color:#b5c1db; font-size:1.02rem; line-height:1.7; max-width:520px; }}
.landing-chips {{ display:flex; flex-wrap:wrap; gap:.55rem; margin-top:1.5rem; }}
.landing-chip {{ color:#dce5ff; border:1px solid rgba(172,187,226,.2); background:rgba(255,255,255,.055); border-radius:12px; padding:.55rem .75rem; font-size:.78rem; }}
.ai-stage {{ min-height:340px; position:relative; display:flex; align-items:center; justify-content:center; }}
.ai-core {{ position:relative; width:190px; height:190px; display:flex; align-items:center; justify-content:center; border-radius:50%; background:radial-gradient(circle at 35% 30%,#a99dff 0%,#6658e8 28%,#282a71 65%,#141c3d 100%); box-shadow:0 0 45px rgba(120,105,255,.45), inset -12px -14px 30px rgba(4,10,35,.5), inset 8px 8px 22px rgba(255,255,255,.24); animation:coreFloat 5s ease-in-out infinite; z-index:2; }}
.ai-core:before {{ content:""; position:absolute; inset:-17px; border:1px solid rgba(154,146,255,.55); border-radius:50%; box-shadow:0 0 25px rgba(116,103,255,.2); }}
.ai-core:after {{ content:""; position:absolute; inset:-43px; border:1px dashed rgba(89,210,226,.48); border-radius:50%; animation:orbitSpin 24s linear infinite; }}
.core-symbol {{ color:white; font-size:4.2rem; text-shadow:0 5px 22px rgba(255,255,255,.35); }}
.orbit {{ position:absolute; width:300px; height:300px; border:1px solid rgba(112,203,225,.24); border-radius:50%; transform:rotate(-24deg) scaleY(.43); }}
.orbit.two {{ width:390px; height:390px; border-color:rgba(151,130,255,.28); transform:rotate(52deg) scaleY(.42); }}
.orbit-node {{ position:absolute; z-index:3; display:flex; align-items:center; gap:.5rem; padding:.65rem .85rem; border:1px solid rgba(180,194,230,.22); border-radius:15px; color:#edf2ff; background:rgba(18,29,57,.82); backdrop-filter:blur(12px); box-shadow:0 10px 30px rgba(0,0,0,.24); font-size:.8rem; font-weight:750; animation:nodeFloat 5s ease-in-out infinite; }}
.orbit-node b {{ font-size:1.15rem; }}
.node-telegram {{ top:12%; right:4%; }} .node-email {{ bottom:13%; right:0%; animation-delay:-1.8s; }} .node-whatsapp {{ bottom:4%; left:1%; animation-delay:-3.2s; }}
@keyframes coreFloat {{ 0%,100% {{ transform:translateY(0) scale(1); }} 50% {{ transform:translateY(-10px) scale(1.025); }} }}
@keyframes nodeFloat {{ 0%,100% {{ translate:0 0; }} 50% {{ translate:0 -9px; }} }}
@keyframes orbitSpin {{ to {{ transform:rotate(336deg); }} }}
.landing-foot {{ position:relative; z-index:2; display:flex; flex-wrap:wrap; gap:1.3rem; border-top:1px solid rgba(180,194,230,.16); padding-top:1rem; margin-top:1.2rem; color:#aab8d6; font-size:.76rem; }}
.landing-foot strong {{ color:#e9edff; }}
@media(max-width:760px) {{ .landing {{ min-height:unset; padding:1.4rem; }} .landing-grid {{ grid-template-columns:1fr; gap:0; }} .landing-copy {{ text-align:center; margin:auto; }} .landing-eyebrow {{ margin:auto; }} .landing-title {{ font-size:2.65rem; }} .landing-desc {{ font-size:.92rem; margin:auto; }} .landing-chips {{ justify-content:center; }} .ai-stage {{ min-height:290px; transform:scale(.82); margin:-.1rem 0; }} .landing-foot {{ justify-content:center; text-align:center; }} .brand-pill {{ display:none; }} }}
.metric-card {{ position:relative; overflow:hidden; background:linear-gradient(135deg,var(--card-a),var(--card-b)); border:1px solid var(--card-border); border-radius:20px; padding:1.05rem 1.15rem; min-height:132px; box-shadow:0 8px 24px rgba(15,23,42,.12); transition:transform .22s ease,box-shadow .22s ease,filter .22s ease; }}
.metric-card:before {{ content:""; position:absolute; width:115px; height:115px; border-radius:50%; right:-28px; top:-42px; background:rgba(255,255,255,.13); }}
.metric-card:hover {{ transform:translateY(-5px); box-shadow:0 15px 32px rgba(15,23,42,.22); filter:saturate(1.14); }}
.metric-label {{ color:var(--card-text); font-size:.85rem; font-weight:650; position:relative; }}
.metric-value {{ color:var(--card-text); font-size:2.15rem; font-weight:850; margin-top:.3rem; position:relative; }}
.metric-icon {{ font-size:1.5rem; position:relative; }}
.section-card {{ background: {panel}; border:1px solid {border}; border-radius:18px; padding:1.1rem 1.2rem; margin-bottom:.8rem; }}
[data-testid="stVerticalBlockBorderWrapper"] {{ border-radius:18px; transition:border-color .2s ease,transform .2s ease,box-shadow .2s ease; }}
[data-testid="stVerticalBlockBorderWrapper"]:hover {{ border-color:{accent}; box-shadow:0 8px 22px rgba(99,102,241,.10); }}
div.stButton > button, div.stFormSubmitButton > button {{ border-radius: 12px; min-height: 2.7rem; font-weight: 700; }}
div[data-testid="stTabs"] button {{ border-radius: 10px; }}
[data-testid="stMetric"] {{ background: {panel}; border: 1px solid {border}; padding: 1rem; border-radius: 16px; }}
hr {{ border-color: {border}; }}

/* Responsive global: teléfono, tablet y escritorio */
@media (max-width: 760px) {
  .block-container { padding: 1rem .85rem 2rem !important; }
  .brandbar { gap: .65rem; padding-bottom: .9rem; }
  .brandmark { width: 42px; height: 42px; border-radius: 13px; }
  .brandname { font-size: 1rem; }
  .brandtag { font-size: .58rem; letter-spacing: .1em; }
  .landing { border-radius: 22px; }
  .landing-title { overflow-wrap: anywhere; }
  .ai-stage { max-width: 100%; overflow: hidden; }
  .metric-card { min-height: 116px; }
  [data-testid="stHorizontalBlock"] { flex-wrap: wrap !important; gap: .75rem !important; }
  [data-testid="stHorizontalBlock"] > [data-testid="column"] { flex: 1 1 100% !important; min-width: 100% !important; width: 100% !important; }
  [data-testid="stDataFrame"], [data-testid="stTable"] { max-width: 100%; overflow-x: auto; }
  [data-testid="stForm"] { padding: .15rem; }
  div.stButton > button, div.stFormSubmitButton > button { width: 100%; }
  input, textarea, [data-baseweb="select"] { max-width: 100%; }
}
@media (max-width: 520px) {
  .block-container { padding-left: .65rem !important; padding-right: .65rem !important; }
  .brandbar { flex-wrap: wrap; }
  .brandmark { width: 38px; height: 38px; font-size: 1.4rem; }
  .brandname { font-size: .92rem; }
  .brandtag { font-size: .52rem; }
  .landing { padding: 1.05rem !important; border-radius: 18px; }
  .landing-title { font-size: clamp(2rem, 10vw, 2.55rem) !important; line-height: 1.03; }
  .landing-desc { font-size: .88rem; line-height: 1.55; }
  .landing-chip { font-size: .7rem; padding: .48rem .58rem; }
  .ai-stage { min-height: 245px; transform: scale(.72); transform-origin: center center; margin: -1rem 0; width: 100%; }
  .orbit-node { font-size: .72rem; padding: .5rem .62rem; }
  .ai-core { width: 165px; height: 165px; }
  .landing-foot { gap: .65rem; font-size: .68rem; }
  h1 { font-size: 1.75rem !important; }
  h2 { font-size: 1.4rem !important; }
  h3 { font-size: 1.18rem !important; }
  [data-testid="stMetric"] { padding: .75rem; }
}
@media (prefers-reduced-motion: reduce) {
  .ai-core, .ai-core:after, .orbit-node { animation: none !important; }
  .metric-card, [data-testid="stVerticalBlockBorderWrapper"] { transition: none !important; }
}

</style>
""", unsafe_allow_html=True)

def metric_card(label, value, icon, note, palette):
    palettes = {
        "violet": ("#635bdb", "#9b6dff", "#ffffff", "rgba(255,255,255,.35)"),
        "cyan": ("#087eaa", "#20c6d7", "#ffffff", "rgba(255,255,255,.35)"),
        "green": ("#087f67", "#20b486", "#ffffff", "rgba(255,255,255,.35)"),
        "orange": ("#c45b22", "#f59e0b", "#ffffff", "rgba(255,255,255,.35)"),
    }
    a, b, text_color, outline = palettes[palette]
    st.markdown(
        f'<div class="metric-card" style="--card-a:{a};--card-b:{b};--card-text:{text_color};--card-border:{outline}">'
        f'<div class="metric-icon">{icon}</div><div class="metric-label">{label}</div>'
        f'<div class="metric-value">{value}</div><div class="metric-label">{note}</div></div>',
        unsafe_allow_html=True,
    )

def section_heading(title, subtitle=None):
    st.subheader(title)
    if subtitle:
        st.caption(subtitle)

with st.sidebar:
    st.markdown("## 🤖 BOT FACTORY")
    st.caption("AI · AUTOMATION PLATFORM")
    st.divider()
    page = st.radio("NAVEGACIÓN", ["⌂  Inicio", "🔐  Acceso de usuario", "🤖  Bots", "🧠  Agentes IA", "📡  Canales", "🧩  Plantillas", "💼  Planes y servicios", "🛡️  Administración", "⚙️  Configuración"], label_visibility="visible")
    st.divider()
    st.markdown("**Apariencia**")
    st.radio("Tema", ["Oscuro", "Claro"], key="theme_choice", horizontal=True, label_visibility="collapsed")
    st.markdown("**Vista de perfil (demo)**")
    st.selectbox("Rol de vista", ["Administrador", "Usuario"], key="role_preview", label_visibility="collapsed")
    st.caption("El perfil es solo visual. El control real de acceso se implementará con Supabase Auth y RLS.")
    st.divider()
    st.markdown("🟢 Telegram · MVP de conector")
    st.markdown("🟡 Correo · En desarrollo")
    st.markdown("🟡 WhatsApp · En desarrollo")
    st.caption("BOT FACTORY AI · MVP")

total_bots = len(st.session_state.bot_registry)
total_agents = len(st.session_state.agent_registry)
telegram_count = sum(1 for bot in st.session_state.bot_registry if bot.get("channel") == "Telegram")
email_count = sum(1 for bot in st.session_state.bot_registry if bot.get("channel") == "Correo")
whatsapp_count = sum(1 for bot in st.session_state.bot_registry if bot.get("channel") == "WhatsApp")

st.markdown('<div class="brandbar"><div class="brandmark">✦</div><div><div class="brandname">BOT FACTORY AI</div><div class="brandtag">INTELLIGENT AUTOMATION PLATFORM</div></div><div class="brand-spacer"></div><div class="brand-pill">AI WORKSPACE</div></div>', unsafe_allow_html=True)

if page.startswith("🔐"):
    st.markdown('<div class="login-shell">', unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown('<div class="login-title">Bienvenido a tu espacio</div><div class="login-subtitle">Accede a tus bots, agentes y automatizaciones.</div>', unsafe_allow_html=True)
        login_tab, signup_tab = st.tabs(["Iniciar sesión", "Crear cuenta"])
        with login_tab:
            with st.form("user_login_form"):
                login_email = st.text_input("Correo electrónico", placeholder="usuario@empresa.com")
                login_password = st.text_input("Contraseña", type="password", placeholder="Ingresa tu contraseña")
                login_submit = st.form_submit_button("Entrar a BOT FACTORY AI", type="primary", use_container_width=True)
            if login_submit:
                st.info("La pantalla de acceso está diseñada. La validación de credenciales y las sesiones seguras se activarán al conectar Supabase Auth.")
            st.caption("¿Olvidaste tu contraseña? La recuperación se habilitará con Supabase Auth.")
        with signup_tab:
            with st.form("user_signup_form"):
                signup_name = st.text_input("Nombre")
                signup_email = st.text_input("Correo electrónico", placeholder="usuario@empresa.com")
                signup_password = st.text_input("Crear contraseña", type="password")
                signup_confirm = st.text_input("Confirmar contraseña", type="password")
                signup_submit = st.form_submit_button("Crear mi cuenta", type="primary", use_container_width=True)
            if signup_submit:
                if not signup_name.strip() or not signup_email.strip() or not signup_password:
                    st.error("Completa todos los campos.")
                elif signup_password != signup_confirm:
                    st.error("Las contraseñas no coinciden.")
                else:
                    st.info("El formulario está preparado visualmente. El registro real y el almacenamiento seguro se habilitarán con Supabase Auth.")
    st.markdown('</div>', unsafe_allow_html=True)
    st.caption("BOT FACTORY AI · Acceso de usuario · Vista de demostración; todavía no autentica ni crea cuentas.")

elif page.startswith("⌂"):
    st.markdown('<section class="landing"><div class="landing-grid"><div class="landing-copy"><div class="landing-eyebrow"><i class="live-dot"></i> TU CENTRO DE AUTOMATIZACIÓN IA</div><div class="landing-title">Dale vida a tus ideas.<br><span>Automatiza el futuro.</span></div><div class="landing-desc">Diseña bots y agentes inteligentes que conectan conversaciones, procesos y clientes desde una sola plataforma.</div><div class="landing-chips"><span class="landing-chip">✦ Agentes IA</span><span class="landing-chip">↗ Flujos inteligentes</span><span class="landing-chip">⌘ Multi-canal</span></div></div><div class="ai-stage"><div class="orbit"></div><div class="orbit two"></div><div class="ai-core"><div class="core-symbol">✳</div></div><div class="orbit-node node-telegram"><b>✈️</b> Telegram</div><div class="orbit-node node-email"><b>✉️</b> Email</div><div class="orbit-node node-whatsapp"><b>◉</b> WhatsApp</div></div></div><div class="landing-foot"><span><strong>01</strong> · Diseña</span><span><strong>02</strong> · Conecta</span><span><strong>03</strong> · Automatiza</span><span>Una fábrica. Infinitas posibilidades.</span></div></section>', unsafe_allow_html=True)
    st.markdown("### Tu centro de operaciones")
    st.caption("Visión general de tu fábrica digital. Los indicadores reflejan los registros de esta sesión.")
    cols = st.columns(4)
    with cols[0]: metric_card("Bots registrados", total_bots, "🤖", "En tu espacio de trabajo", "violet")
    with cols[1]: metric_card("Agentes IA", total_agents, "🧠", "Definiciones creadas", "cyan")
    with cols[2]: metric_card("Telegram", telegram_count, "✈️", "Bots asociados", "green")
    with cols[3]: metric_card("Canales", 3, "🔗", "Telegram · Correo · WhatsApp", "orange")
    st.write("")
    left, right = st.columns([1.2, 1])
    with left:
        with st.container(border=True):
            section_heading("Actividad de tu espacio", "Resumen de los elementos creados")
            if not st.session_state.bot_registry and not st.session_state.agent_registry:
                st.info("Tu espacio está listo. Crea tu primer bot o agente para comenzar.")
            for bot in st.session_state.bot_registry[-5:]:
                st.markdown(f"**🤖 {bot['name']}** · {bot['channel']}  ")
                st.caption(f"{bot['status']} · {bot['client'] or 'Espacio interno'}")
            for agent in st.session_state.agent_registry[-5:]:
                st.markdown(f"**🧠 {agent['name']}** · {agent['provider']}")
                st.caption(f"{agent['status']} · {agent['channel']}")
    with right:
        with st.container(border=True):
            section_heading("Conectores", "Estado real del desarrollo")
            st.markdown("🟢 **Telegram**")
            st.caption("Worker MVP creado; falta validar con token real.")
            st.markdown("🟡 **Correo electrónico**")
            st.caption("Conector pendiente de implementación.")
            st.markdown("🟡 **WhatsApp**")
            st.caption("Integración oficial pendiente.")
        with st.container(border=True):
            section_heading("Motor de inteligencia artificial")
            st.markdown("✨ **Google Gemini**")
            st.caption("Adaptador implementado. Requiere configurar el secreto para probarlo.")

elif page.startswith("🤖"):
    section_heading("Gestión de bots", "Registra y organiza las soluciones que implementaremos para tus clientes.")
    with st.container(border=True):
        with st.form("create_bot_form", clear_on_submit=True):
            c1, c2 = st.columns(2)
            with c1:
                name = st.text_input("Nombre del bot", placeholder="Ej. Asistente de ventas")
                channel = st.selectbox("Canal", ["Telegram", "Correo", "WhatsApp"])
            with c2:
                client = st.text_input("Cliente / empresa", placeholder="Ej. Empresa Demo")
                description = st.text_area("Objetivo y descripción", placeholder="¿Qué tareas realizará?")
            submitted = st.form_submit_button("＋ Registrar bot", type="primary", use_container_width=True)
    if submitted:
        if not name.strip():
            st.error("Ingresa un nombre para el bot.")
        else:
            st.session_state.bot_registry.append({"id": f"BOT-{len(st.session_state.bot_registry)+1:04d}", "name": name.strip(), "channel": channel, "client": client.strip(), "description": description.strip(), "status": "Pendiente de configuración", "created_at": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")})
            st.success("Ficha registrada en esta sesión.")
            st.rerun()
    section_heading("Tus bots", f"{total_bots} registro(s)")
    if not st.session_state.bot_registry:
        st.info("Todavía no tienes bots registrados.")
    for bot in st.session_state.bot_registry:
        with st.container(border=True):
            a,b = st.columns([3,1])
            with a:
                st.markdown(f"**🤖 {bot['name']}**")
                st.caption(f"{bot['id']} · {bot['channel']} · {bot['client'] or 'Interno'}")
                st.write(bot["description"] or "Sin descripción")
            with b:
                st.info(bot["status"])

elif page.startswith("🧠"):
    section_heading("Agent Factory", "Diseña agentes inteligentes con identidad, instrucciones y proveedor configurable.")
    with st.container(border=True):
        with st.form("create_agent_form", clear_on_submit=True):
            agent_name = st.text_input("Nombre del agente", placeholder="Ej. Agente de atención al cliente")
            role = st.text_input("Especialidad / rol", placeholder="Ej. Especialista de soporte nivel 1")
            instructions = st.text_area("Instrucciones principales", placeholder="Objetivos, tono, límites y cuándo derivar a una persona.", height=130)
            a,b = st.columns(2)
            with a:
                provider = st.selectbox("Proveedor IA", ["google", "anthropic", "openai", "manual"])
                model = st.text_input("Modelo (opcional)", placeholder="Nombre exacto del modelo")
            with b:
                agent_channel = st.selectbox("Canal", ["none", "telegram", "email", "whatsapp"])
                tenant = st.text_input("Cliente / espacio", value="local-demo")
            tool_options = st.multiselect("Herramientas previstas (no ejecutables todavía)", ["Base de conocimiento", "Búsqueda web", "Lectura de documentos", "Crear tickets", "Notificaciones", "CRM"])
            create_agent = st.form_submit_button("＋ Crear agente IA", type="primary", use_container_width=True)
    if create_agent:
        try:
            spec = create_agent_spec(name=agent_name, role=role, instructions=instructions, provider=provider, model=model, channel=agent_channel, tools=tuple(tool_options), tenant_id=tenant or "local-demo")
            record = spec.to_dict()
            record.update({"id": f"AGT-{len(st.session_state.agent_registry)+1:04d}", "status": "Definido · proveedor no conectado", "created_at": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")})
            st.session_state.agent_registry.append(record)
            st.success("Agente definido en esta sesión.")
            st.rerun()
        except ValueError as exc:
            st.error(str(exc))
    section_heading("Agentes creados", f"{total_agents} agente(s)")
    for agent in st.session_state.agent_registry:
        with st.container(border=True):
            st.markdown(f"**🧠 {agent['name']}** · {agent['id']}")
            st.caption(f"{agent['role']} · {agent['provider']} · {agent['channel']}")
            st.write(agent["instructions"])
            with st.expander("Configuración"):
                st.json(agent)

    st.divider()
    section_heading("Laboratorio Gemini", "Prueba el modelo con un agente configurado para Google.")
    try:
        gemini_api_key = st.secrets.get("GEMINI_API_KEY", "")
        gemini_model = st.secrets.get("GEMINI_MODEL", os.getenv("GEMINI_MODEL", "gemini-2.5-flash-lite"))
    except Exception:
        gemini_api_key = os.getenv("GEMINI_API_KEY", "")
        gemini_model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash-lite")
    gemini_api_key = gemini_api_key or os.getenv("GEMINI_API_KEY", "")
    if not gemini_api_key:
        st.info("Configura GEMINI_API_KEY en App settings → Secrets para habilitar las pruebas.")
    else:
        google_agents = [a for a in st.session_state.agent_registry if a.get("provider") == "google"]
        if google_agents:
            selected_agent_name = st.selectbox("Agente", [a["name"] for a in google_agents], key="gemini_test_agent")
            selected_agent = next(a for a in google_agents if a["name"] == selected_agent_name)
            test_message = st.text_area("Mensaje de prueba", key="gemini_test_message")
            if st.button("Enviar mensaje a Gemini", type="primary"):
                if test_message.strip():
                    try:
                        agent_spec = AgentSpec(name=selected_agent["name"], role=selected_agent["role"], instructions=selected_agent["instructions"], provider="google", model=selected_agent.get("model") or gemini_model, channel=selected_agent.get("channel", "none"), tools=tuple(selected_agent.get("tools", [])), tenant_id=selected_agent.get("tenant_id", "local-demo"))
                        with st.spinner("Gemini está respondiendo..."):
                            st.markdown(GeminiProvider(api_key=gemini_api_key, model=gemini_model).generate(agent_spec, test_message.strip()))
                    except Exception as exc:
                        st.error(f"No se pudo completar la prueba: {exc}")
        else:
            st.caption("Crea un agente con proveedor google para comenzar.")

elif page.startswith("📡"):
    section_heading("Canales de comunicación", "Conectores para desplegar tus automatizaciones donde están tus usuarios.")
    channel_data = [("✈️","Telegram","MVP creado","Worker independiente y comandos /start, /help y /status. Requiere token privado de BotFather y prueba real."),("✉️","Correo electrónico","En planificación","Diseño de recepción, clasificación, respuestas y notificaciones con APIs/SMTP seguro."),("💬","WhatsApp","En planificación","Integración mediante API oficial o proveedor autorizado, con plantillas y consentimiento.")]
    for icon, title, status, desc in channel_data:
        with st.container(border=True):
            st.markdown(f"### {icon} {title}")
            st.caption(status)
            st.write(desc)

elif page.startswith("🧩"):
    section_heading("Biblioteca de plantillas", "Puntos de partida para acelerar cada implementación.")
    templates = [("🛍️","Agente comercial","Califica consultas, responde preguntas y deriva oportunidades."),("🎧","Agente de soporte","Resuelve preguntas frecuentes y escala casos complejos."),("📁","Agente administrativo","Clasifica documentos y organiza tareas."),("🔔","Telegram · Alertas","Envía notificaciones operativas."),("📨","Correo · Clasificador","Organiza correos por categoría y prioridad."),("💬","WhatsApp · Atención","Atiende consultas mediante integración oficial.")]
    cols = st.columns(2)
    for i,(icon,title,detail) in enumerate(templates):
        with cols[i%2]:
            with st.container(border=True):
                st.markdown(f"### {icon} {title}")
                st.write(detail)
                st.caption("Plantilla conceptual · automatización pendiente de conexión")

elif page.startswith("💼"):
    section_heading("Planes y servicios", "Elige autoservicio SaaS o solicita una implementación personalizada con BOT FACTORY Studio.")
    st.info("Planes piloto de referencia en CLP. Son precios de prueba para validar con clientes; todavía no hay cobro, suscripciones ni límites automatizados.")
    plan_cols = st.columns(4)
    plans = [
        ("Starter", "$14.990", "1 bot · 1 canal", "Para profesionales y microempresas"),
        ("Pro", "$39.990", "Hasta 3 bots · 2 canales", "Para pymes"),
        ("Business", "$99.990", "Hasta 10 bots · varios usuarios", "Para equipos en crecimiento"),
        ("Enterprise", "A cotizar", "Volumen e integraciones", "Para operaciones empresariales"),
    ]
    for col, (plan_name, price, scope, audience) in zip(plan_cols, plans):
        with col:
            with st.container(border=True):
                st.markdown(f"### {plan_name}")
                st.markdown(f"## {price}")
                st.caption("CLP / mes · precio piloto" if price != "A cotizar" else "Propuesta personalizada")
                st.write(scope)
                st.caption(audience)
    st.caption("Los costos externos de IA, WhatsApp, correo y proveedores pueden cobrarse aparte. No se ofrece uso ilimitado. Los precios finales se definirán tras medir costos reales.")
    st.divider()
    section_heading("BOT FACTORY Studio", "Desarrollo a medida para empresas que necesitan algo más que una plantilla.")
    studio_cols = st.columns(2)
    with studio_cols[0]:
        st.markdown("**Servicios disponibles en el catálogo**")
        st.markdown("- Diagnóstico y diseño de procesos")
        st.markdown("- Bots y agentes personalizados")
        st.markdown("- Integración con CRM, ERP y APIs")
        st.markdown("- Capacitación y documentación")
        st.markdown("- Soporte y mantenimiento")
    with studio_cols[1]:
        st.markdown("**Solicitar una evaluación**")
        with st.form("studio_request_form", clear_on_submit=True):
            contact_name = st.text_input("Nombre de contacto")
            company_name = st.text_input("Empresa")
            contact_email = st.text_input("Correo de contacto")
            project_channel = st.multiselect("Canales de interés", ["Telegram", "WhatsApp", "Correo electrónico"])
            project_need = st.text_area("¿Qué proceso quieres automatizar?", height=110)
            request_sent = st.form_submit_button("Registrar solicitud de evaluación", type="primary", use_container_width=True)
        if request_sent:
            if not contact_name.strip() or not contact_email.strip() or not project_need.strip():
                st.error("Completa nombre, correo y descripción del proyecto.")
            else:
                st.session_state.setdefault("studio_requests", [])
                st.session_state.studio_requests.append({
                    "contact": contact_name.strip(),
                    "company": company_name.strip(),
                    "email": contact_email.strip(),
                    "channels": project_channel,
                    "need": project_need.strip(),
                    "status": "Solicitud registrada en esta sesión",
                })
                st.success("Solicitud guardada temporalmente en esta sesión de demostración. Todavía no se envía por correo ni se persiste en una base de datos.")
    if st.session_state.get("studio_requests"):
        with st.expander("Solicitudes de demostración de esta sesión"):
            for request in st.session_state.studio_requests:
                st.write(f"**{request['contact']}** · {request['company'] or 'Sin empresa'} · {request['email']}")
                st.caption(f"Canales: {', '.join(request['channels']) or 'Por definir'} · {request['status']}")
                st.write(request["need"])

elif page.startswith("🛡️"):
    section_heading("Administración", "Centro de control de la plataforma.")
    if st.session_state.role_preview != "Administrador":
        st.warning("Esta vista está en modo Usuario. Cambia el selector de perfil en el menú lateral para ver la vista administrativa de demostración.")
    else:
        st.success("Vista de administrador (demostración visual; todavía no existe autenticación real).")
        a,b,c = st.columns(3)
        with a:
            with st.container(border=True):
                st.markdown("### 👥 Usuarios")
                st.metric("Cuentas registradas", "—")
                st.caption("Pendiente: Supabase Auth y roles.")
        with b:
            with st.container(border=True):
                st.markdown("### 🏢 Clientes")
                st.metric("Organizaciones", "—")
                st.caption("Pendiente: multiempresa y RLS.")
        with c:
            with st.container(border=True):
                st.markdown("### 🧾 Auditoría")
                st.metric("Eventos", "—")
                st.caption("Pendiente: trazabilidad persistente.")
        st.warning("No uses esta vista como control de seguridad: el selector de rol solo cambia la presentación. Los permisos reales se implementarán con Supabase Auth + RLS.")

else:
    section_heading("Configuración", "Preferencias y estado técnico del espacio de trabajo.")
    with st.container(border=True):
        st.markdown("### 🎨 Apariencia")
        st.write(f"Tema seleccionado: **{st.session_state.theme_choice}**")
        st.caption("Puedes cambiarlo en cualquier momento desde el menú lateral.")
    with st.container(border=True):
        st.markdown("### 🔐 Seguridad y credenciales")
        st.write("Las API keys y tokens deben configurarse en Secrets del despliegue, nunca en formularios ni en GitHub.")
        st.caption("Variables actuales: GEMINI_API_KEY, GEMINI_MODEL.")
    with st.container(border=True):
        st.markdown("### ℹ️ Estado del MVP")
        st.write("Los bots y agentes se guardan temporalmente en la sesión. Supabase, autenticación, correo y WhatsApp siguen pendientes.")

st.divider()
st.caption("BOT FACTORY AI · Plataforma modular de bots y agentes inteligentes · Versión visual MVP 0.2")
