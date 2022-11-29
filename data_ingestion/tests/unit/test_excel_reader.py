from src.excel_to_db import ExcelToDB
import pandas as pd
import os
from utils.db import DBConfiguration
from utils.db import DBConnection

def test_read_excel():
    """
    GIVEN there is an excel workbook with one or more sheets
    WHEN want to read all the sheets at once
    THEN read all the sheets and store at a dictionary
    """
    
    reader = ExcelToDB(dir_file=os.path.abspath('./tests/unit/data/file_excel_1.xlsx'), db_configuration='')
    reader.read_excel()
    
    assert len(reader.data) == 2
    assert list(reader.data.keys())[0] == 'file_excel_1_xlsx_sheet_1' 
    assert reader.data['file_excel_1_xlsx_sheet_2'].shape == (6,2)
    
    
def test_ingest_to_db(create_db):
    """
    GIVEN an excel data is read and put at a dictionary as name:data 
    WHEN data is ingested to the db
    THEN check the data is written to db correctly
    """

    conf = DBConfiguration(**{ 
        "username":"sa",
        "password":"Test_password_123",
        "host":"test_db",
        "port":"1433",
        "database":"pytest_ingestion_db",
        "schema_name":"test_schema"})
        
    reader = ExcelToDB(dir_file='test',db_configuration=conf)

    seed_data = pd.DataFrame({'a':[1,2,3],'b':[3,4,5]})
    reader.data['seed_data'] = seed_data
    reader.ingest_data_to_mssql_database()
    
    dbconn = DBConnection(conf)
    read_seed_data = dbconn.read_table_from_schema('seed_data')
    
    assert read_seed_data.shape == (3,2)