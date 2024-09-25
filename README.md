
# JobScraperUltimate

## Description

**JobScraperUltimate** is a job scraping tool that scrapes job listings from LinkedIn, Indeed, and Skillsire. It allows users to automate the process of searching for jobs and saving results into a CSV file. Additionally, there is an option to email the results.

## Features

- Scrapes jobs from LinkedIn, Indeed, and Skillsire.
- Customizable search term and role filters.
- Fetches up to a specified number of job results per platform.
- Saves job listings in CSV format.
- Optional email notification with CSV attachment.
- Adjustable time intervals between scraping sessions to avoid IP blocks.

## Installation

1. Make sure Python is installed on your system.
2. Install the required package by running the following command:

   ```bash
   pip install -U python-jobspy
   ```

## Usage

### 1. Set Up Parameters:

Before running the scraper, customize the following settings in the script:

```python
# Time-related settings
hours = 1  # Number of hours before the current time to look for jobs.
sleep_time = 10  # Time (in seconds) to wait between each scraping session.

# Job portals to scrape from
scrape_from = ["linkedin", "indeed", "skillsire"]  # Specify portals to search from.

# Job search query
search_term = "software engineer"  # The job title or keyword to search for.

# Results settings
results_fetch_count = 10  # Number of job results to fetch per portal (limit to 300 to avoid IP blocking).

# Country filter (for Indeed only)
country_to_search = 'USA'

# CSV file name prefix (optional)
file_name_prefix = ''  # You can add a prefix to the file name if needed.

# Roles of interest (filter for specific roles in job results)
roles_of_interest = [
    "Backend", "Frontend", "Developer", 
]

# Email settings (optional)
email_send = False  # Set to True to email the CSV results.
from_email = ''  # Your email address.
email_password = ''  # Your email password.
to_email = ''  # Recipient email address.
email_smtp = ''  # SMTP server (e.g., smtp.gmail.com for Gmail, smtp-mail.outlook.com for Outlook).
```

### 2. Running the Script

Once your settings are configured, you can run the `.py` script by executing the following command in your terminal:

```bash
python3 JobScraperUltimate.py
```

This will start the scraper, fetching jobs from the specified portals and saving the results in a CSV file. If the email option is enabled, it will also send the CSV file to the configured recipient.

## Contributing

Feel free to submit issues or pull requests to improve the functionality of this project. Contributions are welcome!


## Contact

For any inquiries, contact me at samirasimha.r@gmail.com.
