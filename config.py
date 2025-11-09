"""
Configuration file for the job scraper
"""

# Job search keywords
JOB_KEYWORDS = [
    "electrical engineering",
    "computer engineering",
    "hardware engineering",
    "circuit design",
    "analog design",
    "digital design",
    "VLSI",
    "FPGA",
    "semiconductor",
    "PCB design",
    "embedded systems",
    "data science"
]

# Specific role keywords for filtering
ROLE_KEYWORDS = [
    "circuit", "analog", "digital", "VLSI", "ASIC", "FPGA",
    "hardware", "semiconductor", "RF", "mixed-signal",
    "embedded", "firmware", "PCB", "layout",
    "chip design", "silicon", "verification",
    "data science", "machine learning", "data engineer"
]

# Internship keywords
INTERNSHIP_KEYWORDS = [
    "intern", "internship", "summer 2026", "co-op", "coop"
]

# Location preferences (can be modified)
LOCATIONS = [
    "United States",
    "Remote",
    "California",
    "Texas",
    "Massachusetts",
    "New York",
    "Washington"
]

# Companies to prioritize (optional - can add specific companies you're interested in)
PRIORITY_COMPANIES = [
    # Semiconductor Companies
    "Intel", "AMD", "NVIDIA", "Qualcomm", "Broadcom", "Micron",
    "Texas Instruments", "Analog Devices", "Microchip", "NXP",
    "Applied Materials", "TSMC", "Samsung Semiconductor", "Marvell",
    "Synopsys", "Cadence", "Xilinx", "KLA", "GlobalFoundries",

    # Tech Giants
    "Apple", "Google", "Microsoft", "Amazon", "Meta",
    "Tesla", "IBM", "Oracle", "Cisco", "HP",

    # Aerospace & Defense
    "SpaceX", "Blue Origin", "Northrop Grumman", "Lockheed Martin",
    "Raytheon", "Boeing", "NASA", "JPL", "Honeywell", "Collins Aerospace",

    # Hardware & Embedded
    "Bosch", "Continental", "Delphi", "Aptiv", "Garmin",
    "Keysight", "Teradyne", "National Instruments"
]

# Scraping settings
SCRAPE_INTERVAL_HOURS = 6  # How often to scrape (for local testing)
MAX_JOBS_PER_SOURCE = 100  # Maximum jobs to fetch per source per run
