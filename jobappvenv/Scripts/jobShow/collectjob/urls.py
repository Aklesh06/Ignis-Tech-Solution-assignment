from . import views
from django.urls import path

urlpatterns = [
    path('api/save_job_data/', views.save_job_data, name='save_job_data'),
    path('api/jobs/', views.get_job_data, name='get_job_data'),
]
