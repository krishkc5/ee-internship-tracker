"""
Glassdoor job scraper
"""

import requests
from bs4 import BeautifulSoup
from typing import List
import time
from .base_scraper import BaseScraper, Job


class GlassdoorScraper(BaseScraper):
    """Scraper for Glassdoor"""

    def __init__(self):
        super().__init__("Glassdoor")
        self.base_url = "https://www.glassdoor.com"

    def scrape(self, keywords: List[str], location: str = "United States") -> List[Job]:
        """Scrape Glassdoor for jobs"""
        self.jobs = []

        for keyword in keywords[:3]:  # Limit keywords
            try:
                jobs = self._scrape_keyword(keyword, location)
                self.jobs.extend(jobs)
                time.sleep(3)  # Be respectful
            except Exception as e:
                print(f"Error scraping Glassdoor for '{keyword}': {e}")

        return self.jobs

    def _scrape_keyword(self, keyword: str, location: str) -> List[Job]:
        """Scrape jobs for a specific keyword"""
        jobs = []

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
        }

        try:
            # Glassdoor search URL
            search_query = f"{keyword} intern"
            params = {
                'sc.keyword': search_query,
                'locT': 'N',
                'locId': '1',
                'jobType': 'internship'
            }

            url = f"{self.base_url}/Job/jobs.htm"
            response = requests.get(url, headers=headers, params=params, timeout=10)

            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')

                # Glassdoor job cards
                job_cards = soup.find_all('li', class_='react-job-listing')

                for card in job_cards[:30]:
                    try:
                        # Extract title
                        title_elem = card.find('a', class_='job-title')
                        if not title_elem:
                            continue

                        title = title_elem.text.strip()
                        job_url = self.base_url + title_elem.get('href', '')

                        # Extract company
                        company_elem = card.find('div', class_='employer-name')
                        company = company_elem.text.strip() if company_elem else "Unknown"

                        # Extract location
                        location_elem = card.find('span', class_='job-location')
                        job_location = location_elem.text.strip() if location_elem else location

                        # Extract description snippet
                        desc_elem = card.find('div', class_='job-description')
                        description = desc_elem.text.strip() if desc_elem else ""

                        job = Job(
                            title=title,
                            company=company,
                            location=job_location,
                            url=job_url,
                            description=description,
                            source="Glassdoor"
                        )

                        jobs.append(job)

                    except Exception as e:
                        continue

        except Exception as e:
            print(f"Error fetching Glassdoor jobs for '{keyword}': {e}")

        return jobs
