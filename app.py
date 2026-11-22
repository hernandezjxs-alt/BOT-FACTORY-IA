"""Punto de entrada de la interfaz BOT FACTORY AI."""

import streamlit as st
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="BOT FACTORY AI",
    page_icon="🤖",
    layout="wide",
)

st.title("🤖 BOT FACTORY AI")
st.caption("Plataforma modular para crear y administrar bots y automatizaciones.")

st.info(
    "Entorno inicial preparado. Los conectores se habilitarán por etapas "
    "comenzando por Telegram."
)

col1, col2, col3 = st.columns(3)
with col1:
    st.subheader("Telegram")
    st.write("Conector planificado para bots, comandos y notificaciones.")
with col2:
    st.subheader("Correo")
    st.write("Conector planificado para automatización de correo.")
with col3:
    st.subheader("WhatsApp")
    st.write("Integración futura mediante API o proveedor oficial.")

st.divider()
st.subheader("Estado del proyecto")
st.write("Fundaciones: en construcción")
st.write("Interfaz: Streamlit")
st.write("Backend principal: Python modular")
