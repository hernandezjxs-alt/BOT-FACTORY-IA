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
    st.markdown('<div style="display:flex;align-items:center;gap:10px;margin:4px 0 12px"><span style="font-size:25px;color:#36dfff;text-shadow:0 0 12px #087dff">⬡</span><div style="font-weight:900;letter-spacing:.04em">BOT FACTORY <span style="color:#a84cff">AI</span><div style="font-size:9px;letter-spacing:.16em;color:#78dfff">AUTOMATION INTELLIGENCE</div></div></div>', unsafe_allow_html=True)
    st.divider()
    page = st.radio("NAVEGACIÓN", ["INICIO", "ACCESO DE USUARIO", "BOTS", "AGENTES IA", "CANALES", "PLANTILLAS", "PLANES Y SERVICIOS", "ADMINISTRACIÓN", "CONFIGURACIÓN"], label_visibility="visible")
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
    <section class="brand-showcase">
      <div class="brand-top">
        <div class="brand-top-item">
          <svg viewBox="0 0 120 120" aria-label="Logotipo BOT FACTORY AI"><defs><linearGradient id="brandHex" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#31f5ff"/><stop offset=".55" stop-color="#087dff"/><stop offset="1" stop-color="#a52cff"/></linearGradient></defs><path d="M35 5h50l30 55-30 55H35L5 60z" fill="none" stroke="url(#brandHex)" stroke-width="8"/><path d="M60 25v17M34 72l15-9m37 9-15-9M60 95V78" stroke="#65f5ff" stroke-width="6" stroke-linecap="round"/><path d="M60 42l19 11v22L60 86 41 75V53z" fill="#092d64" stroke="#52eaff" stroke-width="5"/><path d="M60 50l11 7v13L60 77 49 70V57z" fill="#16cfff"/></svg>
          <strong>BOT FACTORY <span class="ai-word">AI</span></strong><small>AUTOMATION INTELLIGENCE</small><span class="brand-tag">Logo principal</span>
        </div>
        <div class="brand-top-item">
          <svg viewBox="0 0 180 160" aria-label="Mascota robot BOT FACTORY AI"><defs><linearGradient id="botShell" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#ffffff"/><stop offset=".28" stop-color="#c9f2ff"/><stop offset=".62" stop-color="#5ba9ed"/><stop offset="1" stop-color="#123e91"/></linearGradient><linearGradient id="botFace" x1="0" y1="0" x2="0" y2="1"><stop stop-color="#07142f"/><stop offset="1" stop-color="#020817"/></linearGradient><linearGradient id="botBlue" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#50f7ff"/><stop offset=".5" stop-color="#078bff"/><stop offset="1" stop-color="#722bff"/></linearGradient><filter id="botGlow"><feGaussianBlur stdDeviation="3" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs><ellipse cx="91" cy="151" rx="56" ry="7" fill="#087dff" opacity=".45"/><path d="M44 50C35 8 63 3 91 3s55 8 47 48" fill="none" stroke="url(#botBlue)" stroke-width="7" stroke-linecap="round"/><circle cx="91" cy="5" r="5" fill="#6efaff" filter="url(#botGlow)"/><path d="M44 33Q28 32 28 53v23q0 13 15 13h8V33zM138 33q15-1 15 20v23q0 13-15 13h-8V33z" fill="url(#botShell)" stroke="#178fff" stroke-width="3"/><circle cx="36" cy="63" r="10" fill="#0b2c66" stroke="#50eaff" stroke-width="3"/><circle cx="146" cy="63" r="10" fill="#0b2c66" stroke="#50eaff" stroke-width="3"/><rect x="43" y="14" width="96" height="82" rx="34" fill="url(#botShell)" stroke="#56eaff" stroke-width="3"/><rect x="52" y="25" width="78" height="58" rx="26" fill="url(#botFace)" stroke="#267dcb" stroke-width="2"/><path d="M68 54q8-16 17 0M99 54q8-16 17 0" fill="none" stroke="#00edff" stroke-width="7" stroke-linecap="round" filter="url(#botGlow)"/><path d="M55 94q35-17 71 0l21 57H35z" fill="url(#botShell)" stroke="#258fff" stroke-width="3"/><path d="M91 101l20 12v24l-20 12-20-12v-24z" fill="#08285c" stroke="#35edff" stroke-width="4"/><path d="M91 109l12 7v14l-12 7-12-7v-14z" fill="#087dff" stroke="#a6faff" stroke-width="2"/><path d="M40 102q-17-8-21 8l-5 17q-2 11 9 15l24 6 12-25q5-13-8-18z" fill="url(#botShell)" stroke="#168bff" stroke-width="3"/><path d="M136 103q17-8 21 8l5 17q2 11-9 15l-24 6-12-25q-5-13 8-18z" fill="url(#botShell)" stroke="#168bff" stroke-width="3"/><path d="M15 123q-3 8 4 13l20 8 7-14-19-13q-8-4-12 6z" fill="#dffaff" stroke="#168bff" stroke-width="2"/><path d="M164 123q3 8-4 13l-20 8-7-14 19-13q8-4 12 6z" fill="#dffaff" stroke="#168bff" stroke-width="2"/></svg>
          <strong>ASISTENTE IA</strong><small>CREA · CONECTA · AUTOMATIZA</small><span class="brand-tag">Mascota / Asistente</span>
        </div>
        <div class="brand-top-item">
          <svg viewBox="0 0 120 120" aria-label="Cerebro IA"><defs><linearGradient id="brainStroke" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#19efff"/><stop offset=".55" stop-color="#087dff"/><stop offset="1" stop-color="#bc39ff"/></linearGradient></defs><path d="M59 18C42 2 22 15 25 33 7 34 8 57 20 63 8 80 24 99 42 91c7 17 24 12 18-4V18zm2 0c17-16 37-3 34 15 18 1 17 24 5 30 12 17-4 36-22 28-7 17-24 12-18-4V18z" fill="none" stroke="url(#brainStroke)" stroke-width="5"/><path d="M60 15v88M34 29l15 13m-28 19 26 2M37 83l15-14m34-40L71 42m28 19-26 2m14 20L71 69" stroke="#36dcff" stroke-width="3" fill="none"/><g fill="#d6fbff" stroke="#16bfff" stroke-width="2"><circle cx="34" cy="29" r="5"/><circle cx="21" cy="61" r="5"/><circle cx="37" cy="83" r="5"/><circle cx="86" cy="29" r="5"/><circle cx="99" cy="61" r="5"/><circle cx="86" cy="83" r="5"/></g></svg>
          <strong>BOT FACTORY <span class="ai-word">AI</span></strong><small>INTELIGENCIA ARTIFICIAL</small><span class="brand-tag">Cerebro IA</span>
        </div>
      </div>
      <div class="brand-middle">
        <div class="holo-visual">
          <div class="holo-beam"></div><div class="holo-orbit"></div><div class="holo-orbit second"></div>
          <div class="holo-logo"><svg viewBox="0 0 120 120" aria-label="Símbolo holográfico BOT FACTORY"><defs><linearGradient id="holoHex" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#27f4ff"/><stop offset=".55" stop-color="#087dff"/><stop offset="1" stop-color="#ad2cff"/></linearGradient></defs><path d="M35 5h50l30 55-30 55H35L5 60z" fill="#071d4a" stroke="url(#holoHex)" stroke-width="9"/><path d="M60 25v17M34 72l15-9m37 9-15-9M60 95V78" stroke="#65f5ff" stroke-width="6" stroke-linecap="round"/><path d="M60 42l19 11v22L60 86 41 75V53z" fill="#092d64" stroke="#52eaff" stroke-width="5"/><path d="M60 50l11 7v13L60 77 49 70V57z" fill="#16cfff"/></svg></div>
          <div class="holo-platform"></div>
        </div>
        <div class="brand-message">
          <div class="brand-message-head"><svg viewBox="0 0 120 120" aria-hidden="true"><path d="M35 5h50l30 55-30 55H35L5 60z" fill="#08234e" stroke="#168bff" stroke-width="8"/><path d="M60 25v17M34 72l15-9m37 9-15-9M60 95V78" stroke="#65f5ff" stroke-width="6" stroke-linecap="round"/><path d="M60 42l19 11v22L60 86 41 75V53z" fill="#092d64" stroke="#52eaff" stroke-width="5"/></svg><span>BOT FACTORY <em>AI</em></span></div>
          <div class="brand-slogan">Crea. Conecta. Automatiza.</div><div class="brand-divider"></div>
          <div class="brand-description">Una plataforma para crear agentes inteligentes y conectar todos tus canales.</div>
          <div class="channel-links">
            <div class="channel-pill tg"><svg viewBox="0 0 24 24" aria-label="Telegram"><path fill="white" d="M21.7 4.4 18.5 20c-.24 1.1-.88 1.36-1.78.85l-4.92-3.63-2.37 2.28c-.26.26-.48.48-.98.48l.35-5.01 9.12-8.24c.4-.35-.09-.55-.62-.2L6.03 13.7l-4.82-1.5c-1.05-.33-1.07-1.05.22-1.56L20.3 3.22c.87-.32 1.63.21 1.4 1.18Z"/></svg>Telegram</div>
            <div class="channel-pill wa"><svg viewBox="0 0 24 24" aria-label="WhatsApp"><path fill="white" d="M12.04 2a9.8 9.8 0 0 0-8.42 14.82L2.3 22l5.3-1.39A9.98 9.98 0 1 0 12.04 2Zm0 18.1a8.1 8.1 0 0 1-4.13-1.13l-.3-.18-3.15.83.84-3.07-.2-.32A8.12 8.12 0 1 1 12.04 20.1Zm4.46-6.08c-.24-.12-1.42-.7-1.64-.78-.22-.08-.38-.12-.54.12-.16.24-.62.78-.76.94-.14.16-.28.18-.52.06-.24-.12-1.02-.38-1.94-1.2-.72-.64-1.2-1.43-1.34-1.67-.14-.24-.02-.37.1-.49.1-.1.24-.28.36-.42.12-.14.16-.24.24-.4.08-.16.04-.3-.02-.42-.06-.12-.54-1.3-.74-1.78-.2-.47-.4-.4-.54-.4h-.46c-.16 0-.42.06-.64.3-.22.24-.84.82-.84 2s.86 2.32.98 2.48c.12.16 1.7 2.6 4.12 3.64.58.25 1.03.4 1.38.51.58.18 1.1.15 1.51.09.46-.07 1.42-.58 1.62-1.14.2-.56.2-1.04.14-1.14-.06-.1-.22-.16-.46-.28Z"/></svg>WhatsApp</div>
            <div class="channel-pill mail"><svg viewBox="0 0 24 24" aria-label="Email"><path fill="white" d="M2 5.5A2.5 2.5 0 0 1 4.5 3h15A2.5 2.5 0 0 1 22 5.5v13a2.5 2.5 0 0 1-2.5 2.5h-15A2.5 2.5 0 0 1 2 18.5v-13Zm2 .1v.2l8 6.2 8-6.2v-.2H4Zm16 2.7-7.4 5.7a1 1 0 0 1-1.2 0L4 8.3v10.2c0 .3.2.5.5.5h15c.3 0 .5-.2.5-.5V8.3Z"/></svg>Email</div>
          </div>
        </div>
      </div>
      <div class="brand-bottom">
        <div class="brand-bottom-item"><div class="app-tile"><svg viewBox="0 0 120 120"><path d="M35 5h50l30 55-30 55H35L5 60z" fill="#071d4a" stroke="#8ceeff" stroke-width="8"/><path d="M60 25v17M34 72l15-9m37 9-15-9M60 95V78" stroke="#65f5ff" stroke-width="6" stroke-linecap="round"/><path d="M60 42l19 11v22L60 86 41 75V53z" fill="#092d64" stroke="#52eaff" stroke-width="5"/></svg></div>Icono App</div>
        <div class="brand-bottom-item"><svg viewBox="0 0 100 100"><circle cx="50" cy="50" r="44" fill="#071b3e" stroke="#19dfff" stroke-width="6"/><path d="M50 17 78 33v34L50 83 22 67V33z" fill="#0a2c62" stroke="#168bff" stroke-width="5"/><path d="M50 28v14M32 62l12-7m24 7-12-7M50 76V62" stroke="#5cecff" stroke-width="4"/><path d="M50 42l13 8v15L50 73l-13-8V50z" fill="#087dff" stroke="#6ef6ff" stroke-width="3"/></svg>Icono Circular</div>
        <div class="brand-bottom-item"><svg viewBox="0 0 100 100"><path d="M28 5h44l23 45-23 45H28L5 50z" fill="#071b3e" stroke="#22dfff" stroke-width="6"/><path d="M50 22v13M31 60l12-7m26 7-12-7M50 78V63" stroke="#5cecff" stroke-width="4"/><path d="M50 35l14 8v16L50 67l-14-8V43z" fill="#087dff" stroke="#6ef6ff" stroke-width="3"/></svg>Icono Simple</div>
        <div class="brand-bottom-item"><svg viewBox="0 0 100 100"><circle cx="50" cy="50" r="43" fill="#087fe4"/><path fill="white" d="M79 25 67 77c-.8 3.5-2.8 4.3-5.7 2.7L46.5 68.9l-7.6 7.3c-.8.8-1.5 1.5-3.1 1.5l1.1-16 29.2-26.4c1.3-1.1-.3-1.8-2-.6L33 54.8l-15.4-4.8c-3.4-1.1-3.4-3.4.7-5L74.5 20.9c2.8-1 5.2.7 4.5 4.1Z"/></svg>Telegram</div>
        <div class="brand-bottom-item"><svg viewBox="0 0 100 100"><circle cx="50" cy="50" r="43" fill="#08b85c"/><path d="M72 69 61 64c-10 8-26-7-19-18l-5-10-9 3c-5 24 30 53 51 34z" fill="none" stroke="white" stroke-width="6" stroke-linecap="round"/><path d="M50 12a38 38 0 0 0-33 57l-5 18 18-5A38 38 0 1 0 50 12z" fill="none" stroke="white" stroke-width="5"/></svg>WhatsApp</div>
        <div class="brand-bottom-item"><svg viewBox="0 0 100 100"><circle cx="50" cy="50" r="43" fill="#651be7"/><rect x="20" y="30" width="60" height="42" rx="5" fill="none" stroke="white" stroke-width="6"/><path d="m22 33 28 22 28-22" fill="none" stroke="white" stroke-width="6"/></svg>Email</div>
        <div class="brand-bottom-sep"></div>
        <div class="brand-bottom-item"><div class="app-tile"><svg viewBox="0 0 120 120"><path d="M35 5h50l30 55-30 55H35L5 60z" fill="#071d4a" stroke="#8ceeff" stroke-width="8"/><path d="M60 25v17M34 72l15-9m37 9-15-9M60 95V78" stroke="#65f5ff" stroke-width="6" stroke-linecap="round"/><path d="M60 42l19 11v22L60 86 41 75V53z" fill="#092d64" stroke="#52eaff" stroke-width="5"/></svg></div>Favicon</div>
      </div>
    </section>
    """, unsafe_allow_html=True)
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
