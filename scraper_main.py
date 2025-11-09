"""
Main scraper script that coordinates all job scrapers
"""

import json
import os
from datetime import datetime
from scrapers import IndeedScraper, LinkedInScraper
from config import JOB_KEYWORDS, ROLE_KEYWORDS, INTERNSHIP_KEYWORDS, MAX_JOBS_PER_SOURCE


def main():
    """Run all scrapers and aggregate results"""
    print(f"Starting job scraper at {datetime.now()}")

    # Create data directory if it doesn't exist
    os.makedirs('data', exist_ok=True)

    # Initialize scrapers
    scrapers = [
        IndeedScraper(),
        LinkedInScraper(),
    ]

    all_jobs = []
    total_new_jobs = 0

    # Run each scraper
    for scraper in scrapers:
        print(f"\n{'='*50}")
        print(f"Running {scraper.name} scraper...")
        print(f"{'='*50}")

        try:
            # Scrape jobs
            jobs = scraper.scrape(JOB_KEYWORDS[:3], location="United States")  # Limit keywords to avoid rate limits

            # Filter jobs
            filters = {
                "internship_keywords": INTERNSHIP_KEYWORDS,
                "role_keywords": ROLE_KEYWORDS
            }
            filtered_jobs = scraper.filter_jobs(jobs, filters)

            print(f"Found {len(jobs)} total jobs, {len(filtered_jobs)} after filtering")

            # Update scraper's jobs with filtered results
            scraper.jobs = filtered_jobs[:MAX_JOBS_PER_SOURCE]

            # Save to individual scraper file
            scraper_file = f"data/jobs_{scraper.name.lower()}.json"
            new_count = scraper.save_jobs(scraper_file)
            total_new_jobs += new_count

            all_jobs.extend([job.to_dict() for job in scraper.jobs])

        except Exception as e:
            print(f"Error running {scraper.name} scraper: {e}")

    # Save aggregated results
    save_aggregated_jobs(all_jobs)

    print(f"\n{'='*50}")
    print(f"Scraping completed at {datetime.now()}")
    print(f"Total new jobs found: {total_new_jobs}")
    print(f"{'='*50}")


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
