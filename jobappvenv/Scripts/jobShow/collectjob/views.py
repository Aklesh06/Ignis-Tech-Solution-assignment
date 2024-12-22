from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Job  
# Create your views here.

@csrf_exempt
def save_job_data(request):
    if request.method == 'POST':
        try:
            job_data = json.loads(request.body)  # Assuming you send JSON data
            for job_dict in job_data: 
                job = Job.objects.create(
                        company_logo=job_dict['company_logo'],
                        job_title=job_dict['job_title'],
                        company=job_dict['company'],
                        location=job_dict['location'],
                        posted_at=job_dict['posted_at'],
                        updated_at=job_dict['updated_at'],
                        employee_type=job_dict['employee_type'],
                        skills=job_dict['skills'],
                        location_type=job_dict['location_type'],
                        compensation=job_dict['compensation'],
                        job_description=job_dict['job_description'],
                        job_link=job_dict['job_link'],
                    )
                print(job)
            return JsonResponse({'message': 'Job data saved successfully!'}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

def get_job_data(request):
    jobs = Job.objects.all()  # Fetch all job data from the database
    job_list = list(jobs.values())  # Convert query results to a list of dictionaries
    return JsonResponse({'jobs': job_list}, safe=False)