"""Handlers de comandos para el primer bot de Telegram."""

from telegram import Update
from telegram.ext import ContextTypes


async def start_command(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Da la bienvenida e informa las capacidades iniciales."""
    if update.effective_message:
        await update.effective_message.reply_text(
            "¡Hola! Soy un bot creado con BOT FACTORY AI.\n\n"
            "Comandos disponibles:\n"
            "/start - Iniciar el bot\n"
            "/help - Ver la ayuda\n"
            "/status - Consultar el estado"
        )


async def help_command(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Muestra la ayuda del bot."""
    if update.effective_message:
        await update.effective_message.reply_text(
            "Puedo responder comandos básicos. "
            "Próximamente podrás configurar automatizaciones desde el panel."
        )


async def status_command(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Confirma que el proceso del bot está atendiendo comandos."""
    if update.effective_message:
        await update.effective_message.reply_text(
            "Estado: operativo.\nPlataforma: BOT FACTORY AI."
        )
