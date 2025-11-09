"""
Simple test script to verify the scraper setup works
"""

import sys
import os

def test_imports():
    """Test that all modules can be imported"""
    print("Testing imports...")
    try:
        from scrapers import BaseScraper, Job, IndeedScraper, LinkedInScraper
        import config
        print("✓ All imports successful")
        return True
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False

def test_config():
    """Test that configuration is valid"""
    print("\nTesting configuration...")
    try:
        import config

        assert len(config.JOB_KEYWORDS) > 0, "No job keywords defined"
        assert len(config.ROLE_KEYWORDS) > 0, "No role keywords defined"
        assert len(config.INTERNSHIP_KEYWORDS) > 0, "No internship keywords defined"

        print(f"✓ Configuration valid")
        print(f"  - {len(config.JOB_KEYWORDS)} job keywords")
        print(f"  - {len(config.ROLE_KEYWORDS)} role keywords")
        print(f"  - {len(config.INTERNSHIP_KEYWORDS)} internship keywords")
        return True
    except Exception as e:
        print(f"✗ Configuration error: {e}")
        return False

def test_scrapers():
    """Test that scrapers can be initialized"""
    print("\nTesting scrapers...")
    try:
        from scrapers import IndeedScraper, LinkedInScraper

        indeed = IndeedScraper()
        linkedin = LinkedInScraper()

        assert indeed.name == "Indeed", "Indeed scraper name incorrect"
        assert linkedin.name == "LinkedIn", "LinkedIn scraper name incorrect"

        print(f"✓ Scrapers initialized successfully")
        print(f"  - {indeed.name}")
        print(f"  - {linkedin.name}")
        return True
    except Exception as e:
        print(f"✗ Scraper error: {e}")
        return False

def test_job_class():
    """Test Job class functionality"""
    print("\nTesting Job class...")
    try:
        from scrapers.base_scraper import Job

        job = Job(
            title="Hardware Engineering Intern",
            company="Test Corp",
            location="San Francisco, CA",
            url="https://example.com/job/123",
            description="Test description",
            source="Test"
        )

        assert job.title == "Hardware Engineering Intern"
        assert job.company == "Test Corp"
        assert job.id is not None, "Job ID not generated"

        job_dict = job.to_dict()
        assert "id" in job_dict
        assert "title" in job_dict
        assert "company" in job_dict

        print(f"✓ Job class working correctly")
        print(f"  - Job ID: {job.id[:8]}...")
        print(f"  - Title: {job.title}")
        return True
    except Exception as e:
        print(f"✗ Job class error: {e}")
        return False

def test_data_directory():
    """Test that data directory can be created"""
    print("\nTesting data directory...")
    try:
        os.makedirs('data', exist_ok=True)
        assert os.path.isdir('data'), "Data directory not created"
        print(f"✓ Data directory ready")
        return True
    except Exception as e:
        print(f"✗ Data directory error: {e}")
        return False

def main():
    """Run all tests"""
    print("="*50)
    print("Running EE Internship Scraper Tests")
    print("="*50)

    tests = [
        test_imports,
        test_config,
        test_scrapers,
        test_job_class,
        test_data_directory,
    ]

    results = [test() for test in tests]

    print("\n" + "="*50)
    print(f"Test Results: {sum(results)}/{len(results)} passed")
    print("="*50)

    if all(results):
        print("\n✓ All tests passed! Your scraper is ready to run.")
        print("\nNext steps:")
        print("1. Run: python scraper_main.py")
        print("2. Push to GitHub")
        print("3. Enable GitHub Actions and Pages")
        return 0
    else:
        print("\n✗ Some tests failed. Please check the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
