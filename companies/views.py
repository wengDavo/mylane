from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.db.models import Sum
from .models import Company, JobPostByCity, JobPostByJobFamily

def index_view(request):
    companies = Company.objects.all()
    context = {
        "companies": companies
    }
    return render(request, "company/index.html", context)

def company_detail(request, company_id):
    company = get_object_or_404(Company, company_id=company_id)
    
    data = {
        "company_id": company.company_id,
        "company_name": company.company_name,
        "industry_list": company.industry_list or [],
        "city": company.city,
        "state": company.state,
        "linkedin": company.linkedin,
        "founded": company.founded,
        "website": company.website,
        "description": company.description,
        "links": company.links or [],
        "founders": company.founders or [], 
        "ceo": company.ceo,
        "company_ownership": company.company_ownership,
    }
    return JsonResponse(data)

def job_distribution(request, company_id):
    try:
        company = Company.objects.get(pk=company_id)
    except Company.DoesNotExist:
        return JsonResponse({"error": "Company not found"}, status=404)

    # Count jobs per city for the given company
    cities_count = (
        JobPostByCity.objects.filter(company=company)
        .values("city")
        .annotate(count=Sum("position_count"))
    )

    # Count total job openings for the company
    total_jobs = JobPostByCity.objects.filter(company=company).aggregate(Sum("position_count"))["position_count__sum"] or 0

    data = {
        "cities": [{"name": item["city"], "value": item["count"]} for item in cities_count],
        "total_jobs": total_jobs,  # Total job count
    }

    return JsonResponse(data)

def job_distribution_by_family(request, company_id):
    job_families = (
        JobPostByJobFamily.objects
        .filter(company_id=company_id)
        .values("job_family", "position_count")
    )
    data = [{"name": job["job_family"], "value": job["position_count"]} for job in job_families]
    return JsonResponse({"job_families": data})