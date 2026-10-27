<div align="center">

# 🤖 Panduan Membuat Bot Telegram dengan Python

Panduan berbahasa Indonesia dan proyek contoh yang dapat dijalankan menggunakan **python-telegram-bot 22.x**. Berisi polling, percakapan bertahap, SQLite, webhook, pengujian, dan deployment Docker.

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![python-telegram-bot](https://img.shields.io/badge/python--telegram--bot-22.8-26A5E4?logo=telegram&logoColor=white)
![Tests](https://img.shields.io/badge/tests-unittest-success)

</div>

---

## 📑 Daftar Isi

- [Pendahuluan](#-pendahuluan)
- [Prasyarat](#-prasyarat)
- [Membuat bot di Telegram](#-membuat-bot-di-telegram)
- [Menjalankan proyek](#-menjalankan-proyek)
- [Isi dan struktur proyek](#-isi-dan-struktur-proyek)
- [Konfigurasi polling dan webhook](#-konfigurasi-polling-dan-webhook)
- [Database dan data pengguna](#-database-dan-data-pengguna)
- [Pengujian](#-pengujian)
- [Deployment](#-deployment)
- [Keamanan dan batasan](#-keamanan-dan-batasan)
- [Troubleshooting](#-troubleshooting)
- [Referensi](#-referensi)

---

## ✨ Pendahuluan

Bot Telegram adalah akun yang dijalankan oleh program dan berinteraksi melalui Telegram Bot API. Repository ini berisi kode kerja, bukan hanya potongan tutorial: `bot.py`, dependensi, konfigurasi contoh, Dockerfile, dan tes tersedia langsung.

Contoh bot ini bisa:

- merespons `/start`, `/help`, `/register`, dan `/cancel`;
- mengulang pesan teks di **chat pribadi**;
- menampilkan tombol inline;
- menyimpan profil dan hasil pendaftaran ke SQLite;
- berjalan dengan long polling atau webhook.

Bot ini adalah contoh edukasi, bukan template produksi lengkap. Sesuaikan validasi, kapasitas, monitoring, dan kebijakan data sebelum digunakan untuk layanan nyata.

## ✅ Prasyarat

- Python **3.10 atau lebih baru** dan `pip`.
- Akun Telegram aktif.
- Terminal dan editor kode.
- Docker Compose (opsional, untuk deployment container).

Python 3.10+ sesuai persyaratan python-telegram-bot 22.8 ([dokumentasi versi 22.8](https://docs.python-telegram-bot.org/en/v22.8/)).

## 🧩 Membuat bot di Telegram

1. Cari akun resmi **@BotFather** di Telegram dan kirim `/start`.
2. Kirim `/newbot`, lalu tentukan nama dan username bot. Username harus diakhiri `bot` dan unik.
3. Simpan token yang diberikan BotFather secara rahasia. Token memberi akses untuk mengendalikan bot.
4. Jika token pernah terungkap, cabut/ganti melalui BotFather.

Jangan menempelkan token asli ke README, kode, issue, log, atau Git. File `.env` diabaikan oleh Git.

## 🚀 Menjalankan proyek

Clone repository, lalu dari direktori repository:

```bash
python --version
python -m venv .venv
```

Aktifkan virtual environment:

```bash
# Linux / macOS
source .venv/bin/activate

# Windows PowerShell
.venv\Scripts\Activate.ps1
```

Pasang dependensi dan buat konfigurasi lokal:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Salin `.env.example` menjadi `.env`, kemudian isi `BOT_TOKEN` dengan token dari BotFather. Untuk Linux/macOS:

```bash
cp .env.example .env
```

Di Windows, salin berkas itu lewat File Explorer atau jalankan `Copy-Item .env.example .env` di PowerShell. Buka `.env`, ganti `BOT_TOKEN`, lalu jalankan:

```bash
python bot.py
```

Secara default bot berjalan dengan polling. Buka chat pribadi bot di Telegram dan kirim `/start`. Jangan jalankan dua proses polling dengan token yang sama sekaligus.

## 📁 Isi dan struktur proyek

```text
.
├── .env.example             # Template konfigurasi tanpa token sungguhan
├── .github/workflows/tests.yml # Tes otomatis pada push dan pull request
├── .gitignore               # Mengabaikan rahasia, database, dan artefak Python
├── .dockerignore            # Mengeluarkan rahasia dan file lokal dari image
├── Dockerfile               # Image Docker non-root
├── LICENSE                  # Lisensi MIT
├── README.md                # Panduan ini
├── bot.py                   # Implementasi bot yang dapat dijalankan
├── compose.yaml             # Docker Compose dengan volume data persisten
├── requirements.txt         # Versi dependensi yang dikunci
└── tests/
    └── test_bot.py          # Tes konfigurasi dan SQLite
```

`bot.db` dibuat otomatis saat bot dijalankan dan tidak dimasukkan ke Git. `.env.example` aman untuk disalin, tetapi nilainya bukan konfigurasi produksi.

### Variabel konfigurasi

| Variabel | Wajib | Default | Keterangan |
|---|---:|---|---|
| `BOT_TOKEN` | Ya | — | Token dari BotFather. |
| `BOT_MODE` | Tidak | `polling` | `polling` atau `webhook`. |
| `BOT_DB_PATH` | Tidak | `bot.db` | Lokasi file SQLite. Di Compose disetel ke `/data/bot.db`. |
| `WEBHOOK_LISTEN` | Tidak | `0.0.0.0` | Interface lokal untuk server webhook. |
| `WEBHOOK_PORT` | Tidak | `8443` | Port lokal yang didengarkan. |
| `WEBHOOK_PATH` | Tidak | `telegram` | Path webhook tanpa garis miring di awal/akhir. |
| `WEBHOOK_URL` | Webhook | — | URL publik HTTPS, termasuk path, misalnya `https://bot.example.com/telegram`. |
| `WEBHOOK_SECRET` | Webhook | — | Rahasia untuk memvalidasi header webhook Telegram. Gunakan nilai acak. |

Aplikasi menolak konfigurasi webhook tanpa URL HTTPS, path yang cocok, atau secret yang valid. Buat secret acak, misalnya dengan `python -c "import secrets; print(secrets.token_urlsafe(32))"`; karakter yang diterima dibatasi sesuai format Telegram.

## ⚙️ Konfigurasi polling dan webhook

### Polling (default)

Polling tidak memerlukan endpoint publik dan biasanya merupakan cara termudah untuk mulai. Pastikan hanya satu instance memakai token yang sama. Polling juga bisa digunakan di server produksi jika sesuai kebutuhan; webhook bukan persyaratan untuk produksi.

### Webhook

Pilih webhook bila deployment kamu mempunyai domain publik, TLS/HTTPS, dan reverse proxy atau konfigurasi sertifikat yang benar. Instal dependensi dari `requirements.txt`—file itu memasang ekstra `webhooks` yang menyediakan Tornado, dibutuhkan `run_webhook()` ([dokumentasi instalasi PTB](https://docs.python-telegram-bot.org/en/v22.8/)).

Atur `.env` untuk mode webhook, misalnya:

```env
BOT_MODE=webhook
WEBHOOK_LISTEN=0.0.0.0
WEBHOOK_PORT=8443
WEBHOOK_PATH=telegram
WEBHOOK_URL=https://bot.example.com/telegram
WEBHOOK_SECRET=isi_secret_acak_yang_aman
```

`WEBHOOK_URL` harus alamat publik yang dapat diakses Telegram melalui HTTPS. TLS dapat diakhiri di reverse proxy; teruskan request untuk `/telegram` ke port aplikasi yang dikonfigurasi. Compose memetakan `127.0.0.1:8443` untuk reverse proxy yang berjalan di host. Jika proxy berjalan di container terpisah, gunakan jaringan internal bersama dan atur port/routing sesuai kebutuhan—jangan mengekspos endpoint HTTP aplikasi langsung ke internet. Jangan jalankan polling dan webhook secara bersamaan untuk bot yang sama. Kode menggunakan `secret_token`; jangan menghapus validasi secret untuk endpoint publik.

## 💾 Database dan data pengguna

Bot menggunakan SQLite lokal tanpa server database. Operasi database dijalankan di thread terpisah agar operasi file tidak menahan event loop bot. Tabel menyimpan `user_id`, username, nama depan, nama pendaftaran, umur, serta waktu pembaruan. Saat profil berubah, data profil diperbarui tanpa menghapus data pendaftaran. Struktur tabel lama dari contoh awal juga dimigrasikan otomatis.

Di luar Docker, lokasi default adalah `bot.db` relatif ke direktori kerja. Pastikan direktori tersebut dapat ditulis dan buat cadangan bila data penting. Untuk beban besar, banyak instance, atau ketersediaan tinggi, gunakan database server dan strategi migrasi yang sesuai.

Di Docker Compose, data disimpan pada named volume `telegram-bot-data`, sehingga tetap tersedia saat container diperbarui atau dibuat ulang. Jangan menghapus volume jika ingin mempertahankan database.

## 🧪 Pengujian

Tes tidak memerlukan token Telegram atau koneksi ke Bot API:

```bash
python -m unittest discover -s tests -v
python -m compileall -q bot.py tests
```

Tes mencakup validasi mode webhook, upsert profil dan pendaftaran, serta migrasi database lama. Tes ini bukan pengujian integrasi dengan Telegram.

## 🌍 Deployment

### Docker Compose (disarankan untuk contoh ini)

Buat `.env` dan isi token terlebih dahulu, lalu:

```bash
docker compose up --build -d
docker compose logs -f telegram-bot
```

Hentikan container tanpa menghapus database:

```bash
docker compose down
```

Jangan menambahkan `-v` ke perintah `down` kecuali memang ingin menghapus volume dan seluruh data SQLite. File `.env` tidak disalin ke image; Compose memasukkannya saat runtime.

Untuk inspeksi manual terhadap volume, gunakan perintah Docker volume yang sesuai dengan lingkunganmu dan buat salinan database saat bot dihentikan atau setelah memastikan prosedur backup aman.

### VPS dengan systemd

Buat virtual environment, pasang dependensi, dan tempatkan repository serta `.env` di lokasi yang hanya dapat diakses akun service. Contoh unit:

```ini
[Unit]
Description=Telegram Bot
Wants=network-online.target
After=network-online.target

[Service]
Type=simple
User=telegrambot
WorkingDirectory=/opt/telegram-bot
EnvironmentFile=/opt/telegram-bot/.env
Environment=BOT_DB_PATH=/var/lib/telegram-bot/bot.db
ExecStart=/opt/telegram-bot/.venv/bin/python /opt/telegram-bot/bot.py
Restart=on-failure
RestartSec=5
NoNewPrivileges=true
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=/var/lib/telegram-bot

[Install]
WantedBy=multi-user.target
```

Pastikan direktori data dimiliki akun `telegrambot`, lalu muat dan aktifkan service:

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now telegram-bot
sudo systemctl status telegram-bot
sudo journalctl -u telegram-bot -f
```

`EnvironmentFile` di atas untuk format file environment sederhana seperti `.env` contoh; jangan gunakan nilai ber-spasi atau shell substitution di dalamnya.

## 🔐 Keamanan dan batasan

- Jangan commit `.env`, token bot, webhook secret, atau database berisi data pengguna.
- Jika token bocor, cabut segera di BotFather dan perbarui secret di server.
- Contoh membatasi pesan dan perintah ke chat pribadi. Tetap validasi input dan batasi ukuran/jumlah data sesuai kebutuhan aplikasi.
- Handler umur membatasi nilai ke 0–130 dan nama ke 1–100 karakter; aturan ini hanya contoh dan mungkin perlu disesuaikan.
- Terapkan rate limiting dan proteksi spam yang sesuai di aplikasi. Rate limiting permintaan keluar ke Bot API berbeda dari pembatasan pesan masuk pengguna.
- Beri tahu pengguna data apa yang disimpan, batasi akses, tentukan masa retensi, dan sediakan proses penghapusan/backup yang sesuai hukum dan kebutuhan layanan.
- SQLite cocok untuk contoh sederhana/satu instance. Jangan menganggap file database lokal sebagai backup atau penyimpanan high-availability.
- Log error untuk diagnosis, tetapi jangan mencatat token, secret, atau isi percakapan sensitif.
- Jangan aktifkan `concurrent_updates` untuk `ConversationHandler` tanpa memahami persyaratan pemrosesan berurutan.

## 🩺 Troubleshooting

<details>
<summary><b>Bot tidak merespons atau token ditolak</b></summary>

Periksa `BOT_TOKEN`, pastikan pengguna sudah menekan **Start** pada bot, cek koneksi server, dan lihat log proses. Jika token salah atau telah dicabut, buat token baru di BotFather dan perbarui `.env`.

</details>

<details>
<summary><b><code>Conflict: terminated by other getUpdates request</code></b></summary>

Ada instance lain yang menggunakan polling dengan token yang sama. Hentikan instance lama atau pastikan hanya satu worker polling berjalan. Bila beralih ke webhook, pastikan webhook lama tidak mengganggu konfigurasi yang baru.

</details>

<details>
<summary><b><code>BOT_TOKEN tidak ditemukan</code></b></summary>

Pastikan `.env` berada di direktori kerja tempat `python bot.py` dijalankan, atau ekspor `BOT_TOKEN` sebagai environment variable. Pastikan nama variabel tepat dan nilainya bukan placeholder.

</details>

<details>
<summary><b>Webhook gagal diatur atau Telegram tidak dapat mengirim update</b></summary>

Pastikan URL publik memakai HTTPS dengan sertifikat valid, DNS dan reverse proxy benar, path URL sama dengan `WEBHOOK_PATH`, port publik dapat dijangkau Telegram, serta `WEBHOOK_SECRET` disetel. Periksa log aplikasi dan proxy.

</details>

<details>
<summary><b>Data SQLite hilang setelah deployment Docker</b></summary>

Gunakan `docker compose` dari repository ini agar named volume dipasang di `/data`. Jangan menjalankan `docker compose down -v` jika volume berisi data yang masih dibutuhkan.

</details>

## 📚 Referensi

- [Dokumentasi python-telegram-bot v22.8](https://docs.python-telegram-bot.org/en/v22.8/)
- [Contoh resmi python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot/tree/master/examples)
- [Telegram Bot API](https://core.telegram.org/bots/api)
- [BotFather](https://t.me/BotFather)

---

Kode dan panduan dilisensikan di bawah MIT; lihat berkas [`LICENSE`](LICENSE).

⭐ Jika panduan ini membantu, silakan beri bintang pada repository.
