from django.contrib import admin
from companies.models import Company, JobPostByCity, JobPostByJobFamily

admin.site.register(Company)
admin.site.register(JobPostByCity)
admin.site.register(JobPostByJobFamily)