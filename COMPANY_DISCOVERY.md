# Company Discovery Tool 🔍

A meta-scraper that automatically discovers new companies posting EE/Hardware/Semiconductor internships!

## What It Does

This tool scrapes job boards and startup directories to find companies you should add to your scraper. It's like a scraper for finding companies to scrape!

### Sources

The discovery tool searches:

1. **LinkedIn Jobs** - Companies posting hardware/semiconductor internships
2. **Indeed** - Active recruiters for EE positions
3. **Built In** - Hardware and semiconductor startup listings
4. **Y Combinator Directory** - Hardware/semiconductor startups from YC

## How to Use

### Run Company Discovery

```bash
python discover_companies.py
```

This will:
- Search all sources for companies posting relevant internships
- Save results to `data/discovered_companies.json`
- Show you new companies found this run
- Track total companies discovered over time

### Review Results

Check `data/discovered_companies.json`:

```json
{
  "companies": [
    "Cerebras Systems",
    "SiFive",
    "Groq",
    "Astera Labs",
    ...
  ],
  "total_count": 150,
  "new_this_run": 12,
  "last_updated": "2025-01-09 15:30:00",
  "new_companies_list": [
    "NewStartup Inc",
    "CoolChip Corp",
    ...
  ]
}
```

### Add Promising Companies

1. Research the companies from the discovery list
2. Find their careers page URL
3. Add them to `scrapers/company_scraper.py`:

```python
"NewCompany": {
    "url": "https://newcompany.com/careers",
    "search_params": {"q": "intern"}
}
```

## Automated Discovery (Optional)

### Add to GitHub Actions

Create `.github/workflows/discover_companies.yml`:

```yaml
name: Discover New Companies

on:
  schedule:
    - cron: '0 0 1 * *'  # Monthly on the 1st
  workflow_dispatch:

jobs:
  discover:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - run: pip install -r requirements.txt
      - run: python discover_companies.py

      - name: Commit discoveries
        run: |
          git config --local user.email "actions@github.com"
          git config --local user.name "GitHub Actions"
          git add data/discovered_companies.json
          git diff --quiet && git diff --staged --quiet || (git commit -m "Update discovered companies" && git push)
```

This will automatically discover new companies monthly!

## Manual Research Helper

You can also use the scraper to research individual companies:

```python
from scrapers.company_discovery_scraper import CompanyDiscoveryScraper

scraper = CompanyDiscoveryScraper()
info = scraper.get_company_info("Cerebras Systems")
print(info)
# {'name': 'Cerebras Systems', 'careers_url': 'https://cerebras.net/careers/', 'found': True}
```

## Tips

### Best Practices

1. **Run Monthly** - New startups emerge constantly
2. **Check YC Batches** - Y Combinator announces new batches quarterly
3. **Follow Tech News** - New chip startups often get funding announcements
4. **LinkedIn Company Pages** - Check "Companies" section for similar organizations

### Quality Over Quantity

Not every discovered company will be worth adding:
- ✅ Add companies actively hiring interns
- ✅ Add companies with clear hardware/EE roles
- ✅ Add companies with accessible career pages
- ❌ Skip companies with no internship programs
- ❌ Skip companies with complex application portals
- ❌ Skip consulting firms posting for clients

### Startup Categories to Watch

- **AI Chip Startups**: Cerebras, Groq, SambaNova, Graphcore
- **RISC-V Companies**: SiFive, Ventana, Esperanto
- **Interconnect/Networking**: Astera Labs, Alphawave, Marvell
- **Analog/Mixed-Signal**: Cirrus Logic, Skyworks, Qorvo
- **Memory/Storage**: Kioxia, SK Hynix, Western Digital
- **Power/Battery**: Northvolt, QuantumScape, Solid Power
- **Quantum Computing**: IonQ, Rigetti, PsiQuantum

## Example Output

```
======================================================================
🔍 COMPANY DISCOVERY TOOL
======================================================================

Searching job boards and startup directories for companies
posting EE/Hardware/Semiconductor internships...

Discovering companies from LinkedIn...
Found 45 companies on LinkedIn

Discovering companies from Indeed...
Found 38 companies on Indeed

Discovering companies from Built In...
Discovered companies from Built In

Discovering companies from Y Combinator...
Found 23 YC companies

============================================================
Company Discovery Summary:
  Total companies discovered: 156
  New companies this run: 18
  Saved to: data/discovered_companies.json
============================================================

New companies to consider adding:
  1. Astera Labs
  2. Axiado
  3. Celestial AI
  4. d-Matrix
  5. Enfabrica
  6. Etched
  7. Flex Logix
  8. GrAI Matter Labs
  9. Hailo
  10. Lightmatter
  ... and 8 more

✅ Discovery complete!

Next steps:
1. Check 'data/discovered_companies.json' for the full list
2. Research interesting companies
3. Add promising companies to 'scrapers/company_scraper.py'
4. Run the main scraper to start tracking their jobs!

💡 Tip: Run this script monthly to discover new startups and companies!
```

## Integration with Main Scraper

The discovery scraper is separate from the main job scraper:

- **Main scraper** (`scraper_main.py`) - Runs every 6 hours, scrapes known companies
- **Discovery scraper** (`discover_companies.py`) - Run manually/monthly, finds new companies

This separation means:
- Your job scraper stays fast and focused
- You control which companies to add
- You can vet companies before adding them
- Discovery runs don't slow down regular scraping

## Future Enhancements

Potential improvements:
- [ ] Auto-research careers page URLs
- [ ] Score companies by hiring frequency
- [ ] Detect companies that stopped hiring
- [ ] Integration with Crunchbase API
- [ ] Track funding rounds (funded companies hire more)
- [ ] Geographic clustering (find local startups)
- [ ] Technology tag extraction (AI chips, analog, RF, etc.)

---

Happy discovering! May you find that perfect stealth-mode startup with amazing internship programs! 🚀
