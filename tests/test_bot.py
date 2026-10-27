import os
import sqlite3
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from bot import Settings, initialize_database, save_registration, save_user


class SettingsTests(unittest.TestCase):
    def test_polling_defaults(self):
        with patch.dict(os.environ, {"BOT_TOKEN": "test-token"}, clear=True):
            settings = Settings.from_env()
        self.assertEqual(settings.mode, "polling")
        self.assertEqual(settings.db_path, "bot.db")

    def test_webhook_requires_https_url_and_secret(self):
        env = {
            "BOT_TOKEN": "test-token",
            "BOT_MODE": "webhook",
            "WEBHOOK_URL": "https://example.org/telegram",
            "WEBHOOK_SECRET": "random_secret-123",
        }
        with patch.dict(os.environ, env, clear=True):
            settings = Settings.from_env()
        self.assertEqual(settings.webhook_path, "telegram")
        self.assertEqual(settings.webhook_url, "https://example.org/telegram")

    def test_webhook_rejects_missing_secret(self):
        env = {
            "BOT_TOKEN": "test-token",
            "BOT_MODE": "webhook",
            "WEBHOOK_URL": "https://example.org/telegram",
        }
        with patch.dict(os.environ, env, clear=True):
            with self.assertRaisesRegex(ValueError, "WEBHOOK_SECRET"):
                Settings.from_env()

    def test_webhook_rejects_mismatched_path(self):
        env = {
            "BOT_TOKEN": "test-token",
            "BOT_MODE": "webhook",
            "WEBHOOK_URL": "https://example.org/wrong-path",
            "WEBHOOK_SECRET": "random_secret-123",
        }
        with patch.dict(os.environ, env, clear=True):
            with self.assertRaisesRegex(ValueError, "Path WEBHOOK_URL"):
                Settings.from_env()


class DatabaseTests(unittest.TestCase):
    def test_profiles_and_registration_are_upserted(self):
        with tempfile.TemporaryDirectory() as directory:
            db_path = str(Path(directory) / "nested" / "bot.db")
            initialize_database(db_path)
            save_user(db_path, 42, "first_name", "First")
            save_registration(db_path, 42, "new_username", "Updated", "Ada", 36)
            save_user(db_path, 42, "newer_username", "Ada Updated")

            with sqlite3.connect(db_path) as connection:
                row = connection.execute(
                    "SELECT username, first_name, registered_name, age "
                    "FROM users WHERE user_id = ?",
                    (42,),
                ).fetchone()
            self.assertEqual(row, ("newer_username", "Ada Updated", "Ada", 36))

    def test_migrates_original_two_column_table(self):
        with tempfile.TemporaryDirectory() as directory:
            db_path = str(Path(directory) / "bot.db")
            with sqlite3.connect(db_path) as connection:
                connection.execute(
                    "CREATE TABLE users (user_id INTEGER PRIMARY KEY, "
                    "username TEXT, first_name TEXT)"
                )
                connection.execute(
                    "INSERT INTO users VALUES (?, ?, ?)", (7, "old_name", "Old")
                )
            initialize_database(db_path)
            save_registration(db_path, 7, "old_name", "Old", "New Name", 20)
            with sqlite3.connect(db_path) as connection:
                row = connection.execute(
                    "SELECT registered_name, age FROM users WHERE user_id = 7"
                ).fetchone()
            self.assertEqual(row, ("New Name", 20))


if __name__ == "__main__":
    unittest.main()
