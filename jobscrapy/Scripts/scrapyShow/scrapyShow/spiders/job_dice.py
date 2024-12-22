import os
import requests
import json
from bs4 import BeautifulSoup


headers = {
    'x-api-key': '1YAt0R9wBg4WfsF9VB2778F5CHLAPMVW3WAZcKd8',
}

base_params = {
    'q': 'Software',
    'radius': '30',
    'radiusUnit': 'mi',
    'filters.workplaceTypes': 'Remote',
    'filters.employmentType': 'CONTRACTS',
    'filters.postedDate': 'ONE',
    'currencyCode': 'USD',
    'pageSize': '20',
}

api_url = 'https://job-search-api.svc.dhigroupinc.com/v1/dice/jobs/search'

output_folder = 'job_datas'
os.makedirs(output_folder, exist_ok=True)

def scrape_job_detail(url):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Error fetching details from {url}")
        return {}
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    skills_container = soup.find('div', {'data-cy': 'skillsList'})
    location_content = soup.find('div', {'class': 'job-overview_chipContainer__E4zOO'})


    skills = []
    if skills_container:

        skill_divs = skills_container.find_all('div', {'class': 'chip_chip__cYJs6'})
        for skill_div in skill_divs:
            skill = skill_div.find('span').get_text(strip=True)
            
            skills.append(skill)
    else:
        print(f"Skills container not found on {url}")
    loc_type = []
    if location_content:

        loc_divs = location_content.find_all('div', {'class': 'chip_chip__cYJs6'})
        for loc_div in loc_divs:
            loc = loc_div.find('span').get_text(strip=True)
            
            loc_type.append(loc)
    else:
        print(f"Location_type container not found on {url}")
    return {
            'skills': skills,
            'location_type': loc_type,
    }
    
    
def scrape_job_detail_from_redirect_page(url):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Error fetching details from {url}")
        return {}
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    skills = ["Java", "Python", "JavaScript / TypeScript", "C++", "Swift","Verilog"]
    loc_type = ["Remote"]

    return {
            'skills': skills,
            'location_type': loc_type,
    }

page = 1
page_jobs = []

while True:

    params = base_params.copy()
    params['page'] = str(page)
    
    response = requests.get(api_url, headers=headers, params=params)
    
    if response.status_code != 200:
        print(f"Error: Failed to fetch jobs on page {page}. Status code: {response.status_code}")
        break
    
    response_data = response.json()
    jobs = response_data.get('data', [])
    
    if not jobs:
        print(f"No more jobs found. Stopping at page {page}.")
        break

    page_jobs.extend(jobs)
    
    if len(page_jobs) >= 3:
        print("Fetched available jobs from 3 pages")
        break

    page += 1

jobs= []
for job in page_jobs:
    job_data = {
        'company_logo': job.get('companyLogoUrl'),
        'job_title': job.get('title'),
        'company': job.get('companyName'),
        'location': job.get('jobLocation', {}).get('displayName'),
        'posted_at': job.get('postedDate'),
        'updated_at': job.get('modifiedDate'),
        'employee_type': job.get('employmentType'),
        'skills': job.get('jobMetadata', {}).get('skills', []),
        'location_type': job.get('workplaceTypes'),
        'compensation': job.get('salary'),
        'job_description': job.get('summary'),
        'job_link': job.get('detailsPageUrl')
    }
    
    job_detail_url = job.get('detailsPageUrl')
    if job_detail_url:
        print(f"Fetching additional details")
        if('apply-redirect' in job_detail_url):
            job_details = scrape_job_detail_from_redirect_page(job_detail_url)
        else:
            job_details = scrape_job_detail(job_detail_url)
        job_data.update(job_details) 
    
    jobs.append(job_data)
    
post_url = 'http://127.0.0.1:8000/api/save_job_data/'

response = requests.post(post_url, json=jobs)

if response.status_code == 201:
    print("Job data saved successfully!")
else:
    print(f"Failed to save job data. Status code: {response.status_code}, Error: {response.text}")
    
output_file = os.path.join(output_folder, f'jobs_pages.json')
with open(output_file, 'w') as file:
    json.dump(jobs, file, indent=4)

print(f"Saved {len(jobs)} jobs from page {page} to {output_file}")
    
print(f"Job data saved in folder: {output_folder}")

        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        

        # job_data.get({
        #     'job_title': response.xpath('//h1[@data-cy="jobTitle"]/text()').get(),
        #     'company': response.xpath('//a[@data-cy="companyNameLink"]/text()').get(),
        #     'location': response.xpath('//li[@data-cy="location"]/text()').get(),
        #     'posted_updated': response.xpath('span//div[@id="timeAgo"]/text()').get(),
        #     'skills': response.xpath('//div[@data-testid="skillsList"]/text()').getall(),
        #     'employee_type': response.xpath('//span[@id="employmentDetailChip"]/text()').get().replace('Contract -',''),
        #     'location_type': response.xpath('//span[@id="location"]/text()').get(),
        #     'compensation': response.xpath('//span[@id="payChip"]/text()').get(),
        #     'job_detail': response.xpath('//selection[@class="job-description"]/text()').getall(),
        # })
