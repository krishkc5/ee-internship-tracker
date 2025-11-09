"""
Handshake scraper - Popular for college recruiting
Note: Handshake requires login, so this scraper uses their public job board
"""

import requests
from bs4 import BeautifulSoup
from typing import List
import time
from .base_scraper import BaseScraper, Job


class HandshakeScraper(BaseScraper):
    """Scraper for Handshake public job board"""

    def __init__(self):
        super().__init__("Handshake")
        self.base_url = "https://joinhandshake.com"

    def scrape(self, keywords: List[str], location: str = "United States") -> List[Job]:
        """Scrape Handshake for jobs"""
        self.jobs = []

        for keyword in keywords[:3]:  # Limit keywords
            try:
                jobs = self._scrape_keyword(keyword, location)
                self.jobs.extend(jobs)
                time.sleep(2)
            except Exception as e:
                print(f"Error scraping Handshake for '{keyword}': {e}")

        return self.jobs

    def _scrape_keyword(self, keyword: str, location: str) -> List[Job]:
        """Scrape jobs for a specific keyword"""
        jobs = []

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

        try:
            # Handshake public job search
            params = {
                'query': keyword,
                'location': location,
                'job_type': 'internship'
            }

            url = f"{self.base_url}/jobs"
            response = requests.get(url, headers=headers, params=params, timeout=10)

            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')

                # Note: Handshake structure may vary, this is a basic implementation
                job_cards = soup.find_all('div', class_='job-card')

                for card in job_cards[:30]:
                    try:
                        title_elem = card.find('h3')
                        if not title_elem:
                            continue

                        title = title_elem.text.strip()
                        job_url = self.base_url + card.find('a').get('href', '')

                        company_elem = card.find('div', class_='company-name')
                        company = company_elem.text.strip() if company_elem else "Unknown"

                        location_elem = card.find('div', class_='location')
                        job_location = location_elem.text.strip() if location_elem else location

                        job = Job(
                            title=title,
                            company=company,
                            location=job_location,
                            url=job_url,
                            description="",
                            source="Handshake"
                        )

                        jobs.append(job)

                    except Exception as e:
                        continue

        except Exception as e:
            print(f"Error fetching Handshake jobs for '{keyword}': {e}")

        return jobs
