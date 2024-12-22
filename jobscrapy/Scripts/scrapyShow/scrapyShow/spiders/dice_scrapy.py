import scrapy
import json

class JobSpider(scrapy.Spider):
    name = 'dice_job'
    allowed_domains = ['dice.com']
    start_urls = ['https://www.dice.com/jobs?q=Software&radius=30&radiusUnit=mi&page=1&pageSize=20&filters.postedDate=ONE&filters.workplaceTypes=Remote&filters.employmentType=CONTRACTS&currencyCode=USD&language=en']
    
    def parse(self, response):
        
        print("Parsing page:", response.url)
        jobs = json.loads(response.body)
        
        for job in jobs.get('data', []):
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
                yield scrapy.Request(job_detail_url, callback=self.parse_job_detail, meta={'job_data': job_data})

    def parse_job_detail(self, response):
        job_data = response.meta['job_data']
        skills_container = response.xpath('//div[@data-cy="skillsList"]')
        skills = []
        if skills_container:
            skill_divs = skills_container.xpath('.//div[@class="chip_chip_cYJs6"]')
            for skill_div in skill_divs:
                skill = skill_div.xpath('.//span/text()').get()
                if skill:
                    skills.append(skill)

        job_data['skills'] = skills

        print(job_data)
        yield job_data