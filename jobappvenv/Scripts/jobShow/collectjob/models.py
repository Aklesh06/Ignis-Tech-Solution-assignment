from django.db import models

# Create your models here.

class Job(models.Model):
        
        job_title       = models.CharField(max_length=200)
        company_logo    = models.URLField()
        company         = models.CharField(max_length=200)
        location        = models.CharField(max_length=250)
        posted_at       = models.CharField(max_length=100)
        updated_at      = models.CharField(max_length=100)
        employee_type   = models.CharField(max_length=50)
        skills          = models.JSONField()
        location_type   = models.JSONField()
        compensation    = models.CharField(max_length=50)
        job_description = models.TextField()
        job_link        = models.URLField(max_length=2000)