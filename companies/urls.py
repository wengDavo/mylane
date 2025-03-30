from django.urls import path
from .views import index_view, company_detail, job_distribution, job_distribution_by_family

urlpatterns = [
    path('', index_view, name='dashboard_view'),
    path("companies/<int:company_id>/", company_detail, name="company_detail"),
    path("companies/<int:company_id>/job-distribution/", job_distribution, name="job_distribution"),
    path("companies/<int:company_id>/job-family-distribution/", job_distribution_by_family, name="job_family_distribution")
]
