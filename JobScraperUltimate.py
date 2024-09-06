# Job Scraper Ultimate

## Settings

hours = 1  
sleep_time = 10  
scrape_from = ["linkedin", "indeed", "skillsire"]  
search_term = "software engineer" 
results_fetch_count = 300 
country_to_search = 'USA' 
file_name_prefix = '' 
roles_of_interest = [
    "Backend", "Frontend", "Developer", 
]

#Email Settings
email_send = False  
from_email = ''
email_password = ''
to_email = ''
email_smtp = '' 


## Imports

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import time
import calendar
import csv
import os  # To check if the file exists
from jobspy import scrape_jobs
import pandas as pd
from datetime import datetime
import requests
import json


## Helper Functions 


def getFileName(extraText):
    timeObj = time.localtime(time.time())
    
    time_of_day = ''
    
    if timeObj.tm_hour >= 0 and timeObj.tm_hour < 9: 
        time_of_day = 'overnight'
    elif timeObj.tm_hour >= 9 and timeObj.tm_hour < 12: 
        time_of_day = 'morning'
    elif timeObj.tm_hour >=12  and timeObj.tm_hour < 16: 
        time_of_day = 'afternoon'
    elif timeObj.tm_hour >= 16 and timeObj.tm_hour < 21: 
        time_of_day = 'evening'
    elif timeObj.tm_hour >= 21:
        time_of_day = 'night'
    
    file_name = 'jobs_'+calendar.month_name[timeObj.tm_mon]+'_'+str(timeObj.tm_mday)+'_'+time_of_day+'.csv'

    if len(extraText) > 0:
        file_name = extraText+'_'+file_name

    return file_name


# Function to get existing job URLs from the CSV file if it exists
def load_existing_jobs(file_name):
    if os.path.exists(file_name):
        existing_jobs = pd.read_csv(file_name, quoting=csv.QUOTE_NONNUMERIC, escapechar="\\")
        
        if 'job_url' in existing_jobs.columns:
            return existing_jobs['job_url'].tolist()
        else:
            print(f"Warning: 'job_url' column not found in {file_name}. Deduplication skipped.")
            return []
    return []

## Emailer

def send_email(file_path, recipient_email):

    # Create the MIMEMultipart object
    message = MIMEMultipart()
    message['From'] = from_email
    message['To'] = to_email
    message['Subject'] = "Newly Scraped Job Listings"

    # Email body
    body = "Attached is the latest scrape of job listings."
    message.attach(MIMEText(body, 'plain'))

    # Attach the file
    attachment = open(file_path, "rb")
    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= %s" % os.path.basename(file_path))
    message.attach(part)

    # Connect to the SMTP server and send the email
    server = smtplib.SMTP(email_smtp, 587)  # Use 465 for SSL
    server.starttls()  # Secure the connection
    server.login(from_email, email_password)
    text = message.as_string()
    server.sendmail(from_email, recipient_email, text)
    server.quit()

    print("Email sent successfully!")

## Skillsire Scraper

def construct_skillsire_job_url(job_id):
    return f"https://www.skillsire.com/job/jobs-enlisting/all-jobs?jobId={job_id}"

def fetch_jobs_from_skillsire(initial_payload):
    api_url = "https://www.skillsire.com/api/job/all-jobs"
    headers = {'Content-Type': 'application/json'}
    all_jobs = []  # List to hold all jobs
    offset = 0
    batch_size = 20  # Assume API returns jobs in batches of 20

    while True:
        # Update the payload with the current offset
        payload = initial_payload.copy()
        payload['offset'] = offset
        
        try:
            # Make the API call
            response = requests.post(api_url, data=json.dumps(payload), headers=headers)
            
            # Check if the request was successful
            if response.status_code == 200:
                data = response.json()
                jobs = data.get('jobs', [])
                all_jobs.extend(jobs)  
                
                total_jobs = data.get('metaData', {}).get('resultCount', 0) 
                total_jobs = total_jobs if total_jobs < results_fetch_count else results_fetch_count
                print(f"Fetched {len(jobs)} jobs (offset: {offset}), total so far from SkillSire: {len(all_jobs)} of {total_jobs}.")
                
                # If no more jobs are returned, we have fetched all available jobs
                if not jobs or len(all_jobs) >= total_jobs:
                    break

                # Update the offset for the next batch of jobs
                offset += batch_size
            else:
                print(f"Failed to fetch data. Status code: {response.status_code}")
                break
        except Exception as e:
            print(f"An error occurred: {e}")
            break

    return all_jobs

def skillSire_scraper(current_jobs):
    # Skillsire API details

    skillsire_hours_before = 'p'+ ('24' if hours > 1 else '1') + 'h'
    print(skillsire_hours_before)
    payload = {"loc":"United States","cc":"us","type":"country","dp":skillsire_hours_before,"query":search_term}

    # Fetch jobs from Skillsire
    skillsire_jobs = fetch_jobs_from_skillsire(payload)
            
    if skillsire_jobs:
        # Convert Skillsire jobs into the structure expected in current_jobs
        skillsire_data = []
        for job in skillsire_jobs:
            
            job_location = "Unknown"  # Default location if not found
            if job.get('jobLocations') and len(job['jobLocations']) > 0:
                job_location = job['jobLocations'][0].get('jobState', "Unknown")
                
            job_data = {
                'job_url': construct_skillsire_job_url(job['jobId']),
                'title': job['jobTitle'],
                'company': job['jobCompany'],
                'location': job_location
            }
            skillsire_data.append(job_data)

        # Convert to DataFrame and append to current_jobs
        skillsire_df = pd.DataFrame(skillsire_data)
        current_jobs = pd.concat([current_jobs, skillsire_df], ignore_index=True)

    return current_jobs


roles_of_interest_lower = [role.lower() for role in roles_of_interest]
selected_fields = ['job_url', 'title', 'company', 'location']

include_skillsire = False

if "skillsire" in scrape_from:
    scrape_from.remove("skillsire")
    include_skillsire = True

try:
    while True:
        file_name_csv = getFileName(file_name_prefix)
        timeObj = time.localtime(time.time())
        # Dummy row to act as a separator between scraping runs
        dummy_row = pd.DataFrame({'job_url': 'Jobs Scraped at : ', 'title': '#', 'company': time.strftime("%m/%d/%Y", timeObj), 'location': time.strftime("%H:%M:%S", timeObj)}, index=[0])
        
        print(f"Starting scrape at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        try:
            # Scrape jobs from different platforms
            current_jobs = scrape_jobs(
                site_name=scrape_from, 
                search_term=search_term, 
                results_wanted=results_fetch_count,
                hours_old=hours,  
                country_indeed=country_to_search,
            )
            if include_skillsire:
                current_jobs = skillSire_scraper(current_jobs)
                
        except Exception as e:
            print(f"Error during scraping: {e}")
            time.sleep(sleep_time)
            continue

        current_jobs['title_lower'] = current_jobs['title'].str.lower()

        # Filter jobs based on matching roles
        matching_jobs = current_jobs[current_jobs['title_lower'].apply(
            lambda title: any(role in title for role in roles_of_interest_lower)
        )]
        matching_jobs = matching_jobs[selected_fields]

        # Load existing jobs from the CSV file (if it exists)
        existing_job_urls = load_existing_jobs(file_name_csv)

        # Perform set subtraction to find new jobs (using job_url)
        if existing_job_urls:
            new_jobs = matching_jobs[~matching_jobs['job_url'].isin(existing_job_urls)]
        else:
            new_jobs = matching_jobs

        job_count = len(new_jobs)
        
        if job_count > 0:
            print(f"Found {job_count} new jobs")

            # Combine the dummy row and new jobs for separation in the CSV file
            new_jobs_with_dummy = pd.concat([dummy_row, new_jobs])

            # Check if the file exists and append to it
            file_exists = os.path.exists(file_name_csv)
            
            # Append new jobs (with dummy row) to the CSV file
            with open(file_name_csv, 'a', newline='', encoding='utf-8') as csv_file:
                # Write the header only if the file is being created for the first time
                new_jobs_with_dummy.to_csv(
                    csv_file, 
                    header=not file_exists,  # Add header only if file doesn't exist
                    quoting=csv.QUOTE_NONNUMERIC, 
                    escapechar="\\", 
                    index=False
                )
        else:
            print("No new jobs found")

        if email_send:
            time.sleep(10) #This is set because the CSV Takes time to save
            send_email(file_name_csv,to_email)

        hours = 1  # After the first run, check only for fresh jobs (1 hour old)
        # Wait before scraping again
        print(f"Sleeping for {sleep_time} seconds...")
        time.sleep(sleep_time)

except KeyboardInterrupt:
    print("Scraping stopped by user.")









