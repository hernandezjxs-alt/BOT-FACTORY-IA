"""Construcción y ejecución del bot Telegram."""

import logging

from telegram.ext import Application, CommandHandler

from bot_factory.connectors.telegram.handlers import (
    help_command,
    start_command,
    status_command,
)

logger = logging.getLogger(__name__)


def build_application(token: str) -> Application:
    """Construye la aplicación Telegram sin iniciar el polling."""
    if not token or not token.strip():
        raise ValueError("Falta TELEGRAM_BOT_TOKEN en el entorno.")

    application = Application.builder().token(token.strip()).build()
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("status", status_command))
    return application


async def run_bot(token: str) -> None:
    """Inicia el bot usando long polling hasta su detención."""
    application = build_application(token)
    logger.info("Iniciando Telegram Bot Factory...")
    await application.initialize()
    await application.start()
    if application.updater is None:
        raise RuntimeError("No se pudo inicializar el updater de Telegram.")
    await application.updater.start_polling(drop_pending_updates=True)
    logger.info("Telegram Bot Factory está operativo.")
    try:
        import asyncio

        await asyncio.Event().wait()
    finally:
        await application.updater.stop()
        await application.stop()
        await application.shutdown()
        logger.info("Telegram Bot Factory detenido.")
