import pytest
import os
import requests
import assignment0.main

# Test 1: Check if the URL is correct and accessible
def test_url_accessibility():
    url = "https://www.normanok.gov/sites/default/files/documents/2024-01/2024-01-01_daily_incident_summary.pdf"
    response = requests.get(url)
    assert response.status_code == 200, "URL is not accessible or does not exist"

# Test 2: Check PDF content is correctly downloaded
def test_pdf_download_and_content():
    url = "https://www.normanok.gov/sites/default/files/documents/2024-01/2024-01-01_daily_incident_summary.pdf"
    assignment0.main.fetchincidents(url)  # Assuming this function downloads the PDF to temp.pdf
    assert os.path.isfile("temp.pdf"), "temp.pdf file was not created"


# Test 3: Confirm temp.pdf creation without issues
def test_temp_pdf_creation():
    url = "https://www.normanok.gov/sites/default/files/documents/2024-01/2024-01-01_daily_incident_summary.pdf"
    assignment0.main.fetchincidents(url)
    assert os.path.isfile("temp.pdf"), "temp.pdf file was not created"

# You might need a fixture to cleanup after tests that create files or modify the environment.
@pytest.fixture(autouse=True)
def cleanup(request):
    # Cleanup function to remove temp.pdf after each test
    def remove_temp_pdf():
        if os.path.isfile("temp.pdf"):
            os.remove("temp.pdf")
    request.addfinalizer(remove_temp_pdf)
