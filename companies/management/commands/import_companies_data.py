import os
import json
import pandas as pd
from django.core.management.base import BaseCommand
from companies.models import Company, JobPostByCity, JobPostByJobFamily

def safe_value(val):
    """Return the value if it's not NaN; otherwise, return None."""
    return val if pd.notna(val) else None

class Command(BaseCommand):
    help = "Import company and job post data from CSV files"

    def handle(self, *args, **kwargs):
        # Data folder is inside companies app under /companies/data/
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../data"))
        
        self.import_companies(os.path.join(base_path, "company_attributes.csv"))
        self.import_job_posts_by_city(os.path.join(base_path, "job_post_by_city.csv"))
        self.import_job_posts_by_family(os.path.join(base_path, "job_post_by_job_family.csv"))
        
        self.stdout.write(self.style.SUCCESS("Data imported successfully."))

    def import_companies(self, file_path):
        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR(f"File not found: {file_path}"))
            return

        df = pd.read_csv(file_path)

        for _, row in df.iterrows():
            # Parse links and founders fields from string to dict/list
            links_dict = self.parse_json_field(row.get("links"))
            founders_list = self.parse_founders(row.get("founders"))
            industry_list_parsed = self.parse_industry_list(row.get("industry_list"))
            
            Company.objects.update_or_create(
                company_id=row["company_id"],
                defaults={
                    "company_name": row["company_name"],
                    "industry_list": industry_list_parsed,
                    "city": safe_value(row.get("city")),
                    "state": safe_value(row.get("state")),
                    "linkedin": safe_value(row.get("linkedin")),
                    "founded": safe_value(row.get("founded")),
                    "website": safe_value(row.get("website")),
                    "description": row.get("description"),
                    "links": {
                        "website": safe_value(row.get("website")),
                        "linkedin": safe_value(row.get("linkedin")),
                        "career": links_dict.get("CAREER"),
                    },
                    "founders": founders_list,
                    "ceo": row.get("ceo"),
                    "company_ownership": row.get("company_ownership"),
                }
            )
        self.stdout.write(self.style.SUCCESS("Companies imported successfully."))
        


    def import_job_posts_by_city(self, file_path):
            if not os.path.exists(file_path):
                self.stdout.write(self.style.ERROR(f"File not found: {file_path}"))
                return

            try:
                df = pd.read_csv(file_path)

                for _, row in df.iterrows():
                    company = Company.objects.filter(company_id=row["company_id"]).first()
                    if company:
                        JobPostByCity.objects.create(
                            company=company,
                            city=row["city"],
                            state_name=row["state_name"],
                            lat=row["lat"],
                            lng=row["lng"],
                            population=row["population"],
                            position_count=row["position_count"],
                            wage_median=row["wage_median"],
                        )
                self.stdout.write(self.style.SUCCESS("Job posts imported successfully."))

            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error importing data: {e}"))

    def import_job_posts_by_family(self, file_path):
        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR(f"File not found: {file_path}"))
            return

        df = pd.read_csv(file_path)

        for _, row in df.iterrows():
            company = Company.objects.filter(company_id=row["company_id"]).first()
            if company:
                JobPostByJobFamily.objects.create(
                    company=company,
                    job_family=row["job_family"],
                    position_count=row["position_count"],
                    wage_median=row["wage_median"],
                )
        self.stdout.write(self.style.SUCCESS("Famly posts imported successfully."))

    def parse_json_field(self, field_value):
        """
        Safely parses a JSON field from a string.
        If the field is not valid JSON, return an empty dictionary.
        """
        if pd.notna(field_value):
            try:
                return json.loads(field_value)
            except json.JSONDecodeError:
                self.stdout.write(self.style.WARNING(f"Invalid JSON format: {field_value}"))
        return {}

    def parse_founders(self, founders_value):
        """
        Parses the founders field.
        For a value like '{""Marc Benioff"",""Parker Harris"",""Dave Moellenhoff"",""Frank Dominguez""}',
        this function strips braces and splits by commas,
        returning a list of dictionaries in the format: [{'name': 'Marc Benioff'}, ...]
        """
        if pd.notna(founders_value):
            # Remove surrounding braces if they exist.
            value = founders_value.strip()
            if value.startswith("{") and value.endswith("}"):
                value = value[1:-1]
            # Remove any extra quotes and split on commas.
            return [{"name": name.strip().strip('\"')} for name in value.split(",") if name.strip()]
        return []

    def parse_industry_list(self, field_value):
        """
        Parses the industry_list field.
        If valid JSON, returns the parsed value.
        Otherwise, if the value is like '{Technology}' or '{""Consumer Goods"",Technology}',
        removes the braces and splits the string into a list.
        """
        if pd.notna(field_value):
            try:
                # Attempt to load as JSON.
                return json.loads(field_value)
            except json.JSONDecodeError:
                # Fallback: remove surrounding braces and split by commas.
                value = field_value.strip()
                if value.startswith("{") and value.endswith("}"):
                    value = value[1:-1]
                industries = [item.strip().strip('\"') for item in value.split(",") if item.strip()]
                return industries
        return None
