<div align="center">

# 🤖 Panduan Lengkap Membuat Bot Telegram dengan Python

Panduan step-by-step membuat bot Telegram menggunakan **python-telegram-bot**,
dari nol sampai siap dideploy ke server.

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![python-telegram-bot](https://img.shields.io/badge/python--telegram--bot-22.x-26A5E4?logo=telegram&logoColor=white)
![Status](https://img.shields.io/badge/status-tutorial-success)

</div>

---

## 📑 Daftar Isi

- [✨ Pendahuluan](#-pendahuluan)
- [✅ Prasyarat](#-prasyarat)
- [🧩 Membuat Bot di Telegram](#-membuat-bot-di-telegram)
- [🔧 Menyiapkan Lingkungan Pengembangan](#-menyiapkan-lingkungan-pengembangan)
- [🚀 Membuat Bot Sederhana](#-membuat-bot-sederhana)
- [⚡ Fitur Lanjutan](#-fitur-lanjutan)
- [📦 Contoh Kode Lengkap](#-contoh-kode-lengkap)
- [🌍 Deployment](#-deployment)
- [🔐 Keamanan & Best Practices](#-keamanan--best-practices)
- [🩺 Troubleshooting](#-troubleshooting)
- [📚 Referensi](#-referensi)

---

## ✨ Pendahuluan

**Bot Telegram** adalah akun yang dijalankan oleh program, bukan manusia. Bot berinteraksi dengan pengguna melalui **Telegram Bot API**.

| Keuntungan | Contoh penggunaan |
|---|---|
| ⚙️ **Otomatisasi** | Menjawab pertanyaan berulang, mengirim pengingat |
| 🔗 **Integrasi** | Terhubung ke database, API, atau layanan eksternal |
| 📈 **Skalabel** | Melayani banyak pengguna secara bersamaan |
| 🎨 **Fleksibel** | Mendukung teks, gambar, video, tombol, dan lainnya |

---

## ✅ Prasyarat

Pastikan kamu sudah memiliki:

- [ ] Akun Telegram aktif
- [ ] **Python 3.10+** (cek dengan `python --version`)
- [ ] `pip` (biasanya sudah terpasang bersama Python)
- [ ] Editor kode, misalnya VS Code atau PyCharm
- [ ] Koneksi internet yang stabil
- [ ] Git *(opsional, untuk version control)*

---

## 🧩 Membuat Bot di Telegram

Token API adalah **kunci akses** bot kamu. Siapa pun yang memilikinya bisa mengendalikan bot.

### 1️⃣ Buka BotFather

1. Cari **@BotFather** di Telegram (pastikan ada centang biru ✔️).
2. Kirim perintah `/start`.

### 2️⃣ Buat bot baru

1. Kirim `/newbot`.
2. Masukkan **nama** bot, misalnya `My Awesome Bot`.
3. Masukkan **username** bot, dengan aturan:
   - Harus diakhiri `bot`, misalnya `myawesome_bot`
   - Hanya huruf, angka, dan underscore (`_`)
   - Harus unik secara global
4. BotFather akan memberikan token seperti ini:

   ```text
   1234567890:ABCdefGHIJklmNOpqrsTUVwxyz-1234567890
   ```

> [!WARNING]
> Jangan bagikan token ini ke siapa pun dan jangan menuliskannya langsung di dalam kode.
> Jika token bocor, kirim `/revoke` ke BotFather untuk membuat token baru.

### 3️⃣ Konfigurasi bot *(opsional, tapi disarankan)*

| Perintah BotFather | Fungsi |
|---|---|
| `/setdescription` | Deskripsi bot yang tampil di profil |
| `/setabouttext` | Teks "About" |
| `/setuserpic` | Foto profil bot |
| `/setcommands` | Daftar perintah yang muncul di menu bot |
| `/setinline` | Mengaktifkan mode inline |

Contoh isi untuk `/setcommands` (satu perintah per baris):

```text
start - Mulai bot
help - Bantuan
register - Daftar nama dan umur
```

---

## 🔧 Menyiapkan Lingkungan Pengembangan

Kita akan menggunakan **python-telegram-bot versi 22.x** yang bersifat *asynchronous* dan berbasis `Application`.

### 1️⃣ Buat folder proyek

```bash
mkdir telegram-bot-tutorial
cd telegram-bot-tutorial
```

### 2️⃣ Buat virtual environment

Virtual environment mengisolasi dependensi proyek dari sistem.

```bash
python -m venv venv
```

Aktifkan:

<table>
<tr>
<th>🪟 Windows</th>
<th>🐧 Linux / 🍎 macOS</th>
</tr>
<tr>
<td>

```bash
venv\Scripts\activate
```

</td>
<td>

```bash
source venv/bin/activate
```

</td>
</tr>
</table>

Jika berhasil, prompt terminal akan menampilkan `(venv)`.

### 3️⃣ Instal dependensi

```bash
pip install "python-telegram-bot==22.8" "python-dotenv==1.2.4"
```

Atau buat file `requirements.txt` lalu jalankan `pip install -r requirements.txt`:

```text
python-telegram-bot==22.8
python-dotenv==1.2.4
```

> [!NOTE]
> Versi di atas dikunci agar contoh kode di panduan ini sudah diuji dan berjalan.
> Jika ingin versi lain, cek [dokumentasi python-telegram-bot](https://docs.python-telegram-bot.org/) karena ada perubahan API antar versi mayor.
> Versi 20.x tidak disarankan untuk Python 3.13 (lihat [Troubleshooting](#-troubleshooting)).

### 4️⃣ Struktur proyek

```text
telegram-bot-tutorial/
├── venv/              # Virtual environment (jangan di-commit)
├── .env               # Token rahasia (jangan di-commit)
├── .env.example       # Contoh isi .env (aman di-commit)
├── .gitignore         # Daftar file yang diabaikan Git
├── .dockerignore      # Daftar file yang tidak dimasukkan ke Docker image
├── Dockerfile         # Resep untuk membuat Docker image
├── requirements.txt   # Daftar dependensi
├── bot.py             # File utama bot
├── bot.db             # Database SQLite (dibuat otomatis)
└── README.md          # Dokumentasi
```

Buat file `.gitignore`:

```gitignore
venv/
.venv/
__pycache__/
*.pyc
.env
bot.db
```

---

## 🚀 Membuat Bot Sederhana

Bot pertama ini akan merespons `/start`, `/help`, dan mengulang (*echo*) pesan teks apa pun.

### 1️⃣ Simpan token di file `.env`

```env
BOT_TOKEN=1234567890:ABCdefGHIJklmNOpqrsTUVwxyz-1234567890
```

Sebagai referensi untuk tim, buat juga `.env.example` tanpa token asli:

```env
BOT_TOKEN=isi_token_dari_botfather
```

### 2️⃣ Kode dasar `bot.py`

```python
import logging
import os

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

# Muat variabel dari file .env
load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise ValueError("BOT_TOKEN tidak ditemukan. Pastikan file .env berisi BOT_TOKEN.")

# Aktifkan logging untuk memantau aktivitas dan error
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Kirim sambutan saat pengguna mengetik /start."""
    user = update.effective_user
    await update.message.reply_text(
        f"Halo {user.first_name}! 👋\n"
        "Saya adalah bot sederhana.\n"
        "Ketik /help untuk melihat bantuan."
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Kirim daftar perintah."""
    await update.message.reply_text(
        "Perintah yang tersedia:\n"
        "/start - Mulai bot\n"
        "/help - Bantuan\n\n"
        "Kirim pesan apa saja untuk saya ulangi."
    )


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Balas pesan teks dengan isi yang sama."""
    await update.message.reply_text(f"Echo: {update.message.text}")


def main() -> None:
    """Jalankan bot."""
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    # Pesan teks yang bukan perintah
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    logger.info("Bot mulai berjalan...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
```

### 3️⃣ Jalankan bot

```bash
python bot.py
```

Jika berhasil, terminal menampilkan log `Bot mulai berjalan...`. Buka Telegram, cari username bot kamu, lalu kirim `/start`.

### 📖 Penjelasan singkat

| Bagian | Fungsi |
|---|---|
| `load_dotenv()` | Membaca file `.env` ke environment |
| `Application.builder()` | Membuat instance aplikasi bot |
| `CommandHandler` | Menangani perintah seperti `/start` |
| `MessageHandler` | Menangani pesan biasa (`filters.TEXT & ~filters.COMMAND`) |
| `run_polling()` | Bot terus meminta update baru dari server Telegram |

---

## ⚡ Fitur Lanjutan

### 1️⃣ Reply Keyboard

Reply keyboard menampilkan tombol di area keyboard utama (menggantikan keyboard HP).

```python
from telegram import KeyboardButton, ReplyKeyboardMarkup

async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [KeyboardButton("Info"), KeyboardButton("Kontak")],
        [KeyboardButton("Bantuan")],
    ]
    await update.message.reply_text(
        "Pilih menu:",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True),
    )
```

Tangkap teks tombol dengan regex:

```python
application.add_handler(MessageHandler(filters.Regex("^Info$"), info_handler))
```

### 2️⃣ Inline Keyboard & Callback Query

Inline keyboard menampilkan tombol **di dalam pesan**.

```python
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackQueryHandler

async def start_with_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("✅ Klik saya", callback_data="button_clicked")],
        [InlineKeyboardButton("🌐 Buka website", url="https://example.com")],
    ]
    await update.message.reply_text(
        "Pilih aksi:",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()  # Wajib: memberi tahu Telegram bahwa klik sudah diterima
    if query.data == "button_clicked":
        await query.edit_message_text("Tombol sudah diklik! 🎉")

# Daftarkan handler
application.add_handler(CallbackQueryHandler(button_callback))
```

> [!TIP]
> Batas `callback_data` adalah 64 byte. Simpan data besar di database atau `context.user_data`, lalu kirim ID-nya saja.

### 3️⃣ ConversationHandler (alur multi-langkah)

`ConversationHandler` dipakai untuk percakapan bertahap, misalnya pendaftaran.

```python
from telegram.ext import ConversationHandler

NAME, AGE = range(2)

async def register(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Siapa namamu?")
    return NAME

async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["name"] = update.message.text
    await update.message.reply_text("Berapa umurmu?")
    return AGE

async def get_age(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text.strip()
    if not text.isdigit():
        await update.message.reply_text("Umur harus berupa angka. Coba lagi:")
        return AGE  # Tetap di state AGE
    name = context.user_data.pop("name", "-")
    await update.message.reply_text(f"Terima kasih! Nama: {name}, umur: {text}.")
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data.clear()
    await update.message.reply_text("Pendaftaran dibatalkan.")
    return ConversationHandler.END

conv_handler = ConversationHandler(
    entry_points=[CommandHandler("register", register)],
    states={
        NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
        AGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_age)],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)
application.add_handler(conv_handler)
```

### 4️⃣ Menyimpan data ke SQLite

SQLite adalah database ringan yang tersimpan dalam satu file dan tidak memerlukan server.

```python
import sqlite3

db = sqlite3.connect("bot.db")
db.execute(
    "CREATE TABLE IF NOT EXISTS users ("
    "user_id INTEGER PRIMARY KEY, username TEXT, first_name TEXT)"
)
db.commit()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    db.execute(
        "INSERT OR IGNORE INTO users (user_id, username, first_name) VALUES (?, ?, ?)",
        (user.id, user.username, user.first_name),
    )
    db.commit()
    await update.message.reply_text("Data kamu tersimpan! ✅")
```

> [!NOTE]
> Gunakan parameter `?` seperti contoh di atas. **Jangan** menyusun query dengan f-string, karena rawan SQL injection.
> Untuk bot yang lebih besar, pertimbangkan SQLAlchemy atau database server seperti PostgreSQL.

### 5️⃣ Webhook *(untuk produksi)*

**Polling** cocok untuk pengembangan. Untuk produksi, **webhook** lebih responsif dan hemat resource, karena Telegram yang mengirim update ke server kamu.

Pada python-telegram-bot v20+, webhook bisa dijalankan langsung tanpa Flask:

```python
import os

application.run_webhook(
    listen="0.0.0.0",              # Dengarkan semua interface
    port=8443,
    url_path="telegram",           # Path lokal untuk menerima update
    webhook_url="https://yourdomain.com/telegram",  # URL publik HTTPS kamu
    secret_token=os.getenv("WEBHOOK_SECRET"),       # Verifikasi bahwa request berasal dari Telegram
    allowed_updates=Update.ALL_TYPES,
)
```

> [!IMPORTANT]
> - Webhook **wajib HTTPS** dengan sertifikat yang valid.
> - Simpan `WEBHOOK_SECRET` di `.env` dengan nilai acak yang panjang.
> - Jika memakai polling dan webhook bersamaan, Telegram hanya akan mengirim update ke salah satunya.

---

## 📦 Contoh Kode Lengkap

Berikut `bot.py` yang menggabungkan semua fitur di atas dalam satu file yang konsisten. Simpan sebagai `bot.py`, lalu jalankan dengan `python bot.py`.

<details>
<summary><b>📄 Klik untuk melihat <code>bot.py</code> lengkap</b></summary>

```python
import logging
import os
import sqlite3

from dotenv import load_dotenv
from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Update,
)
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

# ---------- Konfigurasi ----------
load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise ValueError("BOT_TOKEN tidak ditemukan. Isi file .env terlebih dahulu.")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# ---------- Database ----------
db = sqlite3.connect("bot.db")
db.execute(
    "CREATE TABLE IF NOT EXISTS users ("
    "user_id INTEGER PRIMARY KEY, username TEXT, first_name TEXT)"
)
db.commit()

# ---------- State percakapan ----------
NAME, AGE = range(2)


# ---------- Handler perintah ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Simpan user ke database lalu tampilkan tombol."""
    user = update.effective_user
    db.execute(
        "INSERT OR IGNORE INTO users (user_id, username, first_name) VALUES (?, ?, ?)",
        (user.id, user.username, user.first_name),
    )
    db.commit()

    keyboard = [
        [InlineKeyboardButton("ℹ️ Info", callback_data="info")],
        [InlineKeyboardButton("🌐 Website", url="https://example.com")],
    ]
    await update.message.reply_text(
        f"Halo {user.first_name}! 👋\nPilih aksi di bawah ini:",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Tampilkan daftar perintah."""
    await update.message.reply_text(
        "Perintah yang tersedia:\n"
        "/start - Mulai bot\n"
        "/help - Bantuan\n"
        "/register - Daftar nama dan umur\n"
        "/cancel - Batalkan pendaftaran\n\n"
        "Kirim pesan apa saja untuk saya ulangi."
    )


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Balas pesan teks dengan isi yang sama."""
    await update.message.reply_text(f"Echo: {update.message.text}")


# ---------- Callback tombol ----------
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    if query.data == "info":
        await query.edit_message_text("ℹ️ Ini adalah bot contoh dari panduan python-telegram-bot.")


# ---------- ConversationHandler: /register ----------
async def register(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Siapa namamu?")
    return NAME


async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["name"] = update.message.text
    await update.message.reply_text("Berapa umurmu?")
    return AGE


async def get_age(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text.strip()
    if not text.isdigit():
        await update.message.reply_text("Umur harus berupa angka. Coba lagi:")
        return AGE
    name = context.user_data.pop("name", "-")
    await update.message.reply_text(f"Terima kasih! Nama: {name}, umur: {text}.")
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data.clear()
    await update.message.reply_text("Pendaftaran dibatalkan.")
    return ConversationHandler.END


# ---------- Fungsi utama ----------
def main() -> None:
    application = Application.builder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("register", register)],
        states={
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
            AGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_age)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CallbackQueryHandler(button_callback))
    application.add_handler(conv_handler)  # Harus sebelum echo
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    logger.info("Bot mulai berjalan...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
```

</details>

---

## 🌍 Deployment

Setelah bot selesai, jalankan di server agar aktif 24/7.

### 1️⃣ VPS (DigitalOcean, Linode, AWS EC2, dll.)

1. Siapkan server Linux (Ubuntu 22.04 LTS direkomendasikan).
2. Masuk via SSH, lalu pasang Python, pip, dan venv:

   ```bash
   sudo apt update && sudo apt install -y python3 python3-venv python3-pip git
   ```

3. Clone repository atau upload file proyek.
4. Buat virtual environment dan instal dependensi.
5. Buat file `.env` **langsung di server** (jangan dari Git).

### 2️⃣ Menjalankan sebagai service dengan systemd

Buat file `/etc/systemd/system/telegram-bot.service`:

```ini
[Unit]
Description=Telegram Bot
After=network.target

[Service]
User=youruser
WorkingDirectory=/home/youruser/telegram-bot-tutorial
ExecStart=/home/youruser/telegram-bot-tutorial/venv/bin/python bot.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

Aktifkan dan jalankan:

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now telegram-bot
sudo systemctl status telegram-bot      # Cek status
sudo journalctl -u telegram-bot -f      # Lihat log secara live
```

### 3️⃣ Platform cloud

| Platform | Cara singkat | Catatan |
|---|---|---|
| **Railway** | Hubungkan repo GitHub, isi variabel `BOT_TOKEN`, deploy | Cek paket gratis/kredit terbaru |
| **Render** | Buat *Background Worker*, start command `python bot.py` | Worker biasanya berbayar |
| **Fly.io** | Deploy dengan `flyctl`, gunakan Dockerfile | Cocok untuk Docker |
| **PythonAnywhere** | Upload file, buat virtualenv, jalankan di tab *Tasks* | Pastikan task selalu aktif |

> [!CAUTION]
> **Heroku tidak lagi menyediakan paket gratis** (sejak November 2022). Jika memakai Heroku, siapkan paket berbayar, atau pilih platform lain di tabel ini.

### 4️⃣ Docker

Buat `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "bot.py"]
```

Buat `.dockerignore` agar `.env` dan `venv/` tidak ikut masuk ke image:

```dockerignore
venv/
.venv/
__pycache__/
*.pyc
.env
.git/
bot.db
```

Build dan jalankan:

```bash
docker build -t telegram-bot .
docker run -d --name telegram-bot --restart unless-stopped --env-file .env telegram-bot
docker logs -f telegram-bot
```

---

## 🔐 Keamanan & Best Practices

- 🔑 **Jangan commit token.** Simpan di `.env` dan pastikan `.env` ada di `.gitignore`.
- 🔁 **Revoke token jika bocor** lewat `/revoke` di BotFather.
- 🔒 **Gunakan HTTPS** untuk webhook, dan aktifkan `secret_token`.
- ✅ **Validasi input** pengguna, misalnya cek tipe dan panjang teks.
- 🛡️ **Batasi akses** dengan whitelist user ID jika bot bersifat pribadi:

  ```python
  ADMIN_IDS = {123456789}  # Ganti dengan Telegram user ID kamu

  async def admin_only(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
      if update.effective_user.id not in ADMIN_IDS:
          await update.message.reply_text("Maaf, perintah ini hanya untuk admin.")
          return
      await update.message.reply_text("Selamat datang, admin!")
  ```

- ⏱️ **Terapkan rate limiting** untuk mencegah spam.
- 📝 **Gunakan logging** yang baik untuk debugging dan monitoring.
- 🧱 **Pisahkan konfigurasi dari kode**, dan gunakan type hints.

---

## 🩺 Troubleshooting

<details>
<summary><b>Bot tidak merespons</b></summary>

- Pastikan token benar dan bot belum dihapus.
- Cek log di terminal atau `journalctl` untuk melihat error.
- Pastikan koneksi internet server stabil.
- Jika memakai webhook, pastikan URL publik bisa diakses dan sertifikat HTTPS valid.

</details>

<details>
<summary><b><code>Conflict: terminated by other getUpdates request</code></b></summary>

Hanya satu instance bot yang boleh polling pada satu waktu. Hentikan instance lain (misalnya bot yang masih jalan di laptop atau container lama), atau gunakan webhook.

</details>

<details>
<summary><b><code>AttributeError: 'Updater' object has no attribute '_Updater__polling_cleanup_cb'</code></b></summary>

Terjadi jika memakai python-telegram-bot 20.x di Python 3.13. Solusinya, pakai versi yang lebih baru:

```bash
pip install --upgrade "python-telegram-bot==22.8"
```

</details>

<details>
<summary><b>Pesan tidak terkirim</b></summary>

- Pastikan pengguna sudah menekan **Start** di chat bot.
- Perhatikan batas rate limit Telegram. Jika terlalu sering, Telegram akan membatasi sementara.

</details>

<details>
<summary><b><code>telegram.error.Unauthorized</code></b></summary>

Token salah atau sudah di-revoke. Buat token baru lewat BotFather, lalu perbarui `.env`.

</details>

<details>
<summary><b><code>ValueError: BOT_TOKEN tidak ditemukan</code></b></summary>

- Pastikan file `.env` berada di folder yang sama dengan `bot.py` (atau folder kerja saat menjalankan perintah).
- Pastikan isinya `BOT_TOKEN=...` tanpa spasi di sekitar tanda `=`.

</details>

---

## 📚 Referensi

- 📖 [Dokumentasi python-telegram-bot](https://docs.python-telegram-bot.org/)
- 🧪 [Contoh-contoh bot python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot/tree/master/examples)
- 📘 [Dokumentasi Telegram Bot API](https://core.telegram.org/bots/api)
- 🤖 [BotFather](https://t.me/BotFather)

---

<div align="center">

Selamat mencoba dan jangan ragu bereksperimen! 🚀

⭐ Jika panduan ini membantu, beri bintang pada repository ini.

</div>
