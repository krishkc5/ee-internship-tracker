#!/bin/bash

# EE Internship Scraper Setup Script
# This script helps you set up the project quickly

set -e

echo "=========================================="
echo "EE Internship Scraper Setup"
echo "=========================================="
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or later."
    exit 1
fi

echo "✓ Python 3 found: $(python3 --version)"
echo ""

# Install dependencies
echo "Installing Python dependencies..."
pip3 install -r requirements.txt
echo "✓ Dependencies installed"
echo ""

# Run tests
echo "Running tests..."
python3 test_scraper.py
echo ""

# Initialize git if not already initialized
if [ ! -d ".git" ]; then
    echo "Initializing Git repository..."
    git init
    git add .
    git commit -m "Initial commit: EE internship scraper"
    echo "✓ Git repository initialized"
else
    echo "✓ Git repository already initialized"
fi
echo ""

# Instructions for GitHub setup
echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo ""
echo "1. Create GitHub repository:"
echo "   gh repo create ee-internship-tracker --public --source=. --remote=origin --push"
echo ""
echo "2. Enable GitHub Actions:"
echo "   - Go to Settings → Actions → General"
echo "   - Enable 'Read and write permissions'"
echo ""
echo "3. Enable GitHub Pages:"
echo "   - Go to Settings → Pages"
echo "   - Select 'GitHub Actions' as source"
echo ""
echo "4. Your site will be live at:"
echo "   https://YOUR_USERNAME.github.io/ee-internship-tracker/"
echo ""
echo "For detailed instructions, see QUICKSTART.md"
echo ""
