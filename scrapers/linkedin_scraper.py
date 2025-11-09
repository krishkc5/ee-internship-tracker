"""
LinkedIn job scraper
Note: LinkedIn heavily restricts scraping. This uses their public job search.
For production, consider using LinkedIn's official API if available.
"""

import requests
from bs4 import BeautifulSoup
from typing import List
import time
from .base_scraper import BaseScraper, Job


class LinkedInScraper(BaseScraper):
    """Scraper for LinkedIn Jobs"""

    def __init__(self):
        super().__init__("LinkedIn")
        self.base_url = "https://www.linkedin.com"

    def scrape(self, keywords: List[str], location: str = "United States") -> List[Job]:
        """Scrape LinkedIn for jobs"""
        self.jobs = []

        for keyword in keywords:
            try:
                jobs = self._scrape_keyword(keyword, location)
                self.jobs.extend(jobs)
                time.sleep(3)  # Be extra respectful with LinkedIn
            except Exception as e:
                print(f"Error scraping LinkedIn for '{keyword}': {e}")

        return self.jobs

    def _scrape_keyword(self, keyword: str, location: str) -> List[Job]:
        """Scrape jobs for a specific keyword"""
        jobs = []

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        try:
            # LinkedIn public job search URL
            params = {
                'keywords': keyword,
                'location': location,
                'f_JT': 'I',  # Internship
                'f_TPR': 'r604800',  # Past week
                'position': '1',
                'pageNum': '0'
            }

            query_string = '&'.join([f"{k}={v.replace(' ', '%20')}" for k, v in params.items()])
            url = f"{self.base_url}/jobs/search?{query_string}"

            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')

            # Find job cards (LinkedIn's structure may change)
            job_cards = soup.find_all('div', class_='base-card')

            for card in job_cards[:50]:  # Limit to 50 per keyword
                try:
                    # Extract job details
                    title_elem = card.find('h3', class_='base-search-card__title')
                    if not title_elem:
                        continue

                    title = title_elem.text.strip()

                    link_elem = card.find('a', class_='base-card__full-link')
                    if not link_elem:
                        continue

                    job_url = link_elem.get('href', '')

                    company_elem = card.find('h4', class_='base-search-card__subtitle')
                    company = company_elem.text.strip() if company_elem else "Unknown"

                    location_elem = card.find('span', class_='job-search-card__location')
                    job_location = location_elem.text.strip() if location_elem else location

                    # Get posted date if available
                    date_elem = card.find('time')
                    posted_date = date_elem.get('datetime', '') if date_elem else ""

                    job = Job(
                        title=title,
                        company=company,
                        location=job_location,
                        url=job_url,
                        description="",  # LinkedIn doesn't show description in search results
                        posted_date=posted_date,
                        source="LinkedIn"
                    )

                    jobs.append(job)

                except Exception as e:
                    print(f"Error parsing LinkedIn job card: {e}")
                    continue

        except Exception as e:
            print(f"Error fetching LinkedIn jobs for '{keyword}': {e}")

        return jobs
