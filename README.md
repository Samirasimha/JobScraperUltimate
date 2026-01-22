# JobScraperUltimate

An automated job scraping tool that collects job listings from LinkedIn, Indeed, and Skillsire, filters them by role keywords, removes duplicates, and saves results to CSV files with optional email notifications.

## Features

- **Multi-Platform Scraping**: Scrapes jobs from LinkedIn, Indeed, and Skillsire
- **Smart Filtering**: Filter jobs by role keywords (e.g., "Backend", "Frontend", "Developer")
- **Deduplication**: Automatically removes duplicate job postings
- **CSV Export**: Saves results in organized CSV files with timestamps
- **Email Notifications**: Optional email delivery with CSV attachments
- **Continuous Operation**: Runs on a configurable schedule to catch new postings
- **Rate Limiting**: Built-in delays to avoid IP blocking

## Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

## Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/Samirasimha/JobScraperUltimate.git
cd JobScraperUltimate
```

### Step 2: Install Dependencies

Install all required packages using the provided requirements file:

```bash
pip install -r requirements.txt
```

This will install:
- `python-jobspy` - Job scraping library for LinkedIn and Indeed
- `pandas` - Data manipulation and CSV handling
- `requests` - HTTP library for Skillsire API calls

## Configuration

Open [JobScraperUltimate.py](JobScraperUltimate.py) and configure the settings at the top of the file:

### Basic Settings

```python
# How many hours back to search for jobs (first run only)
hours = 1

# Time in seconds to wait between scraping sessions
# Recommended: 600-3600 (10 minutes to 1 hour)
sleep_time = 10

# Job portals to scrape (remove any you don't want)
scrape_from = ["linkedin", "indeed", "skillsire"]

# Your job search query
search_term = "software engineer"

# Maximum number of results to fetch per scraping session
# Note: Higher numbers may increase risk of IP blocking
results_fetch_count = 300

# Country filter (for Indeed only)
country_to_search = 'USA'

# Optional prefix for CSV filenames
file_name_prefix = ''
```

### Role Filtering

Filter jobs by keywords in the job title. Jobs matching ANY of these keywords will be included:

```python
roles_of_interest = [
    "Backend",
    "Frontend",
    "Developer",
    "Engineer",
    # Add more keywords as needed
]
```

### Email Settings (Optional)

To receive job listings via email, configure these settings:

```python
email_send = True  # Set to True to enable email notifications

from_email = 'your.email@gmail.com'
email_password = 'your_app_password'  # See note below about app passwords
to_email = 'recipient@example.com'
email_smtp = 'smtp.gmail.com'  # Gmail SMTP server
```

#### SMTP Server Examples:

| Email Provider | SMTP Server |
|---------------|-------------|
| Gmail | `smtp.gmail.com` |
| Outlook/Hotmail | `smtp-mail.outlook.com` |
| Yahoo | `smtp.mail.yahoo.com` |
| iCloud | `smtp.mail.me.com` |

#### Gmail App Password Setup:

For Gmail, you'll need to create an "App Password" instead of using your regular password:

1. Go to your Google Account settings
2. Select **Security** → **2-Step Verification** (enable if not already)
3. Scroll to **App passwords**
4. Generate a new app password for "Mail"
5. Use this 16-character password in the `email_password` setting

## Usage

### Running the Scraper

Once configured, start the scraper:

```bash
python JobScraperUltimate.py
```

Or on some systems:

```bash
python3 JobScraperUltimate.py
```

### What Happens When You Run It:

1. **First Run**: Searches for jobs posted in the last `hours` hours (as configured)
2. **Subsequent Runs**: Searches for jobs posted in the last 1 hour only
3. **Filtering**: Applies your `roles_of_interest` keywords
4. **Deduplication**: Removes jobs already saved in today's CSV
5. **Saves Results**: Appends new jobs to a timestamped CSV file
6. **Email (Optional)**: Sends the CSV via email if enabled
7. **Sleeps**: Waits for `sleep_time` seconds before the next run
8. **Repeats**: Continues indefinitely until stopped

### Stopping the Scraper

Press `Ctrl + C` in the terminal to stop the scraper gracefully.

## Output Files

CSV files are automatically generated with descriptive names:

**Format**: `[prefix_]jobs_MonthName_Day_TimeOfDay.csv`

**Examples**:
- `jobs_January_21_morning.csv`
- `my_jobs_December_25_afternoon.csv`

**Time of Day Labels**:
- `overnight`: 12:00 AM - 8:59 AM
- `morning`: 9:00 AM - 11:59 AM
- `afternoon`: 12:00 PM - 3:59 PM
- `evening`: 4:00 PM - 8:59 PM
- `night`: 9:00 PM - 11:59 PM

Each scraping run adds a timestamp separator in the CSV, so you can see when each batch of jobs was found.

## CSV File Structure

| Column | Description |
|--------|-------------|
| `job_url` | Direct link to the job posting |
| `title` | Job title |
| `company` | Company name |
| `location` | Job location |

## Tips & Best Practices

### Avoiding IP Blocks

- Keep `results_fetch_count` at 300 or below
- Set `sleep_time` to at least 600 seconds (10 minutes) for production use
- Don't run multiple instances of the scraper simultaneously

### Optimizing Results

- Use specific keywords in `search_term` (e.g., "Python developer" instead of "developer")
- Add specific role keywords to `roles_of_interest` to reduce false positives
- Review the first few runs and adjust filters as needed

### Email Issues

- Ensure 2-factor authentication is enabled for Gmail
- Use app-specific passwords, not your regular account password
- Check your spam folder if emails aren't arriving
- Some email providers may require additional security settings

## Troubleshooting

### "ModuleNotFoundError: No module named 'jobspy'"

**Solution**: Install dependencies:
```bash
pip install -r requirements.txt
```

### "SMTPAuthenticationError" when sending emails

**Solution**:
- Verify your email and password are correct
- For Gmail, use an App Password instead of your regular password
- Check that 2-factor authentication is enabled

### "Too many requests" or IP blocking

**Solution**:
- Increase `sleep_time` to 1800 or 3600 seconds (30-60 minutes)
- Reduce `results_fetch_count` to 100 or less
- Use a VPN or wait 24 hours before trying again

### No jobs found

**Solution**:
- Make your `search_term` more general (e.g., "engineer" instead of "senior backend engineer")
- Remove or broaden your `roles_of_interest` filters
- Increase `hours` to search further back in time
- Check if the job portals are accessible from your location

## Contributing

Contributions are welcome! Feel free to:
- Report bugs or issues
- Suggest new features
- Submit pull requests
- Improve documentation

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For questions or feedback, contact: **samirasimha.r@gmail.com**

---

Made with ❤️ by [Samirasimha Rajasimha](https://github.com/Samirasimha)
