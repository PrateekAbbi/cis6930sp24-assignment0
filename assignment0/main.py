import argparse
import urllib.request
import certifi
import ssl
import sqlite3
import fitz
import pandas as pd
import os


def fetchincidents(url):         
    headers = {'User-Agent': "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"}

    context = ssl.create_default_context(cafile=certifi.where())             
    data = urllib.request.urlopen(urllib.request.Request(url, headers=headers), context=context).read()

    with open('temp.pdf', 'wb') as f:
        f.write(data)


def extractincidents():
    doc = fitz.open("./temp.pdf")

    all_text = ""
    for page in doc:
        all_text += page.get_text()

    doc.close()

    lines = all_text.split('\n')

    date_times, incident_numbers, locations, natures, incident_oris = [], [], [], [], []

    for i in range(0, len(lines)):
        if 'Date / Time' in lines[i]: 
            continue
        
        if i + 4 < len(lines) and '/' in lines[i] and ':' in lines[i]:
            date_times.append(lines[i].strip())
            incident_numbers.append(lines[i + 1].strip())
            locations.append(lines[i + 2].strip())
            natures.append(lines[i + 3].strip())
            incident_oris.append(lines[i + 4].strip())

    
    df = pd.DataFrame({
        'Date/Time': date_times,
        'Incident Number': incident_numbers,
        'Location': locations,
        'Nature': natures,
        'Incident ORI': incident_oris
    })

    return df


def createdb(db):
    try:
        con = sqlite3.connect(f"{db}")
        cur = con.cursor()
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


def populatedb(db, df):
    cur = db.cursor()
    cur.execute("DELETE FROM incidents")
    for _, row in df.iterrows():
        cur.execute(
            '''
            INSERT INTO incidents (incident_time, incident_number, incident_location, nature, incident_ori)
            VALUES (?, ?, ?, ?, ?)
            ''',
            (row['Date/Time'], row['Incident Number'], row['Location'], row['Nature'], row['Incident ORI'])
        )
    db.commit()
    os.remove("temp.pdf")


def status(db):
    cur = db.cursor()
    query = '''
        SELECT nature, COUNT(*) AS count
        FROM incidents
        GROUP BY nature
        ORDER BY count DESC, nature ASC
    '''

    cur.execute(query)

    output = '\n'.join(['|'.join(map(str, row)) for row in cur.fetchall()])

    cur.execute("DROP TABLE incidents")

    return output


def main(url):
    fetchincidents(url)

    incidents = extractincidents()

    # Create new database
    db = createdb("resources/normanpd.db")
	
    # Insert data
    populatedb(db, incidents)
	
    # Print incident counts
    data = status(db)

    return data


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--incidents", type=str, required=True, 
                         help="Incident summary url.")
     
    args = parser.parse_args()
    if args.incidents:
        print(main(args.incidents))