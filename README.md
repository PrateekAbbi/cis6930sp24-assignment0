### Student: Prateek Abbi
### UFID: 89387132

---

### Project Overview

The Norman PD Incident Data Extractor is a Python package developed for the CIS 6930 Spring 2024 course. This project automates the extraction of incident data from PDF files available on the Norman, Oklahoma Police Department website and stores it in an SQLite database. It facilitates efficient data analysis and reporting by parsing specific fields from the PDF files and performing database operations.

---

### Installation Instructions

#### Prerequisites
- Python 3.11
- pip or pip3 (for Mac users)

#### Setup Environment
1. **Install `pipenv`:** If `pipenv` is not installed on your system, you can install it using pip. Open your terminal and run:
    ```bash
    pip install pipenv
    # or for Mac
    pip3 install pipenv
    ```

2. **Install Dependencies:** Navigate to your project directory in the terminal and run the following command to set up your environment and install the required packages:
    ```bash
    pipenv install
    ```

---

### Usage Guide

#### Running the Main Script
- To fetch and process incident data, execute `main.py` using `pipenv` with the following command:
    ```bash
    pipenv run python assignment0/main.py --incidents <URL>
    ```
    Replace `<URL>` with the link to the incident summaries from [Norman PD's Department Activity Reports](https://www.normanok.gov/public-safety/police-department/crime-prevention-data/department-activity-reports).

#### Running Tests
- To run unit tests, use the following command:
    ```bash
    pipenv run pytest
    ```

---

### Key Functionalities

- **Data Extraction:** Parses PDF files to extract incident data.
- **Database Management:** Inserts extracted data into an SQLite database for efficient querying and analysis.
- **Data Analysis:** Provides summaries of incidents by type and frequency.

---

### Technical Details

#### Main Components

- `fetchincidents(url)`: Downloads the PDF file from the specified URL.
- `extractincidents(url)`: Extracts data from the PDF file and prepares it for database insertion.
- `createdb(db)`: Initializes the SQLite database and tables if they do not exist.
- `populatedb(db, data)`: Inserts parsed incident data into the database.
- `status(db)`: Summarizes the incident data stored in the database by type and frequency.

#### Testing Components

- **test_random.py**: Contains unit tests for verifying the functionality of main components using the `pytest` framework.
- **test_download.py**: Tests the download functionality to ensure PDFs are fetched correctly.

---

### Bugs and Assumptions

- Assumes a consistent format for PDF incident reports.
- May not cover all edge cases for error handling, especially with malformed PDFs.
- The database schema is designed based on current incident data formats and may require updates if formats change.
- Specific assumptions are made for handling data anomalies (e.g., handling "RAMP" in location fields).

---

### Dependencies

- **Argparse**: For parsing command-line arguments.
- **urllib**: For opening URLs.
- **Certifi** and **ssl**: For SSL certification handling.
- **sqlite3**: For SQLite database operations.
- **Fitz**: For reading PDF files (alternative to the package recommended by the course due to version conflicts).

---

### Demonstration
[DEMO Video](https://youtu.be/XbHTRp2-7OQ)