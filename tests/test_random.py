import sqlite3
import pytest

import assignment0.main

@pytest.fixture
def baddb():
    return "http://localhost:9000000000"

def test_createDB(baddb):
    conn = assignment0.main.createdb(baddb)
    print(conn)

# import pytest
# from incident_report import fetchincidents, extractincidents, createdb, populatedb, status
import pandas as pd

def test_fetchincidents(mocker):
    # Mock urllib.request.urlopen
    mock_read = mocker.patch('urllib.request.urlopen')
    mock_read.return_value.read.return_value = b'Fake PDF data'
    mocker.patch('builtins.open', mocker.mock_open())
    
    assignment0.main.fetchincidents('http://example.com/incidents.pdf')

    # Assert that open was called to write 'temp.pdf'
    open.assert_called_once_with('temp.pdf', 'wb')
    open().write.assert_called_once_with(b'Fake PDF data')

def test_extractincidents(mocker):
    # Mock fitz.open to return a mock document
    mock_fitz = mocker.patch('fitz.open')
    mock_page = mocker.MagicMock()
    mock_page.get_text.return_value = "01/01/2021 00:00:00\nIncident#123\nLocation XYZ\nNature ABC\nORI1"
    mock_fitz.return_value.__enter__.return_value = [mock_page]
    
    df = assignment0.main.extractincidents()

    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert df.iloc[0]['Date/Time'] == '01/01/2021 00:00:00'

def test_createdb(mocker):
    mock_connect = mocker.patch('sqlite3.connect')
    mock_connect.return_value.cursor.return_value.execute.return_value = None

    db = assignment0.main.createdb("test.db")

    assert db is not None
    mock_connect.assert_called_once_with("test.db")

def test_populatedb(mocker):
    mock_db = mocker.MagicMock()
    mock_remove = mocker.patch('os.remove')

    df = pd.DataFrame({
        'Date/Time': ['01/01/2021 00:00:00'],
        'Incident Number': ['Incident#123'],
        'Location': ['Location XYZ'],
        'Nature': ['Nature ABC'],
        'Incident ORI': ['ORI1']
    })

    assignment0.main.populatedb(mock_db, df)

    assert mock_db.cursor.called
    mock_remove.assert_called_once_with("temp.pdf")

# You can add more tests for functions like `status()` here.





