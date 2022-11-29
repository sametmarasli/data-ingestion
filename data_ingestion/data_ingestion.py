# from src import read_excel_ingest_db
from src.excel_to_db import ExcelToDB
from utils.db import  DBConnection
from utils.config import configmodel
import logging
import click

logging.basicConfig(level=logging.DEBUG)

@click.command()
@click.option('--dir_config', default='./config.json', help='Name of the json dir_config located in "../input/config/" directory')

def main(dir_config):
    
    config = configmodel(dir_config)

    if config.clean_schema == "True":
        db_conn = DBConnection(db_configuration=config.db_configuration)
        db_conn.create_clean_schema()    

    for dir_file in config.dir_files:
        logging.debug(f'File: {dir_file}')
        reader = ExcelToDB(dir_file=dir_file, db_configuration=config.db_configuration)
        reader.read_excel()
        reader.ingest_data_to_mssql_database()        
            
    
if __name__ == "__main__":
    main()
