"""
Simplify.jobs scraper - Popular for tech internships
"""

import requests
from typing import List
import time
from .base_scraper import BaseScraper, Job


class SimplifyScraper(BaseScraper):
    """Scraper for Simplify.jobs"""

    def __init__(self):
        super().__init__("Simplify")
        self.base_url = "https://simplify.jobs"

    def scrape(self, keywords: List[str], location: str = "United States") -> List[Job]:
        """Scrape Simplify for jobs"""
        self.jobs = []

        try:
            # Simplify has a public API/list of internships
            # They maintain a GitHub repo with internship listings
            api_url = "https://raw.githubusercontent.com/SimplifyJobs/Summer2025-Internships/dev/.github/scripts/listings.json"

            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }

            response = requests.get(api_url, headers=headers, timeout=10)

            if response.status_code == 200:
                listings = response.json()

                for listing in listings[:100]:  # Limit to 100
                    try:
                        company = listing.get('company_name', 'Unknown')
                        title = listing.get('title', '')
                        locations = listing.get('locations', [])
                        url = listing.get('url', '')

                        # Filter for EE/hardware related roles
                        title_lower = title.lower()
                        is_relevant = any(keyword in title_lower for keyword in [
                            'hardware', 'electrical', 'circuit', 'analog', 'digital',
                            'semiconductor', 'vlsi', 'fpga', 'embedded', 'firmware'
                        ])

                        if is_relevant:
                            job = Job(
                                title=title,
                                company=company,
                                location=', '.join(locations) if locations else location,
                                url=url,
                                description="",
                                source="Simplify"
                            )
                            self.jobs.append(job)

                    except Exception as e:
                        continue

        except Exception as e:
            print(f"Error fetching Simplify jobs: {e}")

        return self.jobs
