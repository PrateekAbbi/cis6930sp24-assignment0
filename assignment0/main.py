import argparse
import urllib.request
import certifi
import ssl
import sqlite3
import fitz  # PyMuPDF
import os
from datetime import datetime

# Define a function to check if a string can be parsed into a datetime object.
def checkdatetime(str):
    try:
        datetime.strptime(str, "%d/%m/%Y %H:%M")
        return True
    except ValueError:
        return False

# Define a function to fetch a PDF file containing incident data from a specified URL.
def fetchincidents(url):         
    # Set a user agent to mimic a web browser request.
    headers = {'User-Agent': "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"}

    # Create a secure SSL context using certifi's CA bundle.
    context = ssl.create_default_context(cafile=certifi.where())             
    # Open the URL and read the data (PDF content).
    data = urllib.request.urlopen(urllib.request.Request(url, headers=headers), context=context).read()

    # Save the downloaded data to a temporary PDF file.
    with open('./docs/temp.pdf', 'wb') as f:
        f.write(data)

# Define a function to extract incident data from the fetched PDF.
def extractincidents():
    # Open the temporary PDF file.
    doc = fitz.open("./docs/temp.pdf")

    all_text = ""
    # Iterate through each page in the PDF and extract text.
    for page in doc:
        all_text += page.get_text()

    # Close the PDF document to free resources.
    doc.close()

    # Split the extracted text into lines.
    lines = all_text.split('\n')

    # Clean up the extracted lines if necessary.
    for i in range(5):
        if len(lines) > 0:
            lines.pop(0)

    if len(lines) > 0 and lines[-1] == "":
        lines.pop()
    
    if len(lines) > 0 and ":" in lines[-1] and "/" in lines[-1]:
        lines.pop()

    # Initialize lists to hold the extracted incident data.
    date_times, incident_numbers, locations, natures, incident_oris = [], [], [], [], []

    # Loop through the lines and extract incident data.
    for i in range(0, len(lines)):
        if 'Date / Time' in lines[i]: 
            continue

        # Check for the pattern indicating the start of an incident record.
        if i + 4 < len(lines) and '/' in lines[i] and ':' in lines[i]:
            date_times.append(lines[i].strip())
            incident_numbers.append(lines[i + 1].strip())
            locations.append(lines[i + 2].strip())
            if checkdatetime(lines[i + 3].strip()):
                natures.append("prateek")
            else:
                if lines[i + 3].strip() == "RAMP":
                    natures.append(lines[i+4].strip())
                else:
                    natures.append(lines[i + 3].strip())
            incident_oris.append(lines[i + 4].strip())

    # Package the extracted data into a dictionary.
    data = {
        'Date/Time': date_times,
        'Incident Number': incident_numbers,
        'Location': locations,
        'Nature': natures,
        'Incident ORI': incident_oris 
    }

    return data

# Define a function to create a SQLite database for storing incident data.
def createdb(db):
    try:
        # Connect to the SQLite database (or create it if it doesn't exist).
        con = sqlite3.connect(f"{db}")
        cur = con.cursor()
        # Create the incidents table.
        cur.execute(
            '''
            CREATE TABLE incidents (
                incident_time TEXT,
                incident_number TEXT,
                incident_location TEXT,
                nature TEXT,
                incident_ori TEXT
            )
            '''
        )
        return con
    except sqlite3.OperationalError as e:
        print("Invalid Database String")
        return e

# Define a function to populate the SQLite database with incident data.
def populatedb(db, data):
    cur = db.cursor()
    # Clear any existing data in the incidents table.
    cur.execute("DELETE FROM incidents")
    n = len(data["Date/Time"])

    # Insert the new incident data into the database.
    for i in range(n):
        cur.execute(
            '''
            INSERT INTO incidents (incident_time, incident_number, incident_location, nature, incident_ori)
            VALUES (?, ?, ?, ?, ?)
            ''',
            (data['Date/Time'][i], data['Incident Number'][i], data['Location'][i], data['Nature'][i], data['Incident ORI'][i])
        )

    # Commit the changes to the database.
    db.commit()
    # Remove the temporary PDF file.
    os.remove("./docs/temp.pdf")

# Define a function to generate a status report from the database.
def status(db):
    cur = db.cursor()
    # SQL query to count incidents by nature, sorted by count and nature.
    query = '''
        SELECT nature, COUNT(*) AS count
        FROM incidents
        GROUP BY nature
        ORDER BY count DESC, nature ASC
    '''

    # Execute the query and format the results.
    cur.execute(query)
    output = ""
    for row in cur.fetchall():
        if (row[0] == "prateek"):
            output += ""+"|"+str(row[1]) + "\n"
        else:    
            output += row[0] + "|" + str(row[1]) + "\n"

    # Clean up by dropping the incidents table.
    cur.execute("DROP TABLE incidents")

    return output

# Define the main function to orchestrate the fetching, extraction, and processing of incident data.
def main(url):
    # Fetch the PDF containing incident data.
    fetchincidents(url)

    # Extract incident data from the PDF.
    incidents = extractincidents()

    # Create and populate the database.
    db = createdb("resources/normanpd.db")
	
    populatedb(db, incidents)
	
    # Generate and return a status report.
    data = status(db)

    return data

# Entry point of the script.
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--incidents", type=str, required=True, 
                         help="Incident summary url.")
     
    args = parser.parse_args()
    if args.incidents:
        print(main(args.incidents))
