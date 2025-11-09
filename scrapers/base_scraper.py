"""
Base scraper class that all job board scrapers inherit from
"""

import hashlib
import json
from datetime import datetime
from typing import List, Dict, Optional


class Job:
    """Represents a job posting"""

    def __init__(self, title: str, company: str, location: str, url: str,
                 description: str = "", posted_date: str = "", source: str = ""):
        self.title = title
        self.company = company
        self.location = location
        self.url = url
        self.description = description
        self.posted_date = posted_date or datetime.now().strftime("%Y-%m-%d")
        self.source = source
        self.scraped_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.id = self._generate_id()

    def _generate_id(self) -> str:
        """Generate unique ID based on job details"""
        unique_string = f"{self.title}{self.company}{self.url}"
        return hashlib.md5(unique_string.encode()).hexdigest()

    def to_dict(self) -> Dict:
        """Convert job to dictionary"""
        return {
            "id": self.id,
            "title": self.title,
            "company": self.company,
            "location": self.location,
            "url": self.url,
            "description": self.description,
            "posted_date": self.posted_date,
            "scraped_date": self.scraped_date,
            "source": self.source
        }

    def __repr__(self):
        return f"Job(title={self.title}, company={self.company}, location={self.location})"


class BaseScraper:
    """Base class for all job scrapers"""

    def __init__(self, name: str):
        self.name = name
        self.jobs: List[Job] = []

    def scrape(self, keywords: List[str], location: str = "United States") -> List[Job]:
        """
        Scrape jobs based on keywords and location
        Must be implemented by subclasses
        """
        raise NotImplementedError("Subclasses must implement scrape()")

    def filter_jobs(self, jobs: List[Job], filters: Dict) -> List[Job]:
        """Filter jobs based on criteria"""
        filtered = []

        for job in jobs:
            # Check if job matches filters
            title_lower = job.title.lower()
            desc_lower = job.description.lower()

            # Check for internship keywords
            is_internship = any(keyword in title_lower or keyword in desc_lower
                              for keyword in filters.get("internship_keywords", []))

            # Check for role keywords
            has_role_keyword = any(keyword.lower() in title_lower or keyword.lower() in desc_lower
                                  for keyword in filters.get("role_keywords", []))

            if is_internship and has_role_keyword:
                filtered.append(job)

        return filtered

    def save_jobs(self, filepath: str):
        """Save scraped jobs to JSON file"""
        jobs_dict = [job.to_dict() for job in self.jobs]

        # Load existing jobs if file exists
        try:
            with open(filepath, 'r') as f:
                existing_jobs = json.load(f)
        except FileNotFoundError:
            existing_jobs = []

        # Merge jobs (avoid duplicates)
        existing_ids = {job['id'] for job in existing_jobs}
        new_jobs = [job for job in jobs_dict if job['id'] not in existing_ids]

        all_jobs = existing_jobs + new_jobs

        # Sort by scraped date (most recent first)
        all_jobs.sort(key=lambda x: x['scraped_date'], reverse=True)

        with open(filepath, 'w') as f:
            json.dump(all_jobs, f, indent=2)

        print(f"Saved {len(new_jobs)} new jobs from {self.name} (total: {len(all_jobs)})")
        return len(new_jobs)
