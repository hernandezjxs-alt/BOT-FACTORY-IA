"""Worker independiente para ejecutar el bot de Telegram."""

import asyncio
import logging
import os

from dotenv import load_dotenv

from bot_factory.connectors.telegram.bot import run_bot


def main() -> None:
    load_dotenv()
    logging.basicConfig(
        level=os.getenv("LOG_LEVEL", "INFO").upper(),
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )
    token = os.getenv("TELEGRAM_BOT_TOKEN", "")
    if not token:
        raise SystemExit(
            "Configura TELEGRAM_BOT_TOKEN en tu archivo .env antes de iniciar."
        )
    asyncio.run(run_bot(token))


if __name__ == "__main__":
    main()
