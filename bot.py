"""Small, runnable Telegram bot example using python-telegram-bot 22.x."""

from __future__ import annotations

import asyncio
import logging
import os
import re
import sqlite3
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlparse

from dotenv import load_dotenv
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

NAME, AGE = range(2)
WEBHOOK_PATH_PATTERN = re.compile(r"^[A-Za-z0-9_-]{1,64}$")
WEBHOOK_SECRET_PATTERN = re.compile(r"^[A-Za-z0-9_-]{1,256}$")


@dataclass(frozen=True)
class Settings:
    token: str
    mode: str = "polling"
    db_path: str = "bot.db"
    webhook_listen: str = "0.0.0.0"
    webhook_port: int = 8443
    webhook_path: str = "telegram"
    webhook_url: str | None = None
    webhook_secret: str | None = None

    @classmethod
    def from_env(cls) -> "Settings":
        """Load and validate runtime settings from environment variables."""
        load_dotenv()
        token = os.getenv("BOT_TOKEN", "").strip()
        if not token:
            raise ValueError("BOT_TOKEN tidak ditemukan. Isi file .env terlebih dahulu.")

        mode = os.getenv("BOT_MODE", "polling").strip().lower()
        if mode not in {"polling", "webhook"}:
            raise ValueError("BOT_MODE harus bernilai 'polling' atau 'webhook'.")

        try:
            port = int(os.getenv("WEBHOOK_PORT", "8443"))
        except ValueError as exc:
            raise ValueError("WEBHOOK_PORT harus berupa angka.") from exc
        if not 1 <= port <= 65535:
            raise ValueError("WEBHOOK_PORT harus berada di antara 1 dan 65535.")

        path = os.getenv("WEBHOOK_PATH", "telegram").strip("/")
        if not WEBHOOK_PATH_PATTERN.fullmatch(path):
            raise ValueError("WEBHOOK_PATH hanya boleh berisi huruf, angka, '_' atau '-'.")

        webhook_url = os.getenv("WEBHOOK_URL", "").strip() or None
        webhook_secret = os.getenv("WEBHOOK_SECRET", "").strip() or None
        if mode == "webhook":
            if not webhook_url:
                raise ValueError("WEBHOOK_URL wajib diisi saat BOT_MODE=webhook.")
            parsed_url = urlparse(webhook_url)
            if parsed_url.scheme != "https" or not parsed_url.netloc:
                raise ValueError("WEBHOOK_URL harus berupa URL publik HTTPS yang valid.")
            if parsed_url.path.rstrip("/") != f"/{path}":
                raise ValueError("Path WEBHOOK_URL harus sama dengan /WEBHOOK_PATH.")
            if parsed_url.query or parsed_url.fragment:
                raise ValueError("WEBHOOK_URL tidak boleh memiliki query atau fragment.")
            if not webhook_secret or not WEBHOOK_SECRET_PATTERN.fullmatch(webhook_secret):
                raise ValueError(
                    "WEBHOOK_SECRET wajib diisi (1-256 karakter: huruf, angka, '_' atau '-')."
                )

        return cls(
            token=token,
            mode=mode,
            db_path=os.getenv("BOT_DB_PATH", "bot.db").strip() or "bot.db",
            webhook_listen=os.getenv("WEBHOOK_LISTEN", "0.0.0.0").strip() or "0.0.0.0",
            webhook_port=port,
            webhook_path=path,
            webhook_url=webhook_url,
            webhook_secret=webhook_secret,
        )


def initialize_database(db_path: str) -> None:
    """Create the small tutorial database and its users table."""
    path = Path(db_path)
    if path.parent != Path("."):
        path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(path, timeout=10) as connection:
        connection.execute("PRAGMA journal_mode=WAL")
        connection.execute(
            """CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT NOT NULL,
                registered_name TEXT,
                age INTEGER,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP
            )"""
        )
        # Migrate the two-column database from the original README example.
        columns = {row[1] for row in connection.execute("PRAGMA table_info(users)")}
        for name, declaration in (
            ("registered_name", "TEXT"),
            ("age", "INTEGER"),
            ("updated_at", "TEXT"),
        ):
            if name not in columns:
                connection.execute(f"ALTER TABLE users ADD COLUMN {name} {declaration}")
        connection.execute(
            "UPDATE users SET updated_at = CURRENT_TIMESTAMP WHERE updated_at IS NULL"
        )


def save_user(db_path: str, user_id: int, username: str | None, first_name: str) -> None:
    """Insert a user or refresh their profile without erasing registration data."""
    with sqlite3.connect(db_path, timeout=10) as connection:
        connection.execute(
            """INSERT INTO users (user_id, username, first_name)
               VALUES (?, ?, ?)
               ON CONFLICT(user_id) DO UPDATE SET
                   username = excluded.username,
                   first_name = excluded.first_name,
                   updated_at = CURRENT_TIMESTAMP""",
            (user_id, username, first_name),
        )


def save_registration(
    db_path: str,
    user_id: int,
    username: str | None,
    first_name: str,
    name: str,
    age: int,
) -> None:
    """Persist registration data for an existing or newly encountered user."""
    with sqlite3.connect(db_path, timeout=10) as connection:
        connection.execute(
            """INSERT INTO users
                   (user_id, username, first_name, registered_name, age)
               VALUES (?, ?, ?, ?, ?)
               ON CONFLICT(user_id) DO UPDATE SET
                   username = excluded.username,
                   first_name = excluded.first_name,
                   registered_name = excluded.registered_name,
                   age = excluded.age,
                   updated_at = CURRENT_TIMESTAMP""",
            (user_id, username, first_name, name, age),
        )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    message = update.effective_message
    if user is None or message is None:
        return
    settings: Settings = context.application.bot_data["settings"]
    await asyncio.to_thread(
        save_user, settings.db_path, user.id, user.username, user.first_name or ""
    )
    keyboard = [[InlineKeyboardButton("ℹ️ Info", callback_data="info")]]
    await message.reply_text(
        f"Halo {user.first_name or 'teman'}! 👋\nKetik /help untuk melihat bantuan.",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.effective_message
    if message is not None:
        await message.reply_text(
            "Perintah yang tersedia:\n"
            "/start - Mulai bot\n"
            "/help - Bantuan\n"
            "/register - Daftar nama dan umur\n"
            "/cancel - Batalkan pendaftaran\n\n"
            "Kirim pesan teks untuk saya ulangi."
        )


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.effective_message
    if message is not None and message.text is not None:
        await message.reply_text(f"Echo: {message.text}")


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    if query is None:
        return
    await query.answer()
    if query.data == "info":
        await query.edit_message_text(
            "ℹ️ Bot contoh dari panduan python-telegram-bot."
        )


async def register(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    message = update.effective_message
    if message is not None:
        await message.reply_text("Siapa namamu? (maksimal 100 karakter)")
    return NAME


async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    message = update.effective_message
    if message is None or message.text is None:
        return NAME
    name = message.text.strip()
    if not name or len(name) > 100:
        await message.reply_text("Nama harus berisi 1–100 karakter. Coba lagi:")
        return NAME
    context.user_data["registration_name"] = name
    await message.reply_text("Berapa umurmu? (0–130)")
    return AGE


async def get_age(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    message = update.effective_message
    if message is None or message.text is None:
        return AGE
    text = message.text.strip()
    if not text.isdecimal() or not 0 <= int(text) <= 130:
        await message.reply_text("Umur harus berupa angka antara 0 dan 130. Coba lagi:")
        return AGE

    user = update.effective_user
    settings: Settings = context.application.bot_data["settings"]
    name = context.user_data.pop("registration_name", "")
    if user is not None and name:
        await asyncio.to_thread(
            save_registration,
            settings.db_path,
            user.id,
            user.username,
            user.first_name or "",
            name,
            int(text),
        )
    await message.reply_text(f"Terima kasih! Nama: {name}, umur: {text}.")
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data.pop("registration_name", None)
    message = update.effective_message
    if message is not None:
        await message.reply_text("Pendaftaran dibatalkan.")
    return ConversationHandler.END


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log unexpected errors without recording message contents or secrets."""
    del update  # Update objects may contain private chat content and user data.
    logger = logging.getLogger(__name__)
    error = context.error
    if error is not None:
        logger.error(
            "Terjadi error saat memproses update Telegram.",
            exc_info=(type(error), error, error.__traceback__),
        )
    else:
        logger.error("Terjadi error saat memproses update Telegram tanpa detail exception.")


def build_application(settings: Settings) -> Application:
    application = Application.builder().token(settings.token).build()
    application.bot_data["settings"] = settings
    private_command = filters.ChatType.PRIVATE
    private_text = filters.ChatType.PRIVATE & filters.TEXT & ~filters.COMMAND

    conversation = ConversationHandler(
        entry_points=[CommandHandler("register", register, filters=private_command)],
        states={
            NAME: [MessageHandler(private_text, get_name)],
            AGE: [MessageHandler(private_text, get_age)],
        },
        fallbacks=[CommandHandler("cancel", cancel, filters=private_command)],
        # ConversationHandler expects updates to be processed sequentially.
        allow_reentry=False,
    )
    application.add_handler(CommandHandler("start", start, filters=private_command))
    application.add_handler(CommandHandler("help", help_command, filters=private_command))
    application.add_handler(CallbackQueryHandler(button_callback, pattern=r"^info$"))
    application.add_handler(conversation)
    # Also respond to /cancel when no conversation is currently active.
    application.add_handler(CommandHandler("cancel", cancel, filters=private_command))
    application.add_handler(MessageHandler(private_text, echo))
    application.add_error_handler(error_handler)
    return application


def main() -> None:
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO,
    )
    settings = Settings.from_env()
    initialize_database(settings.db_path)
    application = build_application(settings)
    logging.getLogger(__name__).info("Bot mulai berjalan dalam mode %s", settings.mode)

    if settings.mode == "webhook":
        application.run_webhook(
            listen=settings.webhook_listen,
            port=settings.webhook_port,
            url_path=settings.webhook_path,
            webhook_url=settings.webhook_url,
            secret_token=settings.webhook_secret,
            allowed_updates=Update.ALL_TYPES,
        )
    else:
        application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
