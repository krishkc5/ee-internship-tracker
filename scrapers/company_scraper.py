"""
Company-specific career page scraper
Targets major semiconductor and hardware companies
"""

import requests
from bs4 import BeautifulSoup
from typing import List, Dict
import time
from .base_scraper import BaseScraper, Job


class CompanyScraper(BaseScraper):
    """Scraper for company career pages"""

    def __init__(self):
        super().__init__("Company Careers")

        # Major companies with EE/hardware internships
        self.companies = {
            # Large Semiconductor Companies
            "Intel": {
                "url": "https://jobs.intel.com/en/search-jobs",
                "search_params": {"k": "intern hardware", "locationsearch": "United States"}
            },
            "AMD": {
                "url": "https://careers.amd.com/careers-home/jobs",
                "search_params": {"keywords": "intern hardware"}
            },
            "NVIDIA": {
                "url": "https://nvidia.wd5.myworkdayjobs.com/NVIDIAExternalCareerSite",
                "search_params": {"q": "intern hardware"}
            },
            "Qualcomm": {
                "url": "https://careers.qualcomm.com/careers/jobs",
                "search_params": {"keywords": "intern hardware"}
            },
            "Texas Instruments": {
                "url": "https://careers.ti.com/search-jobs",
                "search_params": {"k": "intern hardware"}
            },
            "Analog Devices": {
                "url": "https://careers.analog.com/search-jobs",
                "search_params": {"k": "intern circuit"}
            },
            "Broadcom": {
                "url": "https://broadcom.wd3.myworkdayjobs.com/External",
                "search_params": {"q": "intern hardware"}
            },
            "Micron": {
                "url": "https://careers.micron.com/careers/SearchJobs",
                "search_params": {"10000-10481": "[10000-10481]"}  # Internship filter
            },
            "Applied Materials": {
                "url": "https://careers.appliedmaterials.com/search-jobs",
                "search_params": {"k": "intern engineering"}
            },
            "TSMC": {
                "url": "https://careers.tsmc.com/careers/SearchJobs",
                "search_params": {"10000-8324": "[10000-8324]"}  # Internship filter
            },
            "NXP": {
                "url": "https://nxp.wd3.myworkdayjobs.com/careers",
                "search_params": {"q": "intern hardware"}
            },
            "Marvell": {
                "url": "https://marvell.wd1.myworkdayjobs.com/MarvellCareers",
                "search_params": {"q": "intern hardware"}
            },
            "Xilinx": {  # Now part of AMD
                "url": "https://careers.amd.com/careers-home/jobs",
                "search_params": {"keywords": "intern fpga"}
            },

            # EDA & Design Tools
            "Synopsys": {
                "url": "https://sjobs.brassring.com/TGnewUI/Search/Home/Home?partnerid=25235&siteid=5359",
                "search_params": {"keywords": "intern"}
            },
            "Cadence": {
                "url": "https://cadence.wd1.myworkdayjobs.com/External_Careers",
                "search_params": {"q": "intern"}
            },

            # Smaller/Emerging Semiconductor Companies
            "Cirrus Logic": {
                "url": "https://careers.cirrus.com/search-jobs",
                "search_params": {"k": "intern"}
            },
            "SiFive": {
                "url": "https://boards.greenhouse.io/sifive",
                "search_params": {}
            },
            "Cerebras": {
                "url": "https://cerebras.net/careers/",
                "search_params": {}
            },
            "Groq": {
                "url": "https://groq.com/careers/",
                "search_params": {}
            },
            "Astera Labs": {
                "url": "https://jobs.lever.co/astera-labs",
                "search_params": {}
            },
            "Rebellions": {
                "url": "https://rebellions.ai/en/career/",
                "search_params": {}
            },
            "Tenstorrent": {
                "url": "https://tenstorrent.com/careers/",
                "search_params": {}
            },
            "Rivos": {
                "url": "https://boards.greenhouse.io/rivos",
                "search_params": {}
            },
            "SambaNova": {
                "url": "https://sambanova.ai/careers/",
                "search_params": {}
            },
            "Alphawave": {
                "url": "https://awaveip.com/careers/",
                "search_params": {}
            }
        }

    def scrape(self, keywords: List[str], location: str = "United States") -> List[Job]:
        """Scrape company career pages"""
        self.jobs = []

        for company_name, company_info in self.companies.items():
            try:
                print(f"Scraping {company_name}...")
                jobs = self._scrape_company(company_name, company_info)
                self.jobs.extend(jobs)
                time.sleep(3)  # Be respectful with rate limiting
            except Exception as e:
                print(f"Error scraping {company_name}: {e}")

        return self.jobs

    def _scrape_company(self, company_name: str, company_info: Dict) -> List[Job]:
        """Scrape a specific company's career page"""
        jobs = []

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        try:
            url = company_info["url"]

            response = requests.get(url, headers=headers, params=company_info.get("search_params", {}), timeout=15)

            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')

                # Generic job card selectors (adapt per company)
                job_cards = (
                    soup.find_all('div', class_='job-listing') or
                    soup.find_all('div', class_='job-card') or
                    soup.find_all('li', class_='job') or
                    soup.find_all('tr', class_='job-row') or
                    soup.find_all('article')
                )

                for card in job_cards[:20]:  # Limit to 20 per company
                    try:
                        # Try to extract title
                        title_elem = (
                            card.find('h2') or
                            card.find('h3') or
                            card.find('a', class_='job-title') or
                            card.find('span', class_='title')
                        )

                        if not title_elem:
                            continue

                        title = title_elem.text.strip()

                        # Filter for internships and relevant roles
                        title_lower = title.lower()
                        if 'intern' not in title_lower:
                            continue

                        is_relevant = any(kw in title_lower for kw in [
                            'hardware', 'electrical', 'circuit', 'analog', 'digital',
                            'semiconductor', 'vlsi', 'asic', 'fpga', 'chip', 'silicon',
                            'embedded', 'firmware', 'pcb', 'rf', 'mixed-signal'
                        ])

                        if not is_relevant:
                            continue

                        # Extract URL
                        link_elem = card.find('a')
                        job_url = link_elem.get('href', '') if link_elem else ""
                        if job_url and not job_url.startswith('http'):
                            # Convert relative URL to absolute
                            base = url.split('/search')[0] if '/search' in url else url
                            job_url = base + job_url

                        # Extract location
                        location_elem = (
                            card.find('span', class_='location') or
                            card.find('div', class_='location') or
                            card.find('span', class_='job-location')
                        )
                        job_location = location_elem.text.strip() if location_elem else "United States"

                        # Extract description if available
                        desc_elem = card.find('p', class_='description')
                        description = desc_elem.text.strip() if desc_elem else ""

                        job = Job(
                            title=title,
                            company=company_name,
                            location=job_location,
                            url=job_url,
                            description=description,
                            source=f"{company_name} Careers"
                        )

                        jobs.append(job)

                    except Exception as e:
                        continue

        except Exception as e:
            print(f"Error fetching {company_name} jobs: {e}")

        return jobs
