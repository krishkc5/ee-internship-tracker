"""
Company Discovery Scraper - Meta scraper that finds companies to scrape!
This scraper searches job boards and discovers new companies posting EE/hardware internships,
then you can add them to the main company scraper.
"""

import requests
from bs4 import BeautifulSoup
from typing import List, Set, Dict
import json
import time
from .base_scraper import BaseScraper, Job


class CompanyDiscoveryScraper(BaseScraper):
    """Meta-scraper that discovers companies posting EE/hardware internships"""

    def __init__(self):
        super().__init__("Company Discovery")
        self.discovered_companies: Set[str] = set()

    def scrape(self, keywords: List[str], location: str = "United States") -> List[Job]:
        """
        Scrape job boards to discover companies hiring for EE/hardware roles
        Returns jobs AND saves discovered companies to a file
        """
        self.jobs = []
        self.discovered_companies = set()

        # Scrape different sources to find companies
        self._discover_from_linkedin(keywords)
        self._discover_from_indeed(keywords)
        self._discover_from_builtin()
        self._discover_from_ycombinator()

        # Save discovered companies
        self._save_discovered_companies()

        return self.jobs

    def _discover_from_linkedin(self, keywords: List[str]):
        """Discover companies from LinkedIn job postings"""
        print("Discovering companies from LinkedIn...")

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

        try:
            # Search for hardware/semiconductor internships
            url = "https://www.linkedin.com/jobs/search"
            params = {
                'keywords': 'hardware intern OR semiconductor intern OR circuit design intern',
                'location': 'United States',
                'f_JT': 'I',  # Internship
                'f_TPR': 'r2592000',  # Past month
            }

            response = requests.get(url, headers=headers, params=params, timeout=10)

            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                company_elements = soup.find_all('h4', class_='base-search-card__subtitle')

                for elem in company_elements:
                    company_name = elem.text.strip()
                    if company_name and len(company_name) < 100:  # Filter out bad data
                        self.discovered_companies.add(company_name)

                print(f"Found {len(company_elements)} companies on LinkedIn")

        except Exception as e:
            print(f"Error discovering from LinkedIn: {e}")

        time.sleep(2)

    def _discover_from_indeed(self, keywords: List[str]):
        """Discover companies from Indeed job postings"""
        print("Discovering companies from Indeed...")

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

        try:
            url = "https://www.indeed.com/jobs"
            params = {
                'q': 'hardware engineer intern OR semiconductor intern',
                'l': 'United States',
                'jt': 'internship',
                'fromage': '30',  # Last 30 days
            }

            response = requests.get(url, headers=headers, params=params, timeout=10)

            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                company_elements = soup.find_all('span', {'data-testid': 'company-name'})

                for elem in company_elements:
                    company_name = elem.text.strip()
                    if company_name and len(company_name) < 100:
                        self.discovered_companies.add(company_name)

                print(f"Found {len(company_elements)} companies on Indeed")

        except Exception as e:
            print(f"Error discovering from Indeed: {e}")

        time.sleep(2)

    def _discover_from_builtin(self):
        """Discover semiconductor/hardware startups from Built In"""
        print("Discovering companies from Built In...")

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

        try:
            # Built In has curated lists of semiconductor/hardware companies
            urls = [
                "https://builtin.com/hardware",
                "https://builtin.com/semiconductors",
                "https://www.builtinsf.com/companies/type/hardware-companies",
            ]

            for url in urls:
                try:
                    response = requests.get(url, headers=headers, timeout=10)

                    if response.status_code == 200:
                        soup = BeautifulSoup(response.content, 'html.parser')
                        # Built In company listings
                        company_links = soup.find_all('a', class_='company-title')

                        for link in company_links:
                            company_name = link.text.strip()
                            if company_name and len(company_name) < 100:
                                self.discovered_companies.add(company_name)

                    time.sleep(2)

                except Exception as e:
                    print(f"Error with {url}: {e}")
                    continue

            print(f"Discovered companies from Built In")

        except Exception as e:
            print(f"Error discovering from Built In: {e}")

    def _discover_from_ycombinator(self):
        """Discover hardware/semiconductor startups from Y Combinator companies"""
        print("Discovering companies from Y Combinator...")

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

        try:
            # YC companies directory
            url = "https://www.ycombinator.com/companies"
            params = {
                'industry': 'Hardware',
                'tags': 'semiconductors'
            }

            response = requests.get(url, headers=headers, params=params, timeout=10)

            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')

                # YC company cards
                company_cards = soup.find_all('a', class_='_company_86jzd_338')

                for card in company_cards:
                    company_name_elem = card.find('span', class_='_coName_86jzd_453')
                    if company_name_elem:
                        company_name = company_name_elem.text.strip()
                        if company_name and len(company_name) < 100:
                            self.discovered_companies.add(company_name)

                print(f"Found {len(company_cards)} YC companies")

        except Exception as e:
            print(f"Error discovering from Y Combinator: {e}")

    def _save_discovered_companies(self):
        """Save discovered companies to a JSON file for review"""
        if not self.discovered_companies:
            print("No companies discovered")
            return

        # Load existing discoveries
        try:
            with open('data/discovered_companies.json', 'r') as f:
                existing = json.load(f)
        except FileNotFoundError:
            existing = {
                "companies": [],
                "last_updated": ""
            }

        # Add new companies
        existing_set = set(existing.get("companies", []))
        new_companies = self.discovered_companies - existing_set
        all_companies = sorted(list(existing_set.union(self.discovered_companies)))

        # Save
        import datetime
        discovery_data = {
            "companies": all_companies,
            "total_count": len(all_companies),
            "new_this_run": len(new_companies),
            "last_updated": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "new_companies_list": sorted(list(new_companies))
        }

        with open('data/discovered_companies.json', 'w') as f:
            json.dump(discovery_data, f, indent=2)

        print(f"\n{'='*60}")
        print(f"Company Discovery Summary:")
        print(f"  Total companies discovered: {len(all_companies)}")
        print(f"  New companies this run: {len(new_companies)}")
        print(f"  Saved to: data/discovered_companies.json")
        print(f"{'='*60}")

        if new_companies:
            print("\nNew companies to consider adding:")
            for i, company in enumerate(sorted(list(new_companies))[:20], 1):
                print(f"  {i}. {company}")

            if len(new_companies) > 20:
                print(f"  ... and {len(new_companies) - 20} more")

    def get_company_info(self, company_name: str) -> Dict:
        """
        Research a discovered company to get their careers page URL
        This can be called manually to research companies
        """
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

        # Google search for careers page
        try:
            query = f"{company_name} careers internship hardware"
            search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"

            response = requests.get(search_url, headers=headers, timeout=10)

            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')

                # Try to find careers page link
                links = soup.find_all('a')
                for link in links:
                    href = link.get('href', '')
                    if 'careers' in href.lower() or 'jobs' in href.lower():
                        return {
                            "name": company_name,
                            "careers_url": href,
                            "found": True
                        }

        except Exception as e:
            print(f"Error researching {company_name}: {e}")

        return {
            "name": company_name,
            "careers_url": "",
            "found": False
        }
