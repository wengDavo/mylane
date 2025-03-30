# mylane

## Project Overview
**mylane** is a Django-based web application that provides company profile pages with data visualizations. The project includes:
- Company attributes and details
- Two data visualizations (job distribution by city and job family)
- A dropdown to switch between companies

## Prerequisites
Ensure you have the following installed:
- Python (>=3.8)
- Django
- pip (Python package manager)
- SQLite (default database for django, no additional setup required)

## Installation & Setup
Follow these steps to set up and run the project:

1. **Clone the Repository:**
   ```sh
   git clone https://github.com/your-username/mylane.git
   cd mylane
   ```

2. **Create a Virtual Environment and Activate It:**
   ```sh
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```

3. **Install Dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

4. **Run Migrations:**
   ```sh
   python manage.py migrate
   ```

5. **Load Sample Data:** (Mandatory Step)
   ```sh
   python manage.py import_companies
   ```

6. **Run the Development Server:**
   ```sh
   python manage.py runserver
   ```
   The application will be available at `http://127.0.0.1:8000/`.

## Usage
- Select a company from the dropdown to view details and charts.
- Job distribution charts update dynamically based on selection.

## API Endpoints
- **GET /companies/{id}/** - Retrieve company details
- **GET /companies/{id}/job-distribution/** - Get job distribution by city
- **GET /companies/{id}/job-family-distribution/** - Get job distribution by role

## Notes
- Ensure sample data is loaded before running the server.
- The database is SQLite, so no additional setup is required.

## Acknowledgments
Built using Django and Apache ECharts for visualizations.

