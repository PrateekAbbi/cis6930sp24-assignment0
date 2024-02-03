import csv
from typing import Generator
from pypdf import PdfReader
import sqlite3
from assignment0.main import create_db, get_incidents, populate_db, fetch_pdf_file, get_pages
import pytest


@pytest.mark.parametrize(
    "file_url",
    [
        "https://www.normanok.gov/sites/default/files/documents/2024-01/2024-01-01_daily_incident_summary.pdf",
        "https://www.normanok.gov/sites/default/files/documents/2024-01/2024-01-21_daily_incident_summary.pdf",
    ],
)
def test_fetch_pdf_file(file_url: str):
    pdf_data: PdfReader = fetch_pdf_file(file_url)
    assert len(pdf_data.pages) > 0
    assert isinstance(pdf_data, PdfReader)


@pytest.mark.parametrize(
    "file_path",
    ["tests/2024-01-07_missing_cols.pdf", "tests/2024-01-11_multi_line.pdf"],
)
def test_get_pages(file_path: str):
    # Create a dummy PdfReader object
    pdf_file = PdfReader(file_path)

    # Call the get_pages function
    pages = get_pages(pdf_file)

    # Check if the returned value is a generator
    assert isinstance(pages, Generator)
    for page in pages:
        assert isinstance(page, str)


def test_create_db():
    # Call the create_db function
    connection = create_db()

    # Check if the returned value is a sqlite3.Connection object
    assert isinstance(connection, sqlite3.Connection)

    # Check if the incidents table exists in the database
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM incidents;")
    result = cursor.fetchall()
    assert len(result) == 0

    # Clean up: close the connection
    connection.close()


def test_populate_db():
    # Create a dummy sqlite3.Connection object
    connection = create_db()

    # Create a dummy incident
    incident = ["2024-01-01", "Incident 1", "Location 1", "Category 1", "Description 1"]

    # Call the populate_db function
    populate_db(connection, incident)

    # Check if the incident is inserted into the database
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM incidents;")
    result = cursor.fetchall()
    assert len(result) == 1
    assert result[0] == tuple(incident)

    # Clean up: close the connection
    connection.close()


@pytest.mark.parametrize(
    "file_name",
    ["2024-01-07_missing_cols", "2024-01-11_multi_line"],
)
def test_get_incidents(file_name: str):
    # Create a dummy PdfReader object
    pdf_file = PdfReader("tests/" + file_name + ".pdf")

    # Call the get_incidents function
    incidents: list[list[str]] = get_incidents(pdf_file)

    # Check if the returned value is a list
    assert isinstance(incidents, list)

    # Check if each incident is a list of strings
    for incident in incidents:
        assert isinstance(incident, list)
        assert 3 <= len(incident) <= 5
        for value in incident:
            assert isinstance(value, str)

    csv_file_name = "tests/" + file_name + ".csv"
    with open(csv_file_name, newline="") as csvfile:
        csv_file = csv.reader(csvfile, delimiter=",", quotechar='"')

        for zip_incident, zip_lines in zip(incidents, csv_file):
            assert zip_incident == zip_lines
