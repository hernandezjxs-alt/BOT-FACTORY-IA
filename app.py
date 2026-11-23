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
st.set_page_config(page_title="BOT FACTORY AI", page_icon="🔷", layout="wide", initial_sidebar_state="auto")

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
accent = "#168BFF"
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
.brandmark {{ width:48px; height:48px; display:flex; align-items:center; justify-content:center; border-radius:15px; background:linear-gradient(145deg,#071a3a,#17245a); border:1px solid rgba(75,211,255,.45); box-shadow:0 8px 26px rgba(18,173,255,.22),inset 0 0 18px rgba(83,91,255,.2); }}
.brandmark svg {{ width:39px; height:39px; filter:drop-shadow(0 0 5px rgba(34,211,238,.55)); }}
.brandname {{ font-size:1.15rem; font-weight:900; letter-spacing:.045em; line-height:1.15; }}
.brandtag {{ color:{muted}; font-size:.66rem; letter-spacing:.15em; font-weight:750; margin-top:.2rem; }}
.brand-spacer {{ flex:1; }}
.brand-pill {{ border:1px solid {border}; color:{muted}; border-radius:999px; padding:.42rem .72rem; font-size:.68rem; font-weight:750; letter-spacing:.08em; }}
.login-shell {{ max-width:620px; margin:1.2rem auto; }}
.login-title {{ text-align:center; font-size:1.8rem; font-weight:850; margin-bottom:.2rem; }}
.login-subtitle {{ text-align:center; color:{muted}; margin-bottom:1.2rem; }}
.landing {{ position:relative; overflow:hidden; min-height:470px; padding:clamp(1.5rem,4vw,3.5rem); border:1px solid rgba(22,139,255,.42); border-radius:30px; background:radial-gradient(circle at 78% 48%, rgba(0,132,255,.28), transparent 34%), radial-gradient(circle at 10% 100%, rgba(0,210,255,.12), transparent 36%), linear-gradient(125deg, #07152b 0%, #0b1d3b 55%, #0a1930 100%); box-shadow:0 24px 70px rgba(18,25,55,.22); margin: .3rem 0 1.3rem; }}
.landing:before {{ content:""; position:absolute; inset:0; opacity:.2; background-image:linear-gradient(rgba(160,174,220,.12) 1px,transparent 1px),linear-gradient(90deg,rgba(160,174,220,.12) 1px,transparent 1px); background-size:34px 34px; mask-image:linear-gradient(90deg,black,transparent 95%); pointer-events:none; }}
.landing-grid {{ position:relative; z-index:2; display:grid; grid-template-columns:1.05fr .95fr; align-items:center; gap:1rem; min-height:390px; }}
.landing-copy {{ max-width:620px; }}
.landing-eyebrow {{ display:inline-flex; align-items:center; gap:.55rem; border:1px solid rgba(22,139,255,.42); border-radius:999px; padding:.48rem .8rem; color:#a9d9ff; font-size:.7rem; font-weight:800; letter-spacing:.13em; background:rgba(0,132,255,.13); }}
.live-dot {{ width:7px; height:7px; border-radius:50%; background:#4ce0b1; box-shadow:0 0 12px #4ce0b1; }}
.landing-title {{ color:#f7f8ff; font-size:clamp(2.5rem,5vw,4.6rem); font-weight:900; line-height:.99; letter-spacing:-.055em; margin:1.25rem 0 1rem; }}
.landing-title span {{ background:linear-gradient(90deg,#168BFF,#53E7FF 75%); -webkit-background-clip:text; background-clip:text; color:transparent; }}
.landing-desc {{ color:#b5c1db; font-size:1.02rem; line-height:1.7; max-width:520px; }}
.landing-chips {{ display:flex; flex-wrap:wrap; gap:.55rem; margin-top:1.5rem; }}
.landing-chip {{ color:#dce5ff; border:1px solid rgba(172,187,226,.2); background:rgba(255,255,255,.055); border-radius:12px; padding:.55rem .75rem; font-size:.78rem; }}
.ai-stage {{ min-height:340px; position:relative; display:flex; align-items:center; justify-content:center; }}
.ai-core {{ position:relative; width:230px; height:230px; display:flex; align-items:center; justify-content:center; z-index:2; animation:coreFloat 5s ease-in-out infinite; }}
.ai-core:before {{ content:""; position:absolute; inset:4px; clip-path:polygon(25% 4%,75% 4%,99% 50%,75% 96%,25% 96%,1% 50%); background:linear-gradient(145deg,#62F3FF 0%,#168BFF 58%,#1760E8 100%); filter:drop-shadow(0 0 20px rgba(37,196,255,.8)); }}
.ai-core:after {{ content:""; position:absolute; inset:12px; clip-path:polygon(25% 4%,75% 4%,99% 50%,75% 96%,25% 96%,1% 50%); background:linear-gradient(145deg,#07172f,#101c48 58%,#21134d); }}
.holo-svg {{ position:relative; z-index:3; width:74%; height:74%; overflow:visible; filter:drop-shadow(0 0 9px rgba(34,211,238,.8)); }}
.holo-ring {{ position:absolute; width:310px; height:120px; border:2px solid rgba(48,213,255,.65); border-radius:50%; transform:rotate(-25deg); box-shadow:0 0 18px rgba(48,213,255,.35),inset 0 0 14px rgba(48,213,255,.2); animation:orbitSpin 12s linear infinite; }}
.holo-ring.two {{ width:350px; height:145px; border-color:rgba(52,151,255,.58); transform:rotate(42deg); animation-direction:reverse; }}
.holo-pulse {{ position:absolute; width:180px; height:180px; border-radius:50%; background:radial-gradient(circle,rgba(33,202,255,.2),transparent 68%); filter:blur(9px); animation:pulseGlow 3s ease-in-out infinite; }}
@keyframes pulseGlow {{ 0%,100% {{ transform:scale(.8); opacity:.55; }} 50% {{ transform:scale(1.25); opacity:1; }} }}
.orbit {{ position:absolute; width:300px; height:300px; border:1px solid rgba(112,203,225,.24); border-radius:50%; transform:rotate(-24deg) scaleY(.43); }}
.orbit.two {{ width:390px; height:390px; border-color:rgba(22,139,255,.28); transform:rotate(52deg) scaleY(.42); }}
.orbit-node {{ position:absolute; z-index:3; display:flex; align-items:center; gap:.5rem; padding:.65rem .85rem; border:1px solid rgba(180,194,230,.22); border-radius:15px; color:#edf2ff; background:rgba(18,29,57,.82); backdrop-filter:blur(12px); box-shadow:0 10px 30px rgba(0,0,0,.24); font-size:.8rem; font-weight:750; animation:nodeFloat 5s ease-in-out infinite; }}
.orbit-node b {{ font-size:1.15rem; }}
.orbit-node {{ min-width:124px; justify-content:flex-start; padding:.72rem .9rem; border-color:rgba(22,139,255,.58); background:rgba(8,28,58,.96); }}
.channel-icon {{ width:30px; height:30px; flex:0 0 30px; display:grid; place-items:center; border-radius:9px; background:rgba(255,255,255,.09); }}
.channel-icon svg {{ width:21px; height:21px; display:block; }}
.channel-name {{ color:#f4f7ff; font-size:.78rem; font-weight:800; letter-spacing:.015em; }}
.node-telegram {{ top:8%; right:0%; }} .node-email {{ top:44%; right:-3%; bottom:auto; animation-delay:-1.8s; }} .node-whatsapp {{ bottom:8%; left:0%; animation-delay:-3.2s; }}
@media(max-width:760px) {{ .node-telegram {{ top:4%; right:-2%; }} .node-email {{ top:42%; right:-3%; }} .node-whatsapp {{ bottom:3%; left:-2%; }} .orbit-node {{ min-width:112px; padding:.55rem .68rem; }} }}
.node-telegram {{ top:12%; right:4%; }} .node-email {{ bottom:13%; right:0%; animation-delay:-1.8s; }} .node-whatsapp {{ bottom:4%; left:1%; animation-delay:-3.2s; }}
@keyframes coreFloat {{ 0%,100% {{ transform:translateY(0) scale(1); }} 50% {{ transform:translateY(-10px) scale(1.025); }} }}
@keyframes nodeFloat {{ 0%,100% {{ translate:0 0; }} 50% {{ translate:0 -9px; }} }}
@keyframes orbitSpin {{ to {{ transform:rotate(336deg); }} }}
.landing-foot {{ position:relative; z-index:2; display:flex; flex-wrap:wrap; gap:1.3rem; border-top:1px solid rgba(180,194,230,.16); padding-top:1rem; margin-top:1.2rem; color:#aab8d6; font-size:.76rem; }}
.landing-foot strong {{ color:#e9edff; }}
@media(max-width:760px) {{ .landing {{ min-height:unset; padding:1.4rem; }} .landing-grid {{ grid-template-columns:1fr; gap:0; }} .landing-copy {{ text-align:center; margin:auto; }} .landing-eyebrow {{ margin:auto; }} .landing-title {{ font-size:2.65rem; }} .landing-desc {{ font-size:.92rem; margin:auto; }} .landing-chips {{ justify-content:center; }} .ai-stage {{ min-height:290px; transform:scale(.82); margin:-.1rem 0; }} .landing-foot {{ justify-content:center; text-align:center; }} .brand-pill {{ display:none; }} }}
.metric-card {{ position:relative; overflow:hidden; background:var(--card-a); border:1px solid var(--card-border); border-radius:20px; padding:1.05rem 1.15rem; min-height:132px; box-shadow:0 8px 24px rgba(15,23,42,.12); transition:transform .22s ease,box-shadow .22s ease,filter .22s ease; }}
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
@media (max-width: 760px) {{
  .block-container {{ padding: 1rem .85rem 2rem !important; }}
  .brandbar {{ gap: .65rem; padding-bottom: .9rem; }}
  .brandmark {{ width: 42px; height: 42px; border-radius: 13px; }}
  .brandname {{ font-size: 1rem; }}
  .brandtag {{ font-size: .58rem; letter-spacing: .1em; }}
  .landing {{ border-radius: 22px; }}
  .landing-title {{ overflow-wrap: anywhere; }}
  .ai-stage {{ max-width: 100%; overflow: hidden; }}
  .metric-card {{ min-height: 116px; }}
  [data-testid="stHorizontalBlock"] {{ flex-wrap: wrap !important; gap: .75rem !important; }}
  [data-testid="stHorizontalBlock"] > [data-testid="column"] {{ flex: 1 1 100% !important; min-width: 100% !important; width: 100% !important; }}
  [data-testid="stDataFrame"], [data-testid="stTable"] {{ max-width: 100%; overflow-x: auto; }}
  [data-testid="stForm"] {{ padding: .15rem; }}
  div.stButton > button, div.stFormSubmitButton > button {{ width: 100%; }}
  input, textarea, [data-baseweb="select"] {{ max-width: 100%; }}
}}
@media (max-width: 520px) {{
  .block-container {{ padding-left: .65rem !important; padding-right: .65rem !important; }}
  .brandbar {{ flex-wrap: wrap; }}
  .brandmark {{ width: 38px; height: 38px; font-size: 1.4rem; }}
  .brandname {{ font-size: .92rem; }}
  .brandtag {{ font-size: .52rem; }}
  .landing {{ padding: 1.05rem !important; border-radius: 18px; }}
  .landing-title {{ font-size: clamp(2rem, 10vw, 2.55rem) !important; line-height: 1.03; }}
  .landing-desc {{ font-size: .88rem; line-height: 1.55; }}
  .landing-chip {{ font-size: .7rem; padding: .48rem .58rem; }}
  .ai-stage {{ min-height: 245px; transform: scale(.72); transform-origin: center center; margin: -1rem 0; width: 100%; }}
  .orbit-node {{ font-size: .72rem; padding: .5rem .62rem; }}
  .ai-core {{ width: 165px; height: 165px; }}
  .landing-foot {{ gap: .65rem; font-size: .68rem; }}
  h1 {{ font-size: 1.75rem !important; }}
  h2 {{ font-size: 1.4rem !important; }}
  h3 {{ font-size: 1.18rem !important; }}
  [data-testid="stMetric"] {{ padding: .75rem; }}
}}
@media (prefers-reduced-motion: reduce) {{
  .ai-core, .holo-ring, .holo-pulse, .orbit-node {{ animation: none !important; }}
  .metric-card, [data-testid="stVerticalBlockBorderWrapper"] {{ transition: none !important; }}
}}


/* BOT FACTORY AI — sistema visual fiel a la presentación de marca */
.stApp {{ background:
 radial-gradient(ellipse at 18% 0%, rgba(0,105,255,.13), transparent 38%),
 radial-gradient(ellipse at 90% 30%, rgba(105,35,255,.09), transparent 32%),
 #050b1c; color:#f4f7ff; }}
[data-testid="stSidebar"] {{ background:linear-gradient(180deg,#08152d,#050b1c); border-right:1px solid rgba(30,130,255,.28); }}
.block-container {{ max-width:1480px; padding-top:1.25rem; }}
.brandbar {{ padding: .6rem .2rem 1.3rem; }}
.brandmark {{ width:54px;height:54px;border-radius:17px;background:linear-gradient(145deg,#00d9ff,#075dff 58%,#8c24ff);box-shadow:0 0 26px rgba(0,144,255,.4); }}
.brandname {{ letter-spacing:.055em; }}
.brandtag {{ color:#80eaff !important; }}
[data-testid="stVerticalBlockBorderWrapper"] {{ background:linear-gradient(145deg,rgba(10,28,61,.96),rgba(7,17,40,.98)); border:1px solid rgba(27,126,255,.35); border-radius:20px; box-shadow:0 10px 35px rgba(0,0,0,.2); }}
[data-testid="stVerticalBlockBorderWrapper"]:hover {{ border-color:rgba(43,190,255,.72); box-shadow:0 0 24px rgba(0,119,255,.12); }}
[data-testid="stMetric"] {{ background:#0d2850; border:1px solid rgba(43,157,255,.45); border-radius:17px; }}
div.stButton > button, div.stFormSubmitButton > button {{ background:linear-gradient(100deg,#087dff,#1454e8); color:#fff; border:1px solid #38baff; box-shadow:0 0 18px rgba(0,126,255,.18); }}
div.stButton > button:hover, div.stFormSubmitButton > button:hover {{ border-color:#83f5ff; color:white; box-shadow:0 0 25px rgba(0,180,255,.3); }}
div[data-testid="stTabs"] button[aria-selected="true"] {{ color:#5deaff !important; border-bottom-color:#168bff !important; }}
[data-testid="stRadio"] label, [data-testid="stSelectbox"] label {{ color:#b9d6ff; }}
h1,h2,h3 {{ color:#f5f8ff; }}
.brand-showcase {{ position:relative; overflow:hidden; border:1px solid rgba(24,115,255,.42); border-radius:26px; padding:1.1rem; background:radial-gradient(ellipse at 50% 40%,rgba(0,115,255,.14),transparent 58%),linear-gradient(145deg,#050b1d,#0a1632 58%,#080d24); box-shadow:0 18px 55px rgba(0,0,0,.36),inset 0 0 45px rgba(0,96,255,.07); }}
.brand-showcase:before {{ content:"";position:absolute;inset:0;pointer-events:none;opacity:.18;background-image:linear-gradient(rgba(50,130,255,.2) 1px,transparent 1px),linear-gradient(90deg,rgba(50,130,255,.2) 1px,transparent 1px);background-size:35px 35px;mask-image:linear-gradient(black,transparent 92%); }}
.brand-top {{ position:relative;display:grid;grid-template-columns:1fr 1fr 1fr;gap:1rem;align-items:center;text-align:center;padding:.2rem .5rem 1rem; }}
.brand-top-item {{ display:flex;flex-direction:column;align-items:center;gap:.35rem;min-width:0; }}
.brand-top-item svg {{ width:min(100%,118px);height:110px;filter:drop-shadow(0 0 12px rgba(0,166,255,.55)); }}
.brand-top-item strong {{ font-size:clamp(.72rem,1.4vw,1.05rem);letter-spacing:.035em;color:#f4f8ff; }}
.brand-top-item small {{ color:#91a9d1;font-size:.65rem;letter-spacing:.18em; }}
.brand-top-item .ai-word {{ color:#bd62ff; }}
.brand-tag {{ border:1px solid rgba(28,132,255,.65);border-radius:99px;padding:.35rem .85rem;color:#dbeaff;font-size:.7rem;margin-top:.25rem; }}
.brand-middle {{ position:relative;display:grid;grid-template-columns:1fr 1fr;min-height:390px;border:1px solid rgba(34,124,255,.35);border-radius:24px;overflow:hidden;background:linear-gradient(115deg,rgba(4,15,38,.82),rgba(9,20,48,.82)); }}
.holo-visual {{ position:relative;min-height:390px;display:grid;place-items:center;overflow:hidden;background:radial-gradient(ellipse at 50% 70%,rgba(0,181,255,.3),transparent 52%),linear-gradient(180deg,rgba(0,26,68,.25),rgba(0,7,24,.35)); }}
.holo-beam {{ position:absolute;bottom:19%;width:42%;height:52%;background:linear-gradient(180deg,transparent,rgba(0,212,255,.22),rgba(0,132,255,.03));clip-path:polygon(39% 0,61% 0,100% 100%,0 100%);filter:blur(7px); }}
.holo-logo {{ position:relative;z-index:3;width:min(54%,230px);aspect-ratio:1;display:grid;place-items:center;animation:logoHover 4.5s ease-in-out infinite;filter:drop-shadow(0 0 22px rgba(0,188,255,.7)); }}
.holo-logo svg {{ width:100%;height:100%; }}
.holo-orbit {{ position:absolute;width:84%;height:25%;border:3px solid #078eff;border-radius:50%;transform:rotate(-8deg);box-shadow:0 0 18px #087dff,inset 0 0 15px #087dff;animation:orbitGlow 4s ease-in-out infinite; }}
.holo-orbit.second {{ width:94%;height:35%;border-color:#8d3bff;transform:rotate(10deg);opacity:.8; }}
.holo-platform {{ position:absolute;bottom:8%;width:72%;height:18%;border-radius:50%;border:5px solid #168bff;background:radial-gradient(ellipse,#a9fbff 0%,#078bff 18%,#061b4a 56%,#040b1e 70%);box-shadow:0 0 18px #078bff,0 0 50px rgba(0,166,255,.7),inset 0 0 20px #31dfff; }}
.holo-platform:before,.holo-platform:after {{ content:"";position:absolute;inset:15% 8%;border:2px solid #32dfff;border-radius:50%;box-shadow:0 0 13px #1dbdff; }}
.holo-platform:after {{ inset:-22% -9%;border-color:#813bff;opacity:.7; }}
@keyframes logoHover {{ 0%,100%{{transform:translateY(0)}}50%{{transform:translateY(-13px)}} }}
@keyframes orbitGlow {{ 0%,100%{{filter:brightness(.85)}}50%{{filter:brightness(1.5)}} }}
.brand-message {{ display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;padding:2rem 1.4rem; }}
.brand-message-head {{ display:flex;align-items:center;justify-content:center;gap:.8rem;font-size:clamp(1.3rem,3vw,2.55rem);font-weight:950;letter-spacing:-.04em;white-space:nowrap; }}
.brand-message-head svg {{ width:76px;height:76px;flex:none;filter:drop-shadow(0 0 12px #087dff); }}
.brand-message-head em {{ font-style:normal;background:linear-gradient(90deg,#168bff,#b54cff);color:transparent;background-clip:text; }}
.brand-slogan {{ color:#72eaff;font-size:clamp(.9rem,2vw,1.4rem);font-weight:750;margin:.2rem 0 1rem; }}
.brand-divider {{ height:3px;width:70%;background:linear-gradient(90deg,transparent,#9b36ff,#078bff,#20eaff,transparent);box-shadow:0 0 15px #168bff;margin:.4rem auto 1.5rem; }}
.brand-description {{ color:#e4ecff;font-size:clamp(.9rem,1.4vw,1.12rem);line-height:1.55;max-width:480px;margin-bottom:1.6rem; }}
.channel-links {{ display:flex;justify-content:center;flex-wrap:wrap;gap:.8rem;width:100%; }}
.channel-pill {{ display:flex;align-items:center;justify-content:center;gap:.55rem;border-radius:17px;padding:.75rem .9rem;min-width:135px;color:white;font-weight:800;font-size:.85rem;box-shadow:0 8px 24px rgba(0,0,0,.25); }}
.channel-pill svg {{ width:30px;height:30px; }}
.channel-pill.tg {{ background:linear-gradient(135deg,#087de0,#0752b5); }}
.channel-pill.wa {{ background:linear-gradient(135deg,#08bd62,#087b4c); }}
.channel-pill.mail {{ background:linear-gradient(135deg,#7428d9,#4106a6); }}
.brand-bottom {{ position:relative;display:flex;align-items:center;justify-content:space-around;gap:1rem;flex-wrap:wrap;margin-top:1rem;padding:1rem .6rem .2rem; }}
.brand-bottom-item {{ display:flex;flex-direction:column;align-items:center;gap:.45rem;color:#dce8ff;font-size:.72rem;font-weight:750;min-width:85px; }}
.brand-bottom-item svg {{ width:62px;height:62px;filter:drop-shadow(0 0 12px rgba(0,137,255,.48)); }}
.brand-bottom-item .app-tile {{ width:68px;height:68px;display:grid;place-items:center;border-radius:20px;background:linear-gradient(145deg,#00dfff,#075dff 58%,#8d24ff);box-shadow:0 0 25px rgba(0,130,255,.4); }}
.brand-bottom-item .app-tile svg {{ width:54px;height:54px; }}
.brand-bottom-sep {{ height:75px;width:1px;background:rgba(145,180,255,.45); }}
.metric-card {{ background:#102e58 !important;border:1px solid rgba(45,157,255,.48) !important; }}
@media(max-width:760px) {{
 .brand-showcase{{padding:.55rem;border-radius:18px}}
 .brand-top{{gap:.25rem;padding:.2rem .1rem .65rem}}
 .brand-top-item svg{{height:68px;width:80px}}
 .brand-top-item strong{{font-size:.62rem}}
 .brand-top-item small{{font-size:.48rem;letter-spacing:.08em}}
 .brand-tag{{font-size:.55rem;padding:.25rem .5rem}}
 .brand-middle{{grid-template-columns:1fr;min-height:unset}}
 .holo-visual{{min-height:290px}}
 .brand-message{{padding:1.3rem .7rem 1.5rem}}
 .brand-message-head{{font-size:1.5rem}}
 .brand-message-head svg{{width:55px;height:55px}}
 .brand-description{{font-size:.9rem}}
 .channel-links{{gap:.45rem}}
 .channel-pill{{min-width:0;flex:1;padding:.6rem .45rem;font-size:.72rem;border-radius:12px}}
 .channel-pill svg{{width:24px;height:24px}}
 .brand-bottom{{gap:.65rem}}
 .brand-bottom-item{{min-width:65px;font-size:.62rem}}
 .brand-bottom-item svg{{width:48px;height:48px}}
 .brand-bottom-item .app-tile{{width:54px;height:54px}}
 .brand-bottom-item .app-tile svg{{width:44px;height:44px}}
 .brand-bottom-sep{{height:50px}}
}}


.section-heading {{ display:flex;align-items:center;gap:.8rem;margin:.45rem 0 1.15rem;padding:.2rem 0 .85rem;border-bottom:1px solid rgba(30,137,255,.24); }}
.section-hex {{ font-size:2.3rem;line-height:1;color:#2ceaff;text-shadow:0 0 8px #078bff,0 0 20px #087dff; }}
.section-title {{ color:#f4f8ff;font-size:1.45rem;font-weight:900;letter-spacing:-.025em; }}
.section-subtitle {{ color:#91a9d1;font-size:.82rem;margin-top:.18rem; }}

/* Ajustes de fidelidad visual: tarjetas, holograma y composición */
.brand-top-item:first-child svg {{ width:clamp(110px,14vw,190px);height:clamp(110px,14vw,190px); }}
.brand-top-item:nth-child(2) svg {{ width:clamp(130px,17vw,220px);height:clamp(115px,15vw,190px); }}
.brand-top-item:nth-child(3) svg {{ width:clamp(110px,14vw,190px);height:clamp(110px,14vw,190px); }}
.brand-top {{ align-items:end; padding-bottom:1.15rem; }}
.brand-middle {{ grid-template-columns:1fr 1fr; min-height:510px; }}
.holo-visual {{ min-height:510px; }}
.holo-logo {{ width:min(58%,285px); }}
.holo-platform {{ bottom:8%; width:76%; height:20%; }}
.holo-beam {{ bottom:18%; width:48%; height:59%; }}
.brand-message {{ align-items:stretch; text-align:center; padding:2.2rem clamp(1rem,2.5vw,2.5rem); }}
.brand-message-head {{ justify-content:center; font-size:clamp(1.25rem,2.65vw,2.7rem); }}
.brand-message-head svg {{ width:clamp(58px,7vw,90px);height:clamp(58px,7vw,90px); }}
.brand-description {{ max-width:520px; margin-left:auto;margin-right:auto; }}
.channel-links {{ justify-content:space-between; gap:.55rem; }}
.channel-pill {{ min-width:0; flex:1; padding:.8rem .65rem; font-size:clamp(.72rem,1vw,.95rem); }}
.brand-bottom {{ justify-content:space-between; gap:.5rem; padding:1.25rem .9rem .8rem; }}
.brand-bottom-item {{ flex:1 1 10%; min-width:82px; min-height:138px; padding:.8rem .35rem; border:1px solid rgba(31,123,255,.22); border-radius:20px; background:linear-gradient(155deg,rgba(9,28,63,.96),rgba(5,13,34,.98)); box-shadow:inset 0 0 24px rgba(0,116,255,.08),0 10px 25px rgba(0,0,0,.2); }}
.brand-bottom-item svg {{ width:72px;height:72px; }}
.brand-bottom-item .app-tile {{ width:82px;height:82px; }}
.brand-bottom-item .app-tile svg {{ width:68px;height:68px; }}
.brand-bottom-sep {{ flex:0 0 1px; }}
.metric-card {{ background:linear-gradient(145deg,#10396e,#0a2450) !important; border:1px solid rgba(43,171,255,.58) !important; border-radius:19px; min-height:155px; padding:1.1rem 1.15rem; box-shadow:inset 0 0 25px rgba(0,143,255,.1),0 10px 28px rgba(0,0,0,.25); }}
.metric-card:before {{ background:radial-gradient(circle,rgba(49,220,255,.2),transparent 70%); }}
.metric-icon {{ color:#5ceaff;filter:drop-shadow(0 0 8px #078bff); }}
.metric-value {{ color:#f8fbff; text-shadow:0 0 18px rgba(0,140,255,.25); }}
.section-card,[data-testid="stVerticalBlockBorderWrapper"] {{ background:linear-gradient(145deg,rgba(10,28,61,.96),rgba(7,17,40,.98)) !important; border:1px solid rgba(27,126,255,.35) !important; border-radius:20px !important; box-shadow:0 10px 35px rgba(0,0,0,.2); }}
[data-testid="stVerticalBlockBorderWrapper"]:hover {{ border-color:rgba(43,190,255,.72) !important; box-shadow:0 0 24px rgba(0,119,255,.12) !important; }}
@media(max-width:760px) {{
 .brand-top-item:first-child svg,.brand-top-item:nth-child(3) svg {{ width:76px;height:76px; }}
 .brand-top-item:nth-child(2) svg {{ width:92px;height:84px; }}
 .brand-middle {{ grid-template-columns:1fr;min-height:unset; }}
 .holo-visual {{ min-height:310px; }}
 .holo-logo {{ width:54%; }}
 .brand-message {{ padding:1.25rem .8rem 1.5rem; }}
 .brand-message-head {{ white-space:normal;font-size:1.5rem; }}
 .brand-bottom-item {{ flex:1 1 28%;min-height:112px; }}
 .brand-bottom-item svg {{ width:54px;height:54px; }}
 .brand-bottom-item .app-tile {{ width:60px;height:60px; }}
 .brand-bottom-item .app-tile svg {{ width:50px;height:50px; }}
 .brand-bottom-sep {{ display:none; }}
 .metric-card {{ min-height:128px; }}
}}

/* REPLICA DE PRESENTACIÓN — composición, escala y movimiento */
.brand-showcase {{ padding:1.05rem 1.05rem .8rem; border-radius:28px; background:radial-gradient(ellipse at 50% 34%,rgba(0,83,255,.16),transparent 48%),linear-gradient(145deg,#03091b 0%,#07132c 54%,#050b1d 100%); }}
.brand-showcase:after {{ content:"";position:absolute;inset:0;pointer-events:none;opacity:.22;background:radial-gradient(circle at 18% 20%,#168bff 0 1px,transparent 2px),radial-gradient(circle at 76% 68%,#24eaff 0 1px,transparent 2px),radial-gradient(circle at 48% 86%,#a53cff 0 1px,transparent 2px);background-size:73px 79px,91px 83px,117px 103px;animation:starDrift 18s linear infinite;}}
@keyframes starDrift {{ to {{ background-position:73px 79px,-91px 83px,117px -103px; }} }}
.brand-top {{ grid-template-columns:1fr 1fr 1fr; gap:1.1rem; align-items:end; padding:.25rem .7rem 1rem; }}
.brand-top-item {{ gap:.32rem; }}
.brand-top-item:first-child svg,.brand-top-item:nth-child(3) svg {{ width:clamp(145px,17vw,225px);height:clamp(145px,17vw,225px); }}
.brand-top-item:nth-child(2) svg {{ width:clamp(175px,19vw,250px);height:clamp(155px,17vw,225px); }}
.brand-top-item strong {{ font-size:clamp(1rem,1.9vw,1.55rem);font-weight:950; }}
.brand-top-item small {{ font-size:.72rem;letter-spacing:.22em; }}
.brand-tag {{ font-size:.88rem;padding:.42rem 1.1rem;border-color:#087dff;color:#eaf4ff;box-shadow:0 0 14px rgba(0,119,255,.12); }}
.brand-middle {{ grid-template-columns:1fr 1fr;min-height:500px;border-radius:26px; }}
.holo-visual {{ min-height:500px;background:radial-gradient(ellipse at 50% 76%,rgba(0,199,255,.28),transparent 48%),linear-gradient(180deg,rgba(0,21,57,.25),rgba(0,5,22,.45)); }}
.holo-visual:before {{ content:"";position:absolute;inset:0;background:linear-gradient(90deg,transparent 49.7%,rgba(33,130,255,.13) 50%,transparent 50.3%),repeating-linear-gradient(0deg,transparent 0 27px,rgba(24,129,255,.08) 28px);mask-image:linear-gradient(transparent,#000 18%,#000 85%,transparent); }}
.holo-logo {{ width:min(58%,300px);filter:drop-shadow(0 0 24px rgba(0,188,255,.8)); }}
.holo-logo svg {{ filter:drop-shadow(0 0 10px rgba(24,222,255,.8)); }}
.holo-orbit {{ width:86%;height:28%;border-width:3px;animation:orbitSpin 15s linear infinite,orbitGlow 4s ease-in-out infinite; }}
.holo-orbit.second {{ width:94%;height:36%;animation:orbitSpinReverse 19s linear infinite,orbitGlow 5s ease-in-out infinite; }}
@keyframes orbitSpin {{ from {{ transform:rotate(-8deg); }} to {{ transform:rotate(352deg); }} }}
@keyframes orbitSpinReverse {{ from {{ transform:rotate(10deg); }} to {{ transform:rotate(-350deg); }} }}
.holo-beam {{ width:50%;height:61%;bottom:18%;background:linear-gradient(180deg,transparent,rgba(0,230,255,.24),rgba(0,115,255,.04));filter:blur(9px); }}
.holo-platform {{ width:78%;height:20%;bottom:7%;animation:platformPulse 3.8s ease-in-out infinite; }}
@keyframes platformPulse {{ 0%,100% {{ filter:brightness(.9);box-shadow:0 0 18px #078bff,0 0 50px rgba(0,166,255,.7),inset 0 0 20px #31dfff; }} 50% {{ filter:brightness(1.35);box-shadow:0 0 28px #078bff,0 0 75px rgba(0,166,255,.9),inset 0 0 28px #31dfff; }} }}
.brand-message {{ padding:2.25rem clamp(1.3rem,2.6vw,2.8rem); }}
.brand-message-head {{ font-size:clamp(1.7rem,3.2vw,3rem);gap:1rem; }}
.brand-message-head svg {{ width:clamp(80px,8vw,112px);height:clamp(80px,8vw,112px); }}
.brand-slogan {{ font-size:clamp(1.1rem,2vw,1.55rem); }}
.brand-divider {{ width:82%;margin:.6rem auto 1.8rem; }}
.brand-description {{ font-size:clamp(1.05rem,1.6vw,1.35rem);max-width:560px;margin-bottom:2rem; }}
.channel-links {{ gap:.8rem;justify-content:space-between; }}
.channel-pill {{ min-width:0;flex:1;padding:.9rem .8rem;border-radius:18px;font-size:clamp(.88rem,1.15vw,1.1rem);transition:transform .25s ease,filter .25s ease,box-shadow .25s ease; }}
.channel-pill:hover {{ transform:translateY(-5px) scale(1.025);filter:brightness(1.17);box-shadow:0 12px 30px rgba(0,130,255,.3); }}
.channel-pill svg {{ width:36px;height:36px; }}
.brand-bottom {{ display:grid;grid-template-columns:repeat(3,minmax(110px,1fr)) repeat(3,minmax(90px,.9fr)) 1px minmax(110px,1fr);align-items:stretch;gap:.65rem;margin-top:1rem;padding:.7rem .2rem .2rem; }}
.brand-bottom-item {{ min-width:0;min-height:164px;justify-content:center;border:1px solid rgba(31,123,255,.2);border-radius:21px;background:linear-gradient(155deg,rgba(9,28,63,.9),rgba(5,13,34,.97));box-shadow:inset 0 0 24px rgba(0,116,255,.07),0 10px 25px rgba(0,0,0,.2);font-size:.88rem;transition:transform .25s ease,border-color .25s ease,box-shadow .25s ease; }}
.brand-bottom-item:hover {{ transform:translateY(-5px);border-color:rgba(57,213,255,.78);box-shadow:0 0 25px rgba(0,126,255,.18),inset 0 0 24px rgba(0,116,255,.1); }}
.brand-bottom-item svg {{ width:92px;height:92px; }}
.brand-bottom-item .app-tile {{ width:104px;height:104px;border-radius:28px; }}
.brand-bottom-item .app-tile svg {{ width:84px;height:84px; }}
.brand-bottom-sep {{ height:auto;min-height:135px;align-self:center; }}
.metric-card {{ min-height:158px;background:linear-gradient(145deg,#104b89,#082653)!important;border:1px solid rgba(50,184,255,.65)!important;border-radius:21px;box-shadow:inset 0 0 25px rgba(0,155,255,.12),0 12px 32px rgba(0,0,0,.24); }}
.metric-card:hover {{ border-color:#52eaff!important;box-shadow:0 0 26px rgba(0,139,255,.23),0 15px 35px rgba(0,0,0,.3); }}
.section-heading {{ margin-top:1.4rem; }}
.section-card,[data-testid="stVerticalBlockBorderWrapper"] {{ background:linear-gradient(145deg,#0b2852,#07172f)!important;border:1px solid rgba(34,139,255,.4)!important;box-shadow:inset 0 0 22px rgba(0,118,255,.055),0 12px 30px rgba(0,0,0,.18); }}
@media(max-width:760px) {{
 .brand-top {{ grid-template-columns:1fr 1fr 1fr;gap:.2rem; }}
 .brand-top-item:first-child svg,.brand-top-item:nth-child(3) svg {{ width:clamp(75px,21vw,125px);height:clamp(75px,21vw,125px); }}
 .brand-top-item:nth-child(2) svg {{ width:clamp(85px,24vw,140px);height:clamp(78px,22vw,130px); }}
 .brand-top-item strong {{ font-size:.67rem; }}
 .brand-top-item small {{ font-size:.43rem;letter-spacing:.08em; }}
 .brand-tag {{ font-size:.55rem;padding:.25rem .38rem; }}
 .brand-middle {{ grid-template-columns:1fr; }}
 .holo-visual {{ min-height:330px; }}
 .holo-logo {{ width:55%; }}
 .brand-message-head {{ font-size:1.55rem;white-space:normal; }}
 .brand-message-head svg {{ width:62px;height:62px; }}
 .brand-description {{ font-size:.94rem; }}
 .channel-pill {{ padding:.65rem .35rem;gap:.3rem;font-size:.68rem; }}
 .channel-pill svg {{ width:25px;height:25px; }}
 .brand-bottom {{ grid-template-columns:repeat(3,minmax(0,1fr));gap:.5rem;padding:.6rem 0 0; }}
 .brand-bottom-item {{ min-height:112px;padding:.55rem .2rem;font-size:.62rem; }}
 .brand-bottom-item svg {{ width:54px;height:54px; }}
 .brand-bottom-item .app-tile {{ width:60px;height:60px;border-radius:18px; }}
 .brand-bottom-item .app-tile svg {{ width:50px;height:50px; }}
 .brand-bottom-sep {{ display:none; }}
 .metric-card {{ min-height:132px; }}
}}
@media(prefers-reduced-motion:reduce) {{
 .brand-showcase:after,.holo-orbit,.holo-platform,.holo-logo,.channel-pill,.brand-bottom-item {{ animation:none!important;transition:none!important; }}
}}
</style>
""", unsafe_allow_html=True)


st.markdown("""
<style>
/* Sistema visual unificado: overrides finales para evitar estilos heredados */
:root { --bf-blue:#087dff; --bf-electric:#168bff; --bf-cyan:#35e5ff; --bf-ink:#050d20; --bf-panel:#0a1b38; --bf-panel-2:#0d2850; }
[data-testid="stSidebar"] {
  background: linear-gradient(180deg,#07152d 0%,#061127 55%,#040b1b 100%) !important;
  border-right:1px solid rgba(22,139,255,.32) !important;
  box-shadow:12px 0 38px rgba(0,0,0,.16);
}
[data-testid="stSidebar"] > div { padding:1.1rem .9rem 1rem !important; }
.sidebar-brand { display:flex;align-items:center;gap:.78rem;padding:.45rem .25rem 1.35rem;border-bottom:1px solid rgba(66,155,255,.17); }
.sidebar-brand-mark { width:48px;height:48px;display:grid;place-items:center;border-radius:15px;background:linear-gradient(145deg,#0c2d5d,#07152e);border:1px solid rgba(53,229,255,.5);box-shadow:0 0 22px rgba(0,132,255,.2),inset 0 0 15px rgba(0,132,255,.12); }
.sidebar-brand-mark svg { width:39px;height:39px;filter:drop-shadow(0 0 7px rgba(53,229,255,.7)); }
.sidebar-brand-name { color:#f3f8ff;font-size:.91rem;font-weight:950;letter-spacing:.035em;white-space:nowrap; }
.sidebar-brand-name span { color:#36dfff; }
.sidebar-brand-caption { color:#76a9dc;font-size:.53rem;letter-spacing:.15em;font-weight:800;margin-top:.2rem;white-space:nowrap; }
.sidebar-kicker { color:#5f8fca;font-size:.62rem;font-weight:900;letter-spacing:.16em;padding:.95rem .45rem .42rem; }
.sidebar-divider { height:1px;background:rgba(66,155,255,.16);margin:.75rem .2rem .15rem; }
[data-testid="stSidebar"] [data-testid="stRadio"] > label { display:none; }
[data-testid="stSidebar"] [data-testid="stRadio"] [role="radiogroup"] { gap:.32rem; }
[data-testid="stSidebar"] [data-testid="stRadio"] [role="radiogroup"] > label {
  min-height:43px;padding:.55rem .72rem;margin:0;border:1px solid transparent;border-radius:12px;
  background:transparent;transition:background .18s ease,border-color .18s ease,transform .18s ease;
}
[data-testid="stSidebar"] [data-testid="stRadio"] [role="radiogroup"] > label:hover {
  background:rgba(15,89,166,.2);border-color:rgba(47,162,255,.25);transform:translateX(2px);
}
[data-testid="stSidebar"] [data-testid="stRadio"] [role="radiogroup"] > label:has(input:checked) {
  background:linear-gradient(100deg,rgba(0,125,255,.25),rgba(0,125,255,.08));
  border-color:rgba(53,211,255,.48);box-shadow:inset 3px 0 0 #168bff,0 5px 18px rgba(0,89,255,.1);
}
[data-testid="stSidebar"] [data-testid="stRadio"] [role="radiogroup"] > label p {
  color:#c5d9f5!important;font-size:.82rem;font-weight:700;margin:0;
}
[data-testid="stSidebar"] [data-testid="stRadio"] [role="radiogroup"] > label:has(input:checked) p { color:#f4fbff!important; }
[data-testid="stSidebar"] [data-testid="stRadio"] input { accent-color:#168bff; }
[data-testid="stSidebar"] [data-testid="stSelectbox"] [data-baseweb="select"] > div {
  background:#0b2144;border:1px solid rgba(44,147,255,.3);border-radius:11px;color:#eaf4ff;
}
[data-testid="stSidebar"] [data-testid="stRadio"]:has(input[value="Oscuro"]) [role="radiogroup"] { display:flex;flex-direction:row; }
.sidebar-status { margin-top:1.15rem;padding:.85rem .8rem;border:1px solid rgba(35,139,255,.24);border-radius:15px;background:linear-gradient(145deg,rgba(10,36,75,.82),rgba(5,17,39,.94)); }
.sidebar-status-title { color:#70a8e5;font-size:.61rem;font-weight:900;letter-spacing:.15em;margin-bottom:.6rem; }
.sidebar-status-row { display:flex;align-items:center;gap:.48rem;color:#d6e6fa;font-size:.72rem;padding:.28rem 0; }
.sidebar-status-row small { margin-left:auto;color:#7898bd;font-size:.61rem; }
.status-dot { width:7px;height:7px;border-radius:50%;display:inline-block; }
.status-ready { background:#39d6ae;box-shadow:0 0 9px rgba(57,214,174,.8); }
.status-pending { background:#f3b84b;box-shadow:0 0 8px rgba(243,184,75,.5); }
.sidebar-footer { display:flex;align-items:center;gap:.65rem;margin-top:1rem;padding:.85rem .35rem .25rem;border-top:1px solid rgba(66,155,255,.16); }
.sidebar-footer-mark { color:#35e5ff;font-size:1.5rem;text-shadow:0 0 12px #087dff; }
.sidebar-footer strong { display:block;color:#cfe4ff;font-size:.67rem;letter-spacing:.05em; }
.sidebar-footer small { display:block;color:#668bb7;font-size:.58rem;margin-top:.12rem; }
.metric-card { background:linear-gradient(145deg,#104b89,#082653)!important;border:1px solid rgba(50,184,255,.58)!important; }
.metric-card:hover { transform:translateY(-4px);border-color:#52eaff!important;box-shadow:0 0 26px rgba(0,139,255,.22),0 15px 35px rgba(0,0,0,.3); }
.section-heading { display:flex;align-items:center;gap:.85rem;margin:.6rem 0 1.15rem;padding:.3rem 0 .9rem;border-bottom:1px solid rgba(30,137,255,.24); }
.section-hex { width:43px;height:43px;display:grid;place-items:center;border:1px solid rgba(53,229,255,.4);border-radius:13px;background:rgba(0,113,255,.12);font-size:1.75rem;color:#35e5ff;text-shadow:0 0 12px #087dff; }
.section-title { color:#f4f8ff;font-size:1.42rem;font-weight:900;letter-spacing:-.025em; }
.section-subtitle { color:#91a9d1;font-size:.82rem;margin-top:.18rem; }
[data-testid="stVerticalBlockBorderWrapper"] { border-color:rgba(36,139,255,.34)!important;box-shadow:inset 0 0 20px rgba(0,118,255,.045),0 10px 28px rgba(0,0,0,.16)!important; }
[data-testid="stVerticalBlockBorderWrapper"]:hover { border-color:rgba(53,229,255,.65)!important;box-shadow:0 0 22px rgba(0,119,255,.12)!important; }
div.stButton > button,div.stFormSubmitButton > button { border-radius:12px!important;font-weight:800!important;transition:transform .18s ease,box-shadow .18s ease!important; }
div.stButton > button:hover,div.stFormSubmitButton > button:hover { transform:translateY(-2px); }
@media(max-width:760px) {
  [data-testid="stSidebar"] > div { padding:.8rem .65rem !important; }
  .sidebar-brand { gap:.55rem;padding-bottom:1rem; }
  .sidebar-brand-mark { width:42px;height:42px; }
  .sidebar-brand-name { font-size:.82rem; }
  .sidebar-brand-caption { font-size:.47rem; }
  .sidebar-status { padding:.7rem; }
  .brand-top { gap:.1rem!important; }
  .brand-middle { border-radius:19px!important; }
  .brand-bottom-item { border-color:rgba(31,123,255,.35)!important; }
}
@media(prefers-reduced-motion:reduce) {
  [data-testid="stSidebar"] *, .metric-card, div.stButton > button { transition:none!important; }
}
</style>
""", unsafe_allow_html=True)


st.markdown("""
<style>
/* BOT FACTORY AI — corrección de jerarquía visual y navegación */
[data-testid="stSidebar"] {
  width: 258px !important;
  background: #071329 !important;
  border-right: 1px solid rgba(55,145,255,.2) !important;
}
[data-testid="stSidebar"] > div { padding: 1rem .72rem !important; }
.sidebar-brand { gap:.58rem !important; padding:.35rem .15rem 1rem !important; }
.sidebar-brand-mark { width:38px !important; height:38px !important; border-radius:12px !important; }
.sidebar-brand-mark svg { width:29px !important; height:29px !important; }
.sidebar-brand-name { font-size:.78rem !important; letter-spacing:.025em !important; }
.sidebar-brand-caption { font-size:.47rem !important; letter-spacing:.11em !important; }
.sidebar-kicker { font-size:.56rem !important; padding:.72rem .38rem .34rem !important; }
[data-testid="stSidebar"] [data-testid="stRadio"] [role="radiogroup"] { gap:.2rem !important; }
[data-testid="stSidebar"] [data-testid="stRadio"] [role="radiogroup"] > label {
  min-height:37px !important; padding:.42rem .58rem !important; border-radius:9px !important;
  margin:0 !important; transform:none !important;
}
[data-testid="stSidebar"] [data-testid="stRadio"] [role="radiogroup"] > label p {
  font-size:.76rem !important; font-weight:650 !important; letter-spacing:0 !important;
}
[data-testid="stSidebar"] [data-testid="stRadio"] [role="radiogroup"] > label:has(input:checked) {
  background:rgba(13,119,255,.17) !important; border-color:rgba(44,160,255,.34) !important;
  box-shadow:inset 2px 0 0 #168bff !important;
}
[data-testid="stSidebar"] [data-testid="stRadio"] [role="radiogroup"] > label:hover {
  transform:none !important; background:rgba(18,86,158,.18) !important;
}
.sidebar-status { padding:.65rem .68rem !important; margin-top:.8rem !important; border-radius:11px !important; }
.sidebar-status-row { font-size:.66rem !important; }
.sidebar-footer { margin-top:.7rem !important; padding:.65rem .25rem .1rem !important; }
.sidebar-footer-mark { font-size:1.1rem !important; }

/* Portada: composición equilibrada, sin la fila decorativa de iconos */
.bf-hero {
  position:relative; display:grid; grid-template-columns:1.08fr .92fr; align-items:center;
  gap:1rem; min-height:370px; padding:clamp(1.4rem,3vw,2.8rem);
  overflow:hidden; border-radius:24px; border:1px solid rgba(35,137,255,.34);
  background:radial-gradient(ellipse at 76% 50%,rgba(0,130,255,.16),transparent 38%),linear-gradient(125deg,#07152d,#0a1d3b 58%,#08152c);
  box-shadow:0 18px 46px rgba(0,0,0,.22);
}
.bf-hero:before { content:"";position:absolute;inset:0;pointer-events:none;opacity:.16;
  background-image:linear-gradient(rgba(125,169,230,.1) 1px,transparent 1px),linear-gradient(90deg,rgba(125,169,230,.1) 1px,transparent 1px);background-size:32px 32px; }
.bf-hero-copy { position:relative;z-index:2;max-width:620px; }
.bf-eyebrow { display:inline-flex;align-items:center;gap:.48rem;color:#9bcfff;font-size:.63rem;font-weight:850;letter-spacing:.12em; }
.bf-eyebrow span,.bf-robot-caption span { width:7px;height:7px;border-radius:50%;background:#42dfb6;box-shadow:0 0 10px #42dfb6; }
.bf-hero h1 { margin:.9rem 0 .75rem;font-size:clamp(2.2rem,4vw,3.65rem);line-height:1.02;letter-spacing:-.055em;font-weight:900;color:#f5f8ff; }
.bf-hero h1 em { font-style:normal;color:#42cfff; }
.bf-hero-copy p { max-width:520px;color:#b6c8e3;font-size:.96rem;line-height:1.65; }
.bf-hero-actions { display:flex;flex-wrap:wrap;gap:.5rem;margin-top:1.25rem; }
.bf-hero-chip { padding:.48rem .65rem;border:1px solid rgba(127,172,231,.2);border-radius:9px;background:rgba(255,255,255,.045);color:#dceaff;font-size:.7rem;font-weight:650; }
.bf-hero-chip b { color:#45d9ff;margin-right:.35rem;font-size:.64rem; }
.bf-hero-visual { position:relative;min-height:300px;display:grid;place-items:center;overflow:hidden; }
.bf-robot-glow { position:absolute;width:210px;height:210px;border-radius:50%;background:rgba(0,152,255,.2);filter:blur(36px); }
.bf-robot { position:relative;z-index:2;width:min(64%,205px);filter:drop-shadow(0 12px 25px rgba(0,130,255,.32));animation:bfRobotFloat 5s ease-in-out infinite; }
.bf-robot svg { width:100%;height:auto;display:block; }
.bf-robot-orbit { position:absolute;width:88%;height:34%;border:1px solid rgba(42,201,255,.42);border-radius:50%;transform:rotate(-18deg);box-shadow:0 0 17px rgba(0,146,255,.18); }
.bf-robot-orbit.second { width:96%;height:42%;transform:rotate(24deg);border-color:rgba(126,83,255,.38); }
.bf-robot-caption { position:absolute;bottom:2%;z-index:3;display:flex;align-items:center;gap:.45rem;padding:.4rem .7rem;border:1px solid rgba(80,164,255,.25);border-radius:99px;background:rgba(5,18,40,.86);color:#b9d5f7;font-size:.58rem;font-weight:800;letter-spacing:.1em; }
@keyframes bfRobotFloat { 0%,100%{transform:translateY(0)}50%{transform:translateY(-8px)} }
.bf-section-intro { display:flex;align-items:center;justify-content:space-between;gap:1rem;margin:1.45rem 0 .85rem; }
.bf-section-intro h2 { margin:0;color:#f3f7ff;font-size:1.25rem;font-weight:850; }
.bf-section-intro p { margin:.18rem 0 0;color:#8fa9cc;font-size:.75rem; }
.bf-session-tag { color:#8eb9e9;border:1px solid rgba(54,145,255,.24);border-radius:99px;padding:.34rem .58rem;font-size:.55rem;font-weight:800;letter-spacing:.09em; }
.metric-card { min-height:122px !important;padding:.82rem .92rem !important;border-radius:15px !important;background:linear-gradient(145deg,#10396b,#0a2347) !important; }
.metric-icon { font-size:1rem !important;line-height:1.1 !important;margin-bottom:.35rem !important;color:#64ddff !important; }
.metric-label { font-size:.72rem !important; }
.metric-value { font-size:1.72rem !important;margin-top:.16rem !important; }
.section-heading { gap:.62rem !important;margin:.25rem 0 .85rem !important;padding-bottom:.65rem !important; }
.section-hex { width:32px !important;height:32px !important;border-radius:9px !important;font-size:1.25rem !important; }
.section-title { font-size:1.05rem !important; }
.section-subtitle { font-size:.7rem !important; }
.bf-connector-list { display:flex;flex-direction:column;gap:.35rem; }
.bf-connector-row { display:flex;align-items:center;gap:.65rem;padding:.62rem .1rem;border-bottom:1px solid rgba(96,151,216,.12); }
.bf-connector-row:last-child { border-bottom:0; }
.bf-connector-icon,.bf-provider-icon { width:34px;height:34px;flex:0 0 34px;display:grid;place-items:center;border-radius:10px;font-size:1rem;font-weight:800;color:#fff; }
.bf-connector-icon.telegram { background:#087bc9; }
.bf-connector-icon.email { background:#6042c4; }
.bf-connector-icon.whatsapp { background:#087d55; }
.bf-connector-copy { min-width:0;display:flex;flex-direction:column;gap:.13rem; }
.bf-connector-copy strong,.bf-provider-row strong { color:#eef5ff;font-size:.77rem; }
.bf-connector-copy small,.bf-provider-row small { color:#8fa9cc;font-size:.64rem;line-height:1.35; }
.bf-state { margin-left:auto;white-space:nowrap;border-radius:99px;padding:.24rem .43rem;font-size:.55rem;font-weight:800; }
.bf-state.ready { color:#71e4c0;background:rgba(40,194,143,.1);border:1px solid rgba(40,194,143,.22); }
.bf-state.pending { color:#e6c27c;background:rgba(210,158,55,.1);border:1px solid rgba(210,158,55,.2); }
.bf-provider-row { display:flex;align-items:center;gap:.65rem; }
.bf-provider-icon { background:#173d77;color:#65dfff;font-size:1.15rem; }
.bf-provider-row > div:last-child { display:flex;flex-direction:column;gap:.16rem; }
@media(max-width:900px) {
  .bf-hero { grid-template-columns:1fr .72fr;min-height:330px;padding:1.25rem; }
  .bf-robot { width:min(75%,180px); }
}
@media(max-width:680px) {
  [data-testid="stSidebar"] { width:100% !important; }
  .bf-hero { grid-template-columns:1fr;gap:.2rem;min-height:unset;padding:1.25rem 1.1rem 1rem; }
  .bf-hero-copy { text-align:center;margin:auto; }
  .bf-eyebrow { justify-content:center;font-size:.54rem; }
  .bf-hero h1 { font-size:2.15rem; }
  .bf-hero-copy p { font-size:.84rem;margin:.5rem auto; }
  .bf-hero-actions { justify-content:center; }
  .bf-hero-visual { min-height:210px; }
  .bf-robot { width:135px; }
  .bf-robot-caption { bottom:0; }
  .bf-section-intro { align-items:flex-start; }
  .metric-card { min-height:112px !important; }
  .bf-connector-copy small { font-size:.6rem; }
}
@media(prefers-reduced-motion:reduce) { .bf-robot { animation:none !important; } }
</style>
""", unsafe_allow_html=True)


def metric_card(label, value, icon, note, palette):
    # Todas las tarjetas comparten el azul eléctrico de la marca.
    st.markdown(
        f'<div class="metric-card" style="--card-a:#10396e;--card-b:#0a2450;--card-text:#F3F8FF;--card-border:rgba(45,157,255,.58)">'
        f'<div class="metric-icon">{icon}</div><div class="metric-label">{label}</div>'
        f'<div class="metric-value">{value}</div><div class="metric-label">{note}</div></div>',
        unsafe_allow_html=True,
    )

def section_heading(title, subtitle=None):
    st.markdown(
        '<div class="section-heading"><span class="section-hex">⬡</span><div><div class="section-title">'
        + title + '</div><div class="section-subtitle">' + (subtitle or '') + '</div></div></div>',
        unsafe_allow_html=True,
    )

with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand">
      <div class="sidebar-brand-mark">
        <svg viewBox="0 0 100 100" role="img" aria-label="BOT FACTORY AI">
          <path d="M28 7h44l21 43-21 43H28L7 50z" fill="none" stroke="#36dfff" stroke-width="6"/>
          <path d="M50 25v13M31 60l12-7m26 7-12-7M50 75V62" stroke="#36dfff" stroke-width="5" stroke-linecap="round"/>
          <path d="M50 38l13 7v15l-13 8-13-8V45z" fill="#0b2852" stroke="#168bff" stroke-width="4"/>
        </svg>
      </div>
      <div><div class="sidebar-brand-name">BOT FACTORY <span>AI</span></div>
      <div class="sidebar-brand-caption">AUTOMATION WORKSPACE</div></div>
    </div>
    <div class="sidebar-kicker">PLATAFORMA</div>
    """, unsafe_allow_html=True)
    nav_options = ["INICIO", "ACCESO DE USUARIO", "BOTS", "AGENTES IA", "CANALES", "PLANTILLAS", "PLANES Y SERVICIOS", "ADMINISTRACIÓN", "CONFIGURACIÓN"]
    nav_labels = {
        "INICIO": "⌂   Inicio",
        "ACCESO DE USUARIO": "◎   Acceso de usuario",
        "BOTS": "▦   Mis bots",
        "AGENTES IA": "✳   Agentes IA",
        "CANALES": "↔   Canales",
        "PLANTILLAS": "▧   Plantillas",
        "PLANES Y SERVICIOS": "◈   Planes y servicios",
        "ADMINISTRACIÓN": "⚙   Administración",
        "CONFIGURACIÓN": "☰   Configuración",
    }
    page = st.radio("NAVEGACIÓN", nav_options, format_func=lambda item: nav_labels[item], label_visibility="collapsed", key="main_navigation")
    st.markdown('<div class="sidebar-divider"></div><div class="sidebar-kicker">PREFERENCIAS</div>', unsafe_allow_html=True)
    st.radio("Tema", ["Oscuro", "Claro"], key="theme_choice", horizontal=True, label_visibility="collapsed")
    st.markdown('<div class="sidebar-kicker">VISTA DE TRABAJO</div>', unsafe_allow_html=True)
    st.selectbox("Rol de vista", ["Administrador", "Usuario"], key="role_preview", label_visibility="collapsed")
    st.caption("Selector demostrativo. Los permisos reales se aplicarán con Supabase Auth y RLS.")
    st.markdown("""
    <div class="sidebar-status">
      <div class="sidebar-status-title">CANALES</div>
      <div class="sidebar-status-row"><span class="status-dot status-ready"></span><span>Telegram</span><small>MVP</small></div>
      <div class="sidebar-status-row"><span class="status-dot status-pending"></span><span>Correo</span><small>En desarrollo</small></div>
      <div class="sidebar-status-row"><span class="status-dot status-pending"></span><span>WhatsApp</span><small>En desarrollo</small></div>
    </div>
    <div class="sidebar-footer"><span class="sidebar-footer-mark">⬡</span><div><strong>BOT FACTORY AI</strong><small>Intelligent automation</small></div></div>
    """, unsafe_allow_html=True)

total_bots = len(st.session_state.bot_registry)
total_agents = len(st.session_state.agent_registry)
telegram_count = sum(1 for bot in st.session_state.bot_registry if bot.get("channel") == "Telegram")
email_count = sum(1 for bot in st.session_state.bot_registry if bot.get("channel") == "Correo")
whatsapp_count = sum(1 for bot in st.session_state.bot_registry if bot.get("channel") == "WhatsApp")

if not page.startswith("INICIO"):
    st.markdown('<div class="brandbar"><div class="brandmark"><svg viewBox="0 0 100 100" role="img" aria-label="BOT FACTORY AI"><defs><linearGradient id="bfLogo" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#32e6ff"/><stop offset=".58" stop-color="#278cff"/><stop offset="1" stop-color="#b35cff"/></linearGradient></defs><path d="M29 7h42l22 43-22 43H29L7 50z" fill="none" stroke="url(#bfLogo)" stroke-width="7" stroke-linejoin="round"/><path d="M50 25v13M31 60l12-7m26 7-12-7M50 75V62" stroke="#55eaff" stroke-width="5" stroke-linecap="round"/><path d="M50 38l13 7v15l-13 8-13-8V45z" fill="#102b57" stroke="#55eaff" stroke-width="4"/><circle cx="50" cy="18" r="5" fill="#55eaff"/><circle cx="26" cy="63" r="5" fill="#55eaff"/><circle cx="74" cy="63" r="5" fill="#b66cff"/><circle cx="50" cy="81" r="5" fill="#55eaff"/></svg></div><div><div class="brandname">BOT FACTORY AI</div><div class="brandtag">INTELLIGENT AUTOMATION PLATFORM</div></div><div class="brand-spacer"></div><div class="brand-pill">AI WORKSPACE</div></div>', unsafe_allow_html=True)

if page.startswith("ACCESO"):
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

elif page.startswith("INICIO"):
    st.markdown("""
    <section class="bf-hero">
      <div class="bf-hero-copy">
        <div class="bf-eyebrow"><span></span> PLATAFORMA DE AUTOMATIZACIÓN INTELIGENTE</div>
        <h1>Tu fábrica de<br><em>bots inteligentes.</em></h1>
        <p>Crea, conecta y administra asistentes de IA para Telegram, correo electrónico y WhatsApp desde un solo espacio de trabajo.</p>
        <div class="bf-hero-actions">
          <div class="bf-hero-chip"><b>01</b> Diseña agentes</div>
          <div class="bf-hero-chip"><b>02</b> Conecta canales</div>
          <div class="bf-hero-chip"><b>03</b> Automatiza tareas</div>
        </div>
      </div>
      <div class="bf-hero-visual">
        <div class="bf-robot-orbit"></div><div class="bf-robot-orbit second"></div>
        <div class="bf-robot-glow"></div>
        <div class="bf-robot"><svg viewBox="0 0 180 160" aria-label="Mascota robot BOT FACTORY AI"><defs><linearGradient id="botShell" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#ffffff"/><stop offset=".28" stop-color="#c9f2ff"/><stop offset=".62" stop-color="#5ba9ed"/><stop offset="1" stop-color="#123e91"/></linearGradient><linearGradient id="botFace" x1="0" y1="0" x2="0" y2="1"><stop stop-color="#07142f"/><stop offset="1" stop-color="#020817"/></linearGradient><linearGradient id="botBlue" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#50f7ff"/><stop offset=".5" stop-color="#078bff"/><stop offset="1" stop-color="#722bff"/></linearGradient><filter id="botGlow"><feGaussianBlur stdDeviation="3" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs><ellipse cx="91" cy="151" rx="56" ry="7" fill="#087dff" opacity=".45"/><path d="M44 50C35 8 63 3 91 3s55 8 47 48" fill="none" stroke="url(#botBlue)" stroke-width="7" stroke-linecap="round"/><circle cx="91" cy="5" r="5" fill="#6efaff" filter="url(#botGlow)"/><path d="M44 33Q28 32 28 53v23q0 13 15 13h8V33zM138 33q15-1 15 20v23q0 13-15 13h-8V33z" fill="url(#botShell)" stroke="#178fff" stroke-width="3"/><circle cx="36" cy="63" r="10" fill="#0b2c66" stroke="#50eaff" stroke-width="3"/><circle cx="146" cy="63" r="10" fill="#0b2c66" stroke="#50eaff" stroke-width="3"/><rect x="43" y="14" width="96" height="82" rx="34" fill="url(#botShell)" stroke="#56eaff" stroke-width="3"/><rect x="52" y="25" width="78" height="58" rx="26" fill="url(#botFace)" stroke="#267dcb" stroke-width="2"/><path d="M68 54q8-16 17 0M99 54q8-16 17 0" fill="none" stroke="#00edff" stroke-width="7" stroke-linecap="round" filter="url(#botGlow)"/><path d="M55 94q35-17 71 0l21 57H35z" fill="url(#botShell)" stroke="#258fff" stroke-width="3"/><path d="M91 101l20 12v24l-20 12-20-12v-24z" fill="#08285c" stroke="#35edff" stroke-width="4"/><path d="M91 109l12 7v14l-12 7-12-7v-14z" fill="#087dff" stroke="#a6faff" stroke-width="2"/><path d="M40 102q-17-8-21 8l-5 17q-2 11 9 15l24 6 12-25q5-13-8-18z" fill="url(#botShell)" stroke="#168bff" stroke-width="3"/><path d="M136 103q17-8 21 8l5 17q2 11-9 15l-24 6-12-25q-5-13 8-18z" fill="url(#botShell)" stroke="#168bff" stroke-width="3"/><path d="M15 123q-3 8 4 13l20 8 7-14-19-13q-8-4-12 6z" fill="#dffaff" stroke="#168bff" stroke-width="2"/><path d="M164 123q3 8-4 13l-20 8-7-14 19-13q8-4 12 6z" fill="#dffaff" stroke="#168bff" stroke-width="2"/></svg></div>
        <div class="bf-robot-caption"><span></span> ASISTENTE BOT FACTORY AI</div>
      </div>
    </section>
    """, unsafe_allow_html=True)

    st.markdown('<div class="bf-section-intro"><div><h2>Centro de operaciones</h2><p>Resumen de tu espacio de trabajo y actividad reciente.</p></div><span class="bf-session-tag">SESIÓN ACTUAL</span></div>', unsafe_allow_html=True)
    cols = st.columns(4)
    with cols[0]: metric_card("Bots registrados", total_bots, "▣", "En tu espacio de trabajo", "blue")
    with cols[1]: metric_card("Agentes IA", total_agents, "✧", "Definiciones creadas", "blue")
    with cols[2]: metric_card("Telegram", telegram_count, "➤", "Bots asociados", "blue")
    with cols[3]: metric_card("Canales", 3, "⇄", "Telegram · Correo · WhatsApp", "blue")

    left, right = st.columns([1.15, 1])
    with left:
        with st.container(border=True):
            section_heading("Actividad reciente", "Bots y agentes creados en esta sesión")
            if not st.session_state.bot_registry and not st.session_state.agent_registry:
                st.info("Tu espacio está listo. Crea tu primer bot o agente para comenzar.")
            for bot in st.session_state.bot_registry[-5:]:
                st.markdown(f"**▣ {bot['name']}** · {bot['channel']}")
                st.caption(f"{bot['status']} · {bot['client'] or 'Espacio interno'}")
            for agent in st.session_state.agent_registry[-5:]:
                st.markdown(f"**✧ {agent['name']}** · {agent['provider']}")
                st.caption(f"{agent['status']} · {agent['channel']}")

    with right:
        with st.container(border=True):
            section_heading("Conectores", "Disponibilidad de los canales de comunicación")
            st.markdown("""
            <div class="bf-connector-list">
              <div class="bf-connector-row">
                <div class="bf-connector-icon telegram">➤</div>
                <div class="bf-connector-copy"><strong>Telegram</strong><small>Worker MVP creado · requiere prueba real</small></div>
                <span class="bf-state ready">MVP</span>
              </div>
              <div class="bf-connector-row">
                <div class="bf-connector-icon email">✉</div>
                <div class="bf-connector-copy"><strong>Correo electrónico</strong><small>Conector pendiente de implementación</small></div>
                <span class="bf-state pending">Pendiente</span>
              </div>
              <div class="bf-connector-row">
                <div class="bf-connector-icon whatsapp">◉</div>
                <div class="bf-connector-copy"><strong>WhatsApp</strong><small>Integración oficial pendiente</small></div>
                <span class="bf-state pending">Pendiente</span>
              </div>
            </div>
            """, unsafe_allow_html=True)
        with st.container(border=True):
            section_heading("Motor de inteligencia artificial", "Proveedor disponible en el MVP")
            st.markdown('<div class="bf-provider-row"><div class="bf-provider-icon">✦</div><div><strong>Google Gemini</strong><small>Adaptador implementado · requiere configurar API key</small></div></div>', unsafe_allow_html=True)


elif page.startswith("BOTS"):
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

elif page.startswith("AGENTES"):
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

elif page.startswith("CANALES"):
    section_heading("Canales de comunicación", "Conectores para desplegar tus automatizaciones donde están tus usuarios.")
    channel_data = [("✈️","Telegram","MVP creado","Worker independiente y comandos /start, /help y /status. Requiere token privado de BotFather y prueba real."),("✉️","Correo electrónico","En planificación","Diseño de recepción, clasificación, respuestas y notificaciones con APIs/SMTP seguro."),("💬","WhatsApp","En planificación","Integración mediante API oficial o proveedor autorizado, con plantillas y consentimiento.")]
    for icon, title, status, desc in channel_data:
        with st.container(border=True):
            st.markdown(f"### {icon} {title}")
            st.caption(status)
            st.write(desc)

elif page.startswith("PLANTILLAS"):
    section_heading("Biblioteca de plantillas", "Puntos de partida para acelerar cada implementación.")
    templates = [("🛍️","Agente comercial","Califica consultas, responde preguntas y deriva oportunidades."),("🎧","Agente de soporte","Resuelve preguntas frecuentes y escala casos complejos."),("📁","Agente administrativo","Clasifica documentos y organiza tareas."),("🔔","Telegram · Alertas","Envía notificaciones operativas."),("📨","Correo · Clasificador","Organiza correos por categoría y prioridad."),("💬","WhatsApp · Atención","Atiende consultas mediante integración oficial.")]
    cols = st.columns(2)
    for i,(icon,title,detail) in enumerate(templates):
        with cols[i%2]:
            with st.container(border=True):
                st.markdown(f"### {icon} {title}")
                st.write(detail)
                st.caption("Plantilla conceptual · automatización pendiente de conexión")

elif page.startswith("PLANES"):
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

elif page.startswith("ADMINISTRACIÓN"):
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
