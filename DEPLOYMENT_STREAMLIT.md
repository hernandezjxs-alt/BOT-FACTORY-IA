# ☁️ Despliegue de BOT FACTORY AI en Streamlit Community Cloud

Esta guía permite publicar el panel desde un teléfono Android usando GitHub. No requiere instalar Python en el celular.

## 📌 1. Antes de empezar
- Repositorio: https://github.com/hernandezjxs-alt/BOT-FACTORY-IA
- Rama: main
- Archivo principal: app.py
- Dependencias: requirements.txt
- Revoca cualquier API key de Gemini que hayas compartido en un chat y crea una nueva. No la envíes por mensajes ni la guardes en GitHub.

## 📌 2. Crear la cuenta / entrar
1. Abre https://share.streamlit.io desde Chrome en el celular.
2. Pulsa Continue to sign-in y luego Continue with GitHub.
3. Autoriza Streamlit para acceder a tus repositorios públicos de GitHub.

## 📌 3. Crear la aplicación
1. Pulsa Create app.
2. Elige que ya tienes una aplicación (Yup, I have an app).
3. Repository: hernandezjxs-alt/BOT-FACTORY-IA.
4. Branch: main.
5. Main file path: app.py.
6. En App URL puedes elegir un subdominio si está disponible.
7. En Advanced settings selecciona Python 3.12 si aparece disponible.
8. Pulsa Deploy.

## 🧠 4. Guardar la API key de Gemini de forma privada
En Advanced settings, localiza Secrets y pega estas líneas sustituyendo el texto de ejemplo por tu nueva clave privada:

```toml
GEMINI_API_KEY = "PEGA_AQUI_TU_NUEVA_CLAVE"
GEMINI_MODEL = "gemini-2.5-flash-lite"
```

No compartas una captura donde se vea la clave. No la escribas en app.py, .env.example, GitHub, issues ni comentarios.

Si ya desplegaste sin configurar Secrets: abre App settings > Secrets, agrega las dos líneas y guarda.

## 📌 5. Comprobar
1. Espera a que termine el despliegue.
2. Abre la URL terminada en streamlit.app.
3. Entra en Agent Factory.
4. Crea un agente con proveedor google, nombre, rol e instrucciones.
5. En Prueba de conversación con Gemini, escribe un mensaje y pulsa Enviar prueba a Gemini.
6. Si falla, abre Manage app y revisa los logs; comparte el mensaje de error ocultando cualquier secreto.

## 📌 Limitaciones del MVP
- Los registros de bots y agentes viven en la sesión Streamlit y pueden perderse al reiniciar o cambiar de sesión.
- Todavía no hay autenticación propia, persistencia Supabase ni aislamiento multiempresa.
- El despliegue del panel no mantiene workers Telegram/WhatsApp/correo de larga duración. Esos procesos necesitarán workers/hosting separados.
- No usar todavía con datos confidenciales de clientes.

## 📚 Documentación oficial
- https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy
- https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/secrets-management