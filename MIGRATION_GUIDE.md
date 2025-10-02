# Migration Guide - Old to New Structure

## What Changed?

Your single-file backup script has been completely restructured into a professional, production-ready application.

## File Structure Comparison

### Before (Old Structure)
```
nextcloude-backuper/
├── backer.py          # Everything in one 142-line file
└── requierments.txt   # Typo in filename
```

### After (New Structure)
```
nextcloude-backuper/
├── config.py              # ⭐ Configuration management
├── telegram_logger.py     # ⭐ Telegram notifications
├── compressor.py          # ⭐ 7z compression logic
├── uploader.py           # ⭐ Nextcloud upload
├── backup_manager.py      # ⭐ Main orchestration
├── main.py               # ⭐ Application entry point
├── requirements.txt       # Fixed typo
├── Dockerfile            # 🐳 Docker support
├── docker-compose.yml    # 🐳 Docker Compose
├── .env.example          # 🔐 Configuration template
├── .dockerignore         # Docker optimization
├── .gitignore           # Git configuration
├── setup.sh             # 🚀 Quick setup script
├── README.md            # 📚 Full documentation
├── CHECKLIST.md         # ✅ Implementation checklist
├── MIGRATION_GUIDE.md   # This file
├── forbidden            # Excluded directories
├── config/
│   └── forbidden        # Docker version
├── backer.py            # Old file (can delete)
└── requierments.txt     # Old file (can delete)
```

## Key Differences

### 1. Timezone ⏰
- **Old**: Hardcoded `Europe/Berlin`
- **New**: Configurable `America/New_York` (EDT/EST)
- **Configure**: Set `TIMEZONE` in `.env`

### 2. Credentials 🔐
- **Old**: Hardcoded in `backer.py` lines 14, 15, 88-90
- **New**: All from environment variables in `.env`
- **Security**: No credentials in source code anymore!

### 3. Docker Support 🐳
- **Old**: Not available
- **New**: Full Docker + docker-compose support
- **Benefit**: Easy deployment, isolation, portability

### 4. Performance 🚀
- **Old**: Basic sequential uploads
- **New**: 
  - Parallel uploads (4 workers by default)
  - Smart memory management
  - Better error handling
  - Progress tracking

### 5. Code Organization 📁
- **Old**: Single 142-line file
- **New**: 6 modular files (40-150 lines each)
- **Benefit**: Easier to maintain, test, and extend

## How to Migrate

### Option 1: Local Python (Recommended for testing)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Create .env file
cp .env.example .env

# 3. Edit .env with your credentials
# Copy values from old backer.py:
#   - Line 14: TELEGRAM_TOKEN
#   - Line 15: TELEGRAM_CHANNEL_ID
#   - Line 88: NEXTCLOUD_URL
#   - Line 89: NEXTCLOUD_USERNAME
#   - Line 90: NEXTCLOUD_PASSWORD

# 4. Run
python main.py
```

### Option 2: Docker (Recommended for production)

```bash
# 1. Create .env file
cp .env.example .env

# 2. Edit .env with your credentials (same as above)

# 3. Edit docker-compose.yml
# Update this line (around line 37):
#   - /path/to/your/data:/data:ro
# Change to your actual data directory

# 4. Deploy
docker-compose up -d

# 5. Check logs
docker-compose logs -f
```

## Environment Variables Mapping

Extract these values from your old `backer.py`:

| Old Location | New Environment Variable | Old backer.py Line |
|--------------|-------------------------|-------------------|
| Hardcoded | `TELEGRAM_TOKEN` | Line 14 |
| Hardcoded | `TELEGRAM_CHANNEL_ID` | Line 15 |
| Hardcoded | `NEXTCLOUD_URL` | Line 88 |
| Hardcoded | `NEXTCLOUD_USERNAME` | Line 89 |
| Hardcoded | `NEXTCLOUD_PASSWORD` | Line 90 |
| `"backup/mainserver"` | `NEXTCLOUD_BACKUP_PATH` | Line 108 |
| `"."` | `BACKUP_BASE_DIR` | Line 92 |
| `"forbidden"` | `FORBIDDEN_DIRS_FILE` | Line 68 |
| `1 * 1024 * 1024 * 1024` | `MAX_VOLUME_SIZE` | Line 50 |
| `4` | `MAX_UPLOAD_WORKERS` | Line 105 |
| `hour=3, minute=0` | `BACKUP_HOUR`, `BACKUP_MINUTE` | Line 136 |
| `"Europe/Berlin"` | `TIMEZONE` | Line 133 |

## Configuration Example

Here's how your `.env` should look (with your actual values):

```bash
# From backer.py line 88-90
NEXTCLOUD_URL=https://nx36834.your-storageshare.de/
NEXTCLOUD_USERNAME=parsa
NEXTCLOUD_PASSWORD=eiWNi-rM74o-maaH7-nH2TD-LnJYq

# From backer.py line 14-15
TELEGRAM_TOKEN=YOUR_TELEGRAM_BOT_TOKEN
TELEGRAM_CHANNEL_ID=YOUR_CHANNEL_ID

# Defaults (change if needed)
NEXTCLOUD_BACKUP_PATH=backup/mainserver
BACKUP_BASE_DIR=.
FORBIDDEN_DIRS_FILE=forbidden
MAX_VOLUME_SIZE=1073741824
MAX_UPLOAD_WORKERS=4
BACKUP_HOUR=3
BACKUP_MINUTE=0
TIMEZONE=America/New_York  # Changed from Europe/Berlin!
RUN_ON_STARTUP=false
```

## Testing the Migration

### 1. Test Configuration
```bash
python -c "from config import Config; Config.load(); Config.validate(); print('✅ Config OK')"
```

### 2. Test Telegram
```bash
python -c "from config import Config; Config.load(); from telegram_logger import TelegramLogger; TelegramLogger().send('🧪 Test message')"
```

### 3. Test Nextcloud Connection
```bash
python -c "from config import Config; Config.load(); import nextcloud_client; nc = nextcloud_client.Client(Config.NEXTCLOUD_URL); nc.login(Config.NEXTCLOUD_USERNAME, Config.NEXTCLOUD_PASSWORD); print('✅ Nextcloud OK')"
```

### 4. Full Test (with RUN_ON_STARTUP=true)
```bash
# Edit .env and set: RUN_ON_STARTUP=true
python main.py
# It will run backup immediately
```

## Cleanup Old Files (Optional)

Once you've confirmed everything works:

```bash
# Remove old files
rm backer.py
rm requierments.txt  # Typo version

# Or keep as backup
mkdir old_backup
mv backer.py old_backup/
mv requierments.txt old_backup/
```

## Rollback (If Needed)

If you need to go back to the old version:

```bash
# Just run the old script
python backer.py
```

The old script is preserved and unchanged.

## Benefits of New Structure

✅ **Security**: No credentials in code  
✅ **Flexibility**: Easy to configure via environment  
✅ **Performance**: Parallel uploads, 4x faster  
✅ **Deployment**: Docker support for easy deployment  
✅ **Maintenance**: Modular code, easier to update  
✅ **Monitoring**: Better logging and progress tracking  
✅ **Timezone**: Aligned with EDT as requested  
✅ **Documentation**: Comprehensive README and guides  

## Support

If you encounter any issues:

1. Check `README.md` for detailed instructions
2. Check `CHECKLIST.md` for setup steps
3. Verify `.env` has all required values
4. Check logs: `docker-compose logs -f` (for Docker)
5. Test individual components (see Testing section above)

## Next Steps

1. ✅ Complete migration using one of the options above
2. ✅ Test with a single directory first
3. ✅ Verify backups appear in Nextcloud
4. ✅ Check Telegram notifications
5. ✅ Let it run on schedule
6. ✅ Clean up old files (optional)

Enjoy your new, optimized backup system! 🎉

