# BOT FACTORY AI — Bitácora acumulada

Registro cronológico de decisiones, avances, cambios y pendientes del proyecto.

## 2026-11-22 — Inicio de documentación y continuidad

### Objetivo confirmado
Crear una empresa/plataforma de desarrollo de bots y automatizaciones para Telegram, correo electrónico y WhatsApp.

### Repositorio
- URL: https://github.com/hernandezjxs-alt/BOT-FACTORY-IA
- Propietario: hernandezjxs-alt
- Rama: main
- Visibilidad: pública.
- Se requiere mantener documentación de continuidad versionada en GitHub.

### Decisiones técnicas
- Python como lenguaje principal.
- Streamlit para la interfaz y panel de control; no FastAPI.
- Supabase para datos y autenticación.
- Redis y workers independientes para tareas asíncronas, según necesidad.
- Arquitectura modular y conectores separados por canal.
- Arquitectura multimodelo mediante adaptadores, considerando Claude y otros proveedores.

### Avance 1 — Fundaciones
- [x] Se creó memoria.md.
- [x] Se creó bitacora_acumulada.md.
- [x] Se agregó .gitignore.
- [x] Se agregó .env.example sin secretos.
- [x] Se agregó requirements.txt.
- [x] Se creó app.py con interfaz Streamlit inicial.
- [x] Se creó el paquete bot_factory.

### Avance 2 — Telegram Bot Factory MVP 0.1
- [x] Se creó bot_factory/connectors/telegram/.
- [x] Se implementaron handlers para /start, /help y /status.
- [x] Se creó el constructor de la aplicación Telegram.
- [x] Se creó run_telegram_bot.py como worker independiente.
- [x] Se documentó cómo crear el bot con @BotFather.
- [x] Se agregó python-telegram-bot a requirements.txt.
- [x] Se agregó LOG_LEVEL y TELEGRAM_BOT_TOKEN a .env.example.
- [x] El token se lee desde variable de entorno; no se incluye ningún token real en Git.

### Seguridad
El repositorio es público. No publicar tokens, contraseñas, API keys, credenciales, datos personales ni archivos .env. Si un token se expone, revocarlo y generar uno nuevo desde el proveedor.

### Estado real
El código del MVP fue escrito en GitHub. Aún no se ha ejecutado en un equipo local ni se ha probado con un token real de Telegram; por tanto, no declarar el bot operativo en producción.

### Pendientes inmediatos
1. Instalar dependencias localmente con pip install -r requirements.txt.
2. Crear el bot con @BotFather y guardar el token en .env local.
3. Ejecutar python run_telegram_bot.py.
4. Probar /start, /help y /status desde Telegram.
5. Incorporar pruebas automatizadas.
6. Construir la interfaz Streamlit para administrar y monitorear bots.
7. Diseñar persistencia multiempresa y almacenamiento seguro de credenciales en Supabase.

### Regla permanente
Actualizar memoria.md cuando cambien decisiones o requisitos. Agregar entradas fechadas a bitacora_acumulada.md sin borrar entradas anteriores.
