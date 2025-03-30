from django.db import models

class Company(models.Model):
    company_id = models.IntegerField(primary_key=True)
    company_name = models.CharField(max_length=255)
    industry_list = models.JSONField(blank=True, null=True)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    linkedin = models.CharField(max_length=255, blank=True, null=True)
    founded = models.IntegerField(blank=True, null=True)
    website = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    links = models.JSONField(blank=True, null=True)
    founders = models.JSONField(blank=True, null=True)
    ceo = models.CharField(max_length=255, blank=True, null=True)
    company_ownership = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.company_name


class JobPostByCity(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    city = models.CharField(max_length=255)
    state_name = models.CharField(max_length=255)
    lat = models.FloatField()
    lng = models.FloatField()
    population = models.IntegerField()
    position_count = models.IntegerField()
    wage_median = models.IntegerField()

    def __str__(self):
        return f"{self.company.company_name} - {self.city}"


class JobPostByJobFamily(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    job_family = models.CharField(max_length=255)
    position_count = models.IntegerField()
    wage_median = models.IntegerField()

    def __str__(self):
        return f"{self.company.company_name} - {self.job_family}"
