# EE Internship Scraper - Summer 2026

An automated job scraper that finds electrical engineering, computer engineering, hardware, and semiconductor internships for Summer 2026. Features a clean web interface to track your applications and auto-updates every 6 hours via GitHub Actions.

## Features

- **Automated Scraping**: Runs every 6 hours via GitHub Actions
- **Multiple Job Boards**: Scrapes from Indeed, LinkedIn, and more
- **Smart Filtering**: Focuses on EE, CompE, hardware, semiconductor, and data science roles
- **Application Tracking**: Track which jobs you've applied to and interview status
- **Clean UI**: Beautiful, responsive interface hosted on GitHub Pages
- **Export Data**: Export your application status to CSV
- **Deduplication**: Automatically removes duplicate job postings

## Job Targets

The scraper looks for internships in:
- Circuit Design (Analog, Digital, Mixed-Signal)
- VLSI/ASIC Design
- FPGA Development
- Hardware Engineering
- Semiconductor/Silicon Engineering
- Embedded Systems
- PCB Design
- RF Engineering
- Data Science & Machine Learning

## Setup Instructions

### 1. Clone and Initialize Repository

```bash
cd j*b_scraper
git init
git add .
git commit -m "Initial commit: EE internship scraper"
```

### 2. Create GitHub Repository

```bash
# Create a new repository on GitHub (via web or CLI)
gh repo create ee-internship-tracker --public --source=. --remote=origin

# Or manually:
# 1. Go to github.com/new
# 2. Create a new repository named "ee-internship-tracker"
# 3. Don't initialize with README (we already have files)

# Push to GitHub
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/ee-internship-tracker.git
git push -u origin main
```

### 3. Enable GitHub Pages

1. Go to your repository on GitHub
2. Click "Settings" → "Pages"
3. Under "Source", select "GitHub Actions"
4. The site will be available at: `https://YOUR_USERNAME.github.io/ee-internship-tracker/`

### 4. Enable GitHub Actions

1. Go to "Actions" tab in your repository
2. Enable workflows if prompted
3. The scraper will automatically run every 6 hours
4. You can also manually trigger it from the Actions tab

### 5. Set Up Permissions (Important!)

1. Go to "Settings" → "Actions" → "General"
2. Scroll to "Workflow permissions"
3. Select "Read and write permissions"
4. Check "Allow GitHub Actions to create and approve pull requests"
5. Click "Save"

## Local Testing

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run Scraper Locally

```bash
python scraper_main.py
```

This will create a `data/` directory with JSON files containing scraped jobs.

### Test the Website Locally

```bash
# Serve the docs folder locally
cd docs
python -m http.server 8000

# Open browser to http://localhost:8000
```

Note: When testing locally, you'll need to adjust the fetch path in `docs/app.js` to load from `../data/jobs_all.json`.

## Configuration

Edit [config.py](config.py) to customize:

- **JOB_KEYWORDS**: Search terms for job queries
- **ROLE_KEYWORDS**: Keywords to filter relevant roles
- **LOCATIONS**: Preferred job locations
- **PRIORITY_COMPANIES**: Companies you're particularly interested in
- **SCRAPE_INTERVAL_HOURS**: How often to scrape (for local use)

## Project Structure

```
j*b_scraper/
├── scrapers/
│   ├── __init__.py
│   ├── base_scraper.py      # Base scraper class
│   ├── indeed_scraper.py     # Indeed job board scraper
│   └── linkedin_scraper.py   # LinkedIn job board scraper
├── docs/                     # GitHub Pages site
│   ├── index.html           # Main page
│   ├── styles.css           # Styling
│   └── app.js               # Frontend logic
├── data/                     # Scraped job data (auto-generated)
│   ├── jobs_all.json        # All jobs aggregated
│   ├── jobs_indeed.json     # Indeed jobs
│   └── jobs_linkedin.json   # LinkedIn jobs
├── .github/
│   └── workflows/
│       ├── scrape_jobs.yml  # Automated scraping
│       └── deploy_pages.yml # Deploy to GitHub Pages
├── config.py                 # Configuration settings
├── scraper_main.py          # Main scraper script
├── requirements.txt          # Python dependencies
└── README.md                # This file
```

## Usage

### Viewing Jobs

Visit your GitHub Pages site: `https://YOUR_USERNAME.github.io/ee-internship-tracker/`

### Tracking Applications

- Click "Mark Applied" when you apply to a job
- Click "Mark Interviewing" when you get an interview
- Use filters to view jobs by status
- Search by title, company, or location
- Export your application data to CSV

### Application Status

All tracking data is stored in your browser's localStorage, so it persists across visits but is specific to your device.

## Extending the Scraper

### Add More Job Boards

1. Create a new scraper in `scrapers/` (e.g., `glassdoor_scraper.py`)
2. Inherit from `BaseScraper`
3. Implement the `scrape()` method
4. Add to `scrapers/__init__.py`
5. Add to `scraper_main.py`

Example:
```python
from .base_scraper import BaseScraper, Job

class GlassdoorScraper(BaseScraper):
    def __init__(self):
        super().__init__("Glassdoor")

    def scrape(self, keywords, location):
        # Your scraping logic here
        pass
```

### Adjust Scraping Frequency

Edit `.github/workflows/scrape_jobs.yml`:
```yaml
schedule:
  - cron: '0 */6 * * *'  # Every 6 hours
  # Change to '0 */3 * * *' for every 3 hours
  # Or '0 0 * * *' for daily at midnight
```

## Troubleshooting

### Jobs Not Showing Up

1. Check GitHub Actions logs for errors
2. Verify the scraper ran successfully
3. Check that `data/jobs_all.json` was created
4. Ensure GitHub Pages is enabled and deployed

### Scraper Fails

- Job board websites frequently change their HTML structure
- Update the selectors in the scraper files
- Check for rate limiting (add delays between requests)
- Some sites may block automated access

### Application Tracking Not Saving

- Clear browser cache and localStorage
- Check browser console for errors
- Ensure JavaScript is enabled

## Best Practices

1. **Be Respectful**: Don't scrape too aggressively (rate limits are built in)
2. **Keep Updated**: Job board HTML changes frequently - update scrapers as needed
3. **Test Locally**: Run scrapers locally before pushing to GitHub
4. **Monitor Actions**: Check GitHub Actions logs regularly for errors
5. **Backup Data**: Occasionally export your application tracking data

## Legal & Ethics

- This tool is for personal use to aggregate publicly available job postings
- Respect robots.txt and terms of service of job boards
- Don't use scraped data for commercial purposes
- Always apply through official channels

## Contributing

Feel free to:
- Add more job board scrapers
- Improve filtering logic
- Enhance the UI
- Add notification features (email, Discord, Slack)
- Add unit tests

## Future Enhancements

- [ ] Email notifications for new jobs
- [ ] Discord/Slack integration
- [ ] Mobile-responsive improvements
- [ ] Save notes for each application
- [ ] Deadline tracking
- [ ] Interview preparation resources
- [ ] Company research links
- [ ] Salary information aggregation

## License

MIT License - Feel free to use and modify for your own internship search!

## Good Luck!

Hope this helps you land that dream EE internship for Summer 2026! Remember to:
- Apply early and often
- Tailor your resume for each role
- Network on LinkedIn
- Practice your technical interviews
- Stay persistent!

---

Built with ❤️ by Krishna | Auto-updates every 6 hours
