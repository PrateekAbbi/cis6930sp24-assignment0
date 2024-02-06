### Name:
Prateek Abbi

### Assignment Description
This project is designed to automate the process of fetching, processing, and storing incident data from specified sources. The `main.py` script is responsible for downloading incident reports in PDF format, extracting relevant information, and storing it in a SQLite database for easy access and manipulation. The `test_random.py` file contains tests to ensure the reliability and correctness of the functionality provided by `main.py`.

### How to Install
To set up your environment to run these scripts, you should use `pipenv` for managing dependencies. Ensure you have `pipenv` installed; if not, you can install it using pip:

```bash
pip install pipenv
or 
pip3 install pipenv (FOR MAC)
```

Once `pipenv` is installed, navigate to the project directory and run the following command to install the required packages:

```bash
pipenv install
```

### How to Run

#### main.py
To execute the main script, you will need to use `pipenv` to run the script within the virtual environment. Here is a basic command to start the script:

```bash
pipenv run python assignment0/main.py --incidents <URL>
```

While Entering the URL, keep in mind to put in the URL of Incident summaries from the link https://www.normanok.gov/public-safety/police-department/crime-prevention-data/department-activity-reports.

#### test_random.py
To run the tests, you can use `pytest` within the virtual environment as follows:

```bash
pipenv run pytest
```

### Functions

#### main.py
- `checkdatetime(str)`: Validates if the provided string can be parsed into a datetime object.
- `fetchincidents(url)`: Fetches a PDF file containing incident data from the specified URL.
- Additional functions related to PDF processing and database interactions would be described here.

#### test_random.py
- Contains unit tests for functions defined in `main.py` using the `pytest` framework and mocks.

### Database Development
The script uses a SQLite database to store incident data. It involves creating tables, inserting records, and potentially querying these records for further processing or analysis.

### Bugs and Assumptions
- The script assumes that all PDF files follow a specific format for incident reports.
- Error handling may not cover all edge cases, especially for malformed PDFs or unexpected data formats.
- The database schema is designed with the current understanding of the incident data; changes in the data format may require schema adjustments.
- Assuming that in any PDF file only location and nature of the incident can be missing and every other data is there.
- For the data where location contains "RAMP", I have assumed that Nature is getting pushed into Nature_ORI, so I have adjusted my code logic based on that. 

### Packages Used
#### Argparse
- The URL of the PDF file from which we need to read the data, is getting passed as an argument from the Command line terminal. So, to read that argument, I have used Argparse
#### urllib
- To open the parsed URL, this package is used. 
#### Certifi and ssl
- I have used these packages for the ssl certification of the website.
#### sqlite3
- To operate on sqlite database from python, this package has been used. 
#### Fitz
- I have used this package to open the PDF file. The default package which Prof asked us to use was giving some version error to me. So I had to shift to another pacakge for getting the data from PDF. 

### Demo
To demonstrate the execution and functionality of the scripts, include a gif or video link here showing how the scripts are executed and their expected outcomes.

This README template provides a comprehensive guide for understanding, installing, and using the scripts. Modify the sections as necessary to fit the specific details and requirements of your project.