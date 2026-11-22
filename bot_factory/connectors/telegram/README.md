# Telegram Bot Factory — MVP 0.1

## Funcionalidades iniciales
- `/start`: bienvenida e instrucciones.
- `/help`: ayuda básica.
- `/status`: confirma que el bot está atendiendo comandos.
- Worker Python independiente del panel Streamlit.

## Crear el bot en Telegram
1. Abre Telegram y busca el usuario oficial `@BotFather`.
2. Envía `/newbot` y sigue las instrucciones.
3. Copia el token entregado y mantenlo privado.
4. En tu entorno local, copia `.env.example` a `.env` y asigna el valor a `TELEGRAM_BOT_TOKEN`.

## Instalar y ejecutar
```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
python run_telegram_bot.py
```

No compartas el token en chats, capturas ni repositorios. Si se expone, revócalo desde BotFather y genera uno nuevo.

## Próximas mejoras
- Registro de bots y clientes en Supabase.
- Gestión segura de tokens por cliente.
- Panel Streamlit para alta, configuración y monitoreo.
- Webhooks, métricas, límites y auditoría.
- Pruebas automatizadas y despliegue del worker.
