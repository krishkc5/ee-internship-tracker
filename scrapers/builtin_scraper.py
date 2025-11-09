"""
Built In scraper - Tech job board for startups and companies
"""

import requests
from bs4 import BeautifulSoup
from typing import List
import time
from .base_scraper import BaseScraper, Job


class BuiltInScraper(BaseScraper):
    """Scraper for Built In job boards"""

    def __init__(self):
        super().__init__("BuiltIn")
        self.base_urls = [
            "https://builtin.com",
            "https://www.builtinsf.com",
            "https://www.builtinnyc.com",
            "https://www.builtinboston.com",
            "https://www.builtinaustin.com",
            "https://www.builtinseattle.com"
        ]

    def scrape(self, keywords: List[str], location: str = "United States") -> List[Job]:
        """Scrape Built In for jobs"""
        self.jobs = []

        # Search across different Built In locations
        for base_url in self.base_urls[:3]:  # Limit to 3 locations
            try:
                jobs = self._scrape_builtin(base_url, keywords[0])
                self.jobs.extend(jobs)
                time.sleep(2)
            except Exception as e:
                print(f"Error scraping {base_url}: {e}")

        return self.jobs

    def _scrape_builtin(self, base_url: str, keyword: str) -> List[Job]:
        """Scrape Built In for a specific location"""
        jobs = []

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

        try:
            # Built In job search URL
            search_url = f"{base_url}/jobs/internship"

            response = requests.get(search_url, headers=headers, timeout=10)

            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')

                job_cards = soup.find_all('div', class_='job-item')

                for card in job_cards[:20]:
                    try:
                        title_elem = card.find('h2', class_='job-title')
                        if not title_elem:
                            title_elem = card.find('a', class_='job-title')

                        if not title_elem:
                            continue

                        title = title_elem.text.strip()

                        # Filter for EE/hardware roles
                        title_lower = title.lower()
                        is_relevant = any(kw in title_lower for kw in [
                            'hardware', 'electrical', 'circuit', 'chip', 'silicon',
                            'semiconductor', 'vlsi', 'fpga', 'embedded', 'firmware'
                        ])

                        if not is_relevant:
                            continue

                        link_elem = card.find('a')
                        job_url = base_url + link_elem.get('href', '') if link_elem else ""

                        company_elem = card.find('span', class_='company-name')
                        company = company_elem.text.strip() if company_elem else "Unknown"

                        location_elem = card.find('span', class_='location')
                        job_location = location_elem.text.strip() if location_elem else base_url.split('builtin')[1].replace('.com', '').title()

                        job = Job(
                            title=title,
                            company=company,
                            location=job_location,
                            url=job_url,
                            description="",
                            source="BuiltIn"
                        )

                        jobs.append(job)

                    except Exception as e:
                        continue

        except Exception as e:
            print(f"Error fetching Built In jobs: {e}")

        return jobs
