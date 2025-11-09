# Quick Start Guide

Get your EE internship scraper up and running in 5 minutes!

## Step 1: Initialize Git Repository

```bash
git init
git add .
git commit -m "Initial commit: EE internship scraper"
```

## Step 2: Create GitHub Repository

**Option A: Using GitHub CLI (recommended)**
```bash
gh repo create ee-internship-tracker --public --source=. --remote=origin --push
```

**Option B: Manual**
1. Go to https://github.com/new
2. Repository name: `ee-internship-tracker`
3. Make it public
4. DON'T initialize with README
5. Click "Create repository"
6. Then run:
```bash
git remote add origin https://github.com/YOUR_USERNAME/ee-internship-tracker.git
git branch -M main
git push -u origin main
```

## Step 3: Configure GitHub Settings

### Enable GitHub Actions Permissions
1. Go to your repo → **Settings** → **Actions** → **General**
2. Under "Workflow permissions":
   - Select **"Read and write permissions"**
   - Check **"Allow GitHub Actions to create and approve pull requests"**
3. Click **Save**

### Enable GitHub Pages
1. Go to **Settings** → **Pages**
2. Under "Source", select **"GitHub Actions"**
3. Your site will be live at: `https://YOUR_USERNAME.github.io/ee-internship-tracker/`

## Step 4: Run First Scrape

### Option A: Trigger GitHub Action
1. Go to **Actions** tab
2. Click "Scrape Jobs" workflow
3. Click "Run workflow" → "Run workflow"
4. Wait for it to complete (2-3 minutes)

### Option B: Run Locally First
```bash
# Install dependencies
pip install -r requirements.txt

# Run scraper
python scraper_main.py

# Commit the data
git add data/
git commit -m "Initial job data"
git push
```

## Step 5: View Your Site

Visit `https://YOUR_USERNAME.github.io/ee-internship-tracker/`

It may take 1-2 minutes for GitHub Pages to deploy after your first push.

## That's It!

Your scraper will now automatically run every 6 hours and update your site with new internship postings!

## Customize (Optional)

Edit `config.py` to customize:
- Search keywords
- Target locations
- Priority companies
- Filtering criteria

## Need Help?

Check the main [README.md](README.md) for detailed documentation and troubleshooting.
