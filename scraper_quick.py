"""
Quick scraper - Uses only reliable sources to get you jobs FAST
Run this to quickly populate your site while the main scraper is being debugged
"""

import json
import os
from datetime import datetime
from scrapers import SimplifyScraper
from config import JOB_KEYWORDS, ROLE_KEYWORDS, INTERNSHIP_KEYWORDS


def main():
    """Run quick scraper with only reliable sources"""
    print(f"Starting QUICK job scraper at {datetime.now()}")
    print("Using only fast, reliable sources...")

    # Create data directory
    os.makedirs('data', exist_ok=True)

    # Use only Simplify - it's fast and reliable (uses GitHub API)
    scraper = SimplifyScraper()

    print(f"\n{'='*50}")
    print(f"Running {scraper.name} scraper...")
    print(f"{'='*50}")

    try:
        # Scrape jobs
        jobs = scraper.scrape(JOB_KEYWORDS, location="United States")

        # Filter jobs
        filters = {
            "internship_keywords": INTERNSHIP_KEYWORDS,
            "role_keywords": ROLE_KEYWORDS
        }
        filtered_jobs = scraper.filter_jobs(jobs, filters)

        print(f"Found {len(jobs)} total jobs, {len(filtered_jobs)} after filtering")

        # Save jobs
        scraper.jobs = filtered_jobs[:100]

        # Save to file
        scraper_file = f"data/jobs_{scraper.name.lower()}.json"
        new_count = scraper.save_jobs(scraper_file)

        # Save aggregated
        all_jobs = [job.to_dict() for job in scraper.jobs]
        save_aggregated_jobs(all_jobs)

        print(f"\n{'='*50}")
        print(f"Quick scraping completed at {datetime.now()}")
        print(f"Total jobs found: {len(filtered_jobs)}")
        print(f"New jobs: {new_count}")
        print(f"{'='*50}")

        print("\nNext: Commit and push to GitHub to see jobs on your site!")

    except Exception as e:
        print(f"Error running {scraper.name} scraper: {e}")
        import traceback
        traceback.print_exc()


def save_aggregated_jobs(new_jobs):
    """Save all jobs to a single aggregated file"""
    filepath = "data/jobs_all.json"

    # Load existing jobs
    try:
        with open(filepath, 'r') as f:
            existing_jobs = json.load(f)
    except FileNotFoundError:
        existing_jobs = []

    # Merge jobs (avoid duplicates by ID)
    existing_ids = {job['id'] for job in existing_jobs}
    unique_new_jobs = [job for job in new_jobs if job['id'] not in existing_ids]

    all_jobs = existing_jobs + unique_new_jobs

    # Sort by scraped date (most recent first)
    all_jobs.sort(key=lambda x: x['scraped_date'], reverse=True)

    # Save to file
    with open(filepath, 'w') as f:
        json.dump(all_jobs, f, indent=2)

    print(f"\nSaved aggregated jobs to {filepath}")
    print(f"Total jobs in database: {len(all_jobs)}")


if __name__ == "__main__":
    main()
