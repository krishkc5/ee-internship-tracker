"""
Indeed job scraper
Uses Indeed's RSS feeds and web scraping
"""

import requests
from bs4 import BeautifulSoup
from typing import List
import time
from .base_scraper import BaseScraper, Job


class IndeedScraper(BaseScraper):
    """Scraper for Indeed.com"""

    def __init__(self):
        super().__init__("Indeed")
        self.base_url = "https://www.indeed.com"

    def scrape(self, keywords: List[str], location: str = "United States") -> List[Job]:
        """Scrape Indeed for jobs"""
        self.jobs = []

        for keyword in keywords:
            try:
                jobs = self._scrape_keyword(keyword, location)
                self.jobs.extend(jobs)
                time.sleep(2)  # Be respectful with rate limiting
            except Exception as e:
                print(f"Error scraping Indeed for '{keyword}': {e}")

        return self.jobs

    def _scrape_keyword(self, keyword: str, location: str) -> List[Job]:
        """Scrape jobs for a specific keyword"""
        jobs = []

        # Build search URL
        params = {
            'q': keyword,
            'l': location,
            'jt': 'internship',  # Job type: internship
            'fromage': '7',  # Posted within last 7 days
        }

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        try:
            # Construct URL
            query_string = '&'.join([f"{k}={v.replace(' ', '+')}" for k, v in params.items()])
            url = f"{self.base_url}/jobs?{query_string}"

            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')

            # Find job cards
            job_cards = soup.find_all('div', class_='job_seen_beacon')

            for card in job_cards[:50]:  # Limit to 50 per keyword
                try:
                    # Extract job details
                    title_elem = card.find('h2', class_='jobTitle')
                    if not title_elem:
                        continue

                    title_link = title_elem.find('a')
                    if not title_link:
                        continue

                    title = title_link.get('aria-label', '') or title_link.text.strip()
                    job_url = self.base_url + title_link.get('href', '')

                    company_elem = card.find('span', {'data-testid': 'company-name'})
                    company = company_elem.text.strip() if company_elem else "Unknown"

                    location_elem = card.find('div', {'data-testid': 'text-location'})
                    job_location = location_elem.text.strip() if location_elem else location

                    # Get job description snippet
                    desc_elem = card.find('div', class_='metadata')
                    description = desc_elem.text.strip() if desc_elem else ""

                    job = Job(
                        title=title,
                        company=company,
                        location=job_location,
                        url=job_url,
                        description=description,
                        source="Indeed"
                    )

                    jobs.append(job)

                except Exception as e:
                    print(f"Error parsing job card: {e}")
                    continue

        except Exception as e:
            print(f"Error fetching Indeed jobs for '{keyword}': {e}")

        return jobs
