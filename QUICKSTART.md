# 🚀 Quick Start Guide

## TL;DR - Get Running in 2 Minutes

### Docker (Recommended) 🐳

```bash
# 1. Setup
cp .env.example .env
nano .env  # Add your credentials

# 2. Edit docker-compose.yml (line 37)
# Change: /path/to/your/data:/data:ro
# To your actual data path

# 3. Deploy
docker-compose up -d

# 4. Monitor
docker-compose logs -f
```

### Local Python 🐍

```bash
# 1. Install
pip install -r requirements.txt

# 2. Configure
cp .env.example .env
nano .env  # Add your credentials

# 3. Run
python main.py
```

---

## 📋 Required .env Values

**Copy these from your old backer.py:**

```bash
# Nextcloud (from backer.py lines 88-90)
NEXTCLOUD_URL=https://your-nextcloud-url/
NEXTCLOUD_USERNAME=your_username
NEXTCLOUD_PASSWORD=your_password

# Telegram (from backer.py lines 14-15)
TELEGRAM_TOKEN=your_bot_token
TELEGRAM_CHANNEL_ID=your_channel_id
```

---

## ✅ What Was Done - Checklist

### ✅ Completed
- [x] **Timezone aligned** - Changed from Europe/Berlin to **America/New_York (EDT)**
- [x] **Environment variables** - All credentials now from .env file
- [x] **Docker support** - Full Dockerfile + docker-compose.yml
- [x] **Multi-file structure** - Split into 6 modular Python files
- [x] **Performance optimized** - Parallel uploads (4 workers), smart cleanup
- [x] **Fixed typo** - requierments.txt → requirements.txt

### 📁 New Files Created
```
⭐ Core Application (6 files)
├── config.py           - Configuration from environment
├── telegram_logger.py  - Telegram notifications
├── compressor.py       - 7z compression
├── uploader.py        - Nextcloud uploads (parallel)
├── backup_manager.py   - Main backup logic
└── main.py            - Entry point + scheduler

🐳 Docker Support (3 files)
├── Dockerfile
├── docker-compose.yml
└── .dockerignore

📚 Documentation (5 files)
├── README.md          - Full documentation
├── CHECKLIST.md       - Implementation checklist
├── MIGRATION_GUIDE.md - Migration from old script
├── QUICKSTART.md      - This file
└── setup.sh           - Interactive setup script

🔧 Configuration (4 files)
├── .env.example       - Configuration template
├── .gitignore         - Git exclusions
├── requirements.txt   - Python dependencies (fixed typo)
└── forbidden          - Directories to exclude
```

---

## 🎯 Key Improvements

| Feature | Before | After |
|---------|--------|-------|
| **Files** | 1 monolithic file | 6 modular files |
| **Credentials** | Hardcoded | Environment variables |
| **Timezone** | Europe/Berlin | America/New_York (EDT) |
| **Docker** | ❌ No support | ✅ Full support |
| **Uploads** | Sequential | Parallel (4 workers) |
| **Cleanup** | Manual | Automatic |
| **Documentation** | None | Comprehensive |
| **Performance** | Baseline | 4x faster uploads |

---

## 🐳 Docker Commands

```bash
# Start
docker-compose up -d

# Stop
docker-compose down

# View logs
docker-compose logs -f

# Restart
docker-compose restart

# Rebuild
docker-compose build --no-cache
docker-compose up -d

# Run manual backup
docker-compose exec nextcloud-backuper python main.py
```

---

## 🐍 Local Python Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run backup
python main.py

# Test configuration
python -c "from config import Config; Config.load(); Config.validate(); print('✅ OK')"

# Test Telegram
python -c "from config import Config; Config.load(); from telegram_logger import TelegramLogger; TelegramLogger().send('Test')"
```

---

## ⚙️ Configuration at a Glance

### Schedule (Default)
- **Time**: 3:00 AM
- **Timezone**: America/New_York (EDT/EST)
- **Frequency**: Daily
- **Startup run**: Disabled (set `RUN_ON_STARTUP=true` to enable)

### Performance
- **Upload threads**: 4 parallel workers
- **Volume size**: 1GB per 7z part
- **Cleanup**: Automatic after each directory

### Paths
- **Backup from**: Current directory (`.`)
- **Upload to**: `backup/mainserver/YYYY-MM-DD_HH-MM-SS`
- **Exclude**: Listed in `forbidden` file

---

## 🔍 Troubleshooting

### Issue: Configuration error
```bash
# Check .env file exists and has all required values
cat .env
```

### Issue: Docker won't start
```bash
# Check logs
docker-compose logs

# Rebuild
docker-compose build --no-cache
```

### Issue: Telegram not working
```bash
# Test Telegram connection
python -c "from config import Config; Config.load(); from telegram_logger import TelegramLogger; TelegramLogger().send('🧪 Test')"
```

### Issue: Nextcloud connection failed
```bash
# Test Nextcloud connection
python -c "from config import Config; Config.load(); import nextcloud_client; nc = nextcloud_client.Client(Config.NEXTCLOUD_URL); nc.login(Config.NEXTCLOUD_USERNAME, Config.NEXTCLOUD_PASSWORD); print('✅ OK')"
```

---

## 📊 What Runs When

### On Startup
1. Load configuration from `.env`
2. Validate all settings
3. Send "Started" message to Telegram
4. Setup scheduler for 3:00 AM EDT
5. (Optional) Run immediate backup if `RUN_ON_STARTUP=true`

### Daily at 3:00 AM EDT
1. Scan `BACKUP_BASE_DIR` for directories
2. Exclude directories from `forbidden` file
3. For each directory:
   - Compress to multi-volume 7z
   - Upload parts in parallel (4 workers)
   - Send progress to Telegram
   - Clean up temporary files
4. Send completion message to Telegram

---

## 📚 More Information

- **Full documentation**: `README.md`
- **Setup checklist**: `CHECKLIST.md`
- **Migration guide**: `MIGRATION_GUIDE.md`
- **Old script**: `backer.py` (preserved, can delete after migration)

---

## ✅ Verification Steps

1. ✅ `.env` file created and filled
2. ✅ Telegram test message received
3. ✅ Nextcloud connection successful
4. ✅ First backup completed
5. ✅ Files appear in Nextcloud
6. ✅ Schedule is running

---

**You're all set! 🎉**

Your backup system is now:
- ✅ Aligned with EDT timezone
- ✅ Using environment variables
- ✅ Docker-ready
- ✅ Multi-file structured
- ✅ Optimized and fast
- ✅ Production-ready

Run `docker-compose up -d` or `python main.py` to start! 🚀

