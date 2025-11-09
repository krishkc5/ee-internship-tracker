# Job Scraper Sources

This document lists all the job sources that the scraper monitors for EE/CompE/Hardware internships.

## Job Board Scrapers (7 sources)

### 1. Indeed
- **Coverage**: General job board with wide reach
- **Filters**: Internships in EE, hardware, circuit design, semiconductor
- **Update Frequency**: Every 6 hours
- **Typical Results**: 20-50 jobs per run

### 2. LinkedIn
- **Coverage**: Professional network with extensive company listings
- **Filters**: Internship positions in hardware/electrical engineering
- **Update Frequency**: Every 6 hours
- **Typical Results**: 30-50 jobs per run

### 3. Glassdoor
- **Coverage**: Company reviews + job listings
- **Filters**: EE/hardware internships
- **Update Frequency**: Every 6 hours
- **Typical Results**: 15-30 jobs per run

### 4. Simplify.jobs
- **Coverage**: Tech internship aggregator (uses their public GitHub repo)
- **Filters**: Hardware, electrical, circuit, analog, digital, semiconductor, VLSI, FPGA
- **Update Frequency**: Every 6 hours
- **Typical Results**: 10-20 relevant jobs
- **Note**: Excellent source for Summer 2026 internships

### 5. Handshake
- **Coverage**: College recruiting platform
- **Filters**: Internship positions
- **Update Frequency**: Every 6 hours
- **Typical Results**: 10-30 jobs per run

### 6. Built In
- **Coverage**: Tech startup and company job boards across multiple cities
- **Locations Monitored**: SF, NYC, Boston, Austin, Seattle, general
- **Filters**: Hardware/EE internships
- **Update Frequency**: Every 6 hours
- **Typical Results**: 5-15 jobs per run

### 7. Company Career Pages
- **Coverage**: Direct scraping of company career portals
- **Companies Monitored**: 15+ (see below)
- **Update Frequency**: Every 6 hours
- **Typical Results**: 10-30 jobs per run

## Company Career Pages Monitored (15+ companies)

### Semiconductor Companies
1. **Intel** - jobs.intel.com
2. **AMD** - careers.amd.com
3. **NVIDIA** - nvidia.wd5.myworkdayjobs.com
4. **Qualcomm** - careers.qualcomm.com
5. **Texas Instruments** - careers.ti.com
6. **Analog Devices** - careers.analog.com
7. **Broadcom** - broadcom.wd3.myworkdayjobs.com
8. **Micron** - careers.micron.com
9. **Applied Materials** - careers.appliedmaterials.com
10. **TSMC** - careers.tsmc.com
11. **NXP** - nxp.wd3.myworkdayjobs.com
12. **Marvell** - marvell.wd1.myworkdayjobs.com

### EDA & Design Tools
13. **Synopsys** - sjobs.brassring.com
14. **Cadence** - cadence.wd1.myworkdayjobs.com
15. **Xilinx** (now AMD) - careers.amd.com

## Priority Company List (40+ companies)

The scraper prioritizes and highlights positions from these companies:

### Semiconductor
- Intel, AMD, NVIDIA, Qualcomm, Broadcom, Micron
- Texas Instruments, Analog Devices, Microchip, NXP
- Applied Materials, TSMC, Samsung Semiconductor, Marvell
- Synopsys, Cadence, Xilinx, KLA, GlobalFoundries

### Tech Giants
- Apple, Google, Microsoft, Amazon, Meta
- Tesla, IBM, Oracle, Cisco, HP

### Aerospace & Defense
- SpaceX, Blue Origin, Northrop Grumman, Lockheed Martin
- Raytheon, Boeing, NASA, JPL, Honeywell, Collins Aerospace

### Hardware & Embedded
- Bosch, Continental, Delphi, Aptiv, Garmin
- Keysight, Teradyne, National Instruments

## Target Roles

The scraper specifically looks for internships in:

- Circuit Design (Analog, Digital, Mixed-Signal)
- VLSI/ASIC Design & Verification
- FPGA Development
- Hardware Engineering
- Semiconductor/Silicon Engineering
- Embedded Systems & Firmware
- PCB Design & Layout
- RF Engineering
- Data Science & Machine Learning (related to hardware)

## Keywords Monitored

### Primary Search Keywords
- electrical engineering
- computer engineering
- hardware engineering
- circuit design
- analog design
- digital design
- VLSI
- FPGA
- semiconductor
- PCB design
- embedded systems
- data science

### Role Filter Keywords
- circuit, analog, digital
- VLSI, ASIC, FPGA
- hardware, semiconductor
- RF, mixed-signal
- embedded, firmware
- PCB, layout
- chip design, silicon
- verification

## Total Coverage

**Estimated job postings monitored per cycle**: 150-250 positions

**Update frequency**: Every 6 hours (4 times per day)

**Annual coverage**: ~200,000+ job postings scanned

**Deduplication**: Automatic removal of duplicate postings across sources

## Notes for Customization

Want to add more sources? Edit:
- `scrapers/` - Add new scraper classes
- `scraper_main.py` - Add to scrapers list
- `config.py` - Update keywords and companies

The system is designed to be easily extensible!
