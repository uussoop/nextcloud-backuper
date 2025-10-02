# Nextcloud Backuper

A robust, automated backup solution that compresses directories into multi-volume 7z archives and uploads them to Nextcloud with Telegram notifications.

## Features

- 🗜️ **Multi-volume 7z compression** - Split large directories into manageable chunks
- ☁️ **Nextcloud integration** - Automatic upload to your Nextcloud instance
- 📱 **Telegram notifications** - Real-time status updates via Telegram
- ⏰ **Scheduled backups** - Configurable cron-based scheduling (default: 3:00 AM EDT)
- 🚀 **Parallel uploads** - Multi-threaded uploading for faster transfers
- 🔒 **Directory filtering** - Exclude specific directories from backup
- 🐳 **Docker support** - Easy containerized deployment
- 💾 **Smart cleanup** - Automatic cleanup of temporary files to save disk space

## Project Structure

```
nextcloude-backuper/
├── config.py              # Configuration management
├── telegram_logger.py     # Telegram notification handling
├── compressor.py          # 7z compression logic
├── uploader.py           # Nextcloud upload functionality
├── backup_manager.py      # Main backup orchestration
├── main.py               # Application entry point
├── requirements.txt       # Python dependencies
├── Dockerfile            # Docker image configuration
├── docker-compose.yml    # Docker Compose setup
├── .env.example          # Example environment variables
└── README.md             # This file
```

## Setup

### Prerequisites

- Python 3.11+
- Nextcloud account with WebDAV access
- Telegram bot token and channel ID

### Local Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd nextcloude-backuper
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your credentials
   ```

4. **Create forbidden file (optional)**
   ```bash
   # Create a file named 'forbidden' with directories to exclude (one per line)
   echo "/path/to/exclude" > forbidden
   ```

5. **Run the application**
   ```bash
   python main.py
   ```

### Docker Installation

1. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your credentials
   ```

2. **Update docker-compose.yml**
   - Edit the volumes section to point to your data directory
   - Adjust resource limits if needed

3. **Build and run**
   ```bash
   docker-compose up -d
   ```

4. **View logs**
   ```bash
   docker-compose logs -f
   ```

## Configuration

All configuration is done via environment variables. See `.env.example` for all available options.

### Required Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `NEXTCLOUD_URL` | Your Nextcloud instance URL | `https://cloud.example.com` |
| `NEXTCLOUD_USERNAME` | Nextcloud username | `myuser` |
| `NEXTCLOUD_PASSWORD` | Nextcloud password | `mypassword` |
| `TELEGRAM_TOKEN` | Telegram bot token | `1234567890:ABCdef...` |
| `TELEGRAM_CHANNEL_ID` | Telegram channel/chat ID | `@mychannel` or `-1001234567890` |

### Optional Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `NEXTCLOUD_BACKUP_PATH` | `backup/mainserver` | Remote path for backups |
| `BACKUP_BASE_DIR` | `.` | Local directory to scan for backups |
| `FORBIDDEN_DIRS_FILE` | `forbidden` | File containing excluded directories |
| `MAX_VOLUME_SIZE` | `1073741824` | Max size per 7z volume (1GB) |
| `MAX_UPLOAD_WORKERS` | `4` | Number of parallel upload threads |
| `BACKUP_HOUR` | `3` | Hour to run daily backup (0-23) |
| `BACKUP_MINUTE` | `0` | Minute to run daily backup (0-59) |
| `TIMEZONE` | `America/New_York` | Timezone for scheduling (EDT/EST) |
| `RUN_ON_STARTUP` | `false` | Run backup immediately on startup |

## Usage

### Manual Backup

To run a backup manually:

```bash
# Local
python main.py

# Docker
docker-compose exec nextcloud-backuper python main.py
```

### Scheduled Backup

The application runs automatically based on the schedule defined in your environment variables (default: 3:00 AM EDT daily).

### Excluding Directories

Create a file named `forbidden` (or your custom name) with absolute paths to exclude:

```
/path/to/exclude/dir1
/path/to/exclude/dir2
```

## How It Works

1. **Scan**: Scans `BACKUP_BASE_DIR` for directories (excluding those in forbidden file)
2. **Compress**: Compresses each directory into multi-volume 7z archives
3. **Upload**: Uploads archive parts to Nextcloud in parallel using thread pool
4. **Notify**: Sends progress updates to Telegram
5. **Cleanup**: Removes temporary files after each directory to save space

## Optimization Features

- **Parallel uploads**: Multiple files uploaded simultaneously using `ThreadPoolExecutor`
- **Smart memory management**: Temporary files cleaned up after each directory
- **Multi-volume archives**: Large directories split into manageable chunks
- **Silent notifications**: Progress updates sent without sound to reduce spam
- **Efficient compression**: Uses py7zr with LZMA2 compression

## Troubleshooting

### Missing dependencies
```bash
pip install -r requirements.txt --force-reinstall
```

### Permission errors
- Ensure the application has read access to backup directories
- Check Nextcloud credentials and permissions

### Docker issues
```bash
# Rebuild container
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### Telegram not working
- Verify bot token and channel ID
- Ensure bot is admin in the channel
- Check that bot can send messages

## License

MIT License - See LICENSE file for details

## Support

For issues and feature requests, please open an issue on the repository.

