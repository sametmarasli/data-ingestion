from src.excel_to_db import ExcelToDB

def read_excel_ingest_db(config):
    reader = ExcelToDB(**config)
    reader.read_excel()
    reader.ingest_data_to_mssql_database()

