#!/bin/bash
# Quick setup script for Nextcloud Backuper

set -e

echo "🚀 Nextcloud Backuper - Quick Setup"
echo "===================================="
echo ""

# Check if .env exists
if [ -f ".env" ]; then
    echo "⚠️  .env file already exists. Skipping copy."
else
    echo "📝 Copying .env.example to .env..."
    cp .env.example .env
    echo "✅ Created .env file"
    echo "⚠️  IMPORTANT: Edit .env and fill in your credentials!"
fi

echo ""

# Check if Python is installed
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    echo "✅ Python detected: $PYTHON_VERSION"
else
    echo "❌ Python 3 is not installed. Please install Python 3.11 or higher."
    exit 1
fi

echo ""
echo "Choose setup method:"
echo "1) Local Python installation"
echo "2) Docker installation"
echo ""
read -p "Enter choice (1 or 2): " choice

if [ "$choice" == "1" ]; then
    echo ""
    echo "📦 Installing Python dependencies..."
    pip install -r requirements.txt
    echo "✅ Dependencies installed"
    echo ""
    echo "📝 Next steps:"
    echo "   1. Edit .env file with your credentials"
    echo "   2. Edit 'forbidden' file with directories to exclude"
    echo "   3. Run: python3 main.py"
    echo ""
    
elif [ "$choice" == "2" ]; then
    # Check if Docker is installed
    if ! command -v docker &> /dev/null; then
        echo "❌ Docker is not installed. Please install Docker first."
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null 2>&1; then
        echo "❌ Docker Compose is not installed. Please install Docker Compose first."
        exit 1
    fi
    
    echo "✅ Docker detected"
    echo ""
    echo "📝 Next steps:"
    echo "   1. Edit .env file with your credentials"
    echo "   2. Edit docker-compose.yml and update volume paths"
    echo "   3. Edit config/forbidden file with directories to exclude"
    echo "   4. Run: docker-compose up -d"
    echo "   5. Monitor: docker-compose logs -f"
    echo ""
else
    echo "❌ Invalid choice"
    exit 1
fi

echo "📚 For detailed instructions, see README.md"
echo "📋 For complete checklist, see CHECKLIST.md"

