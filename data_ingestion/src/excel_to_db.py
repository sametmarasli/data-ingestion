'''
The main class for reading an excel workbook and ingesting to a mssql db
'''

import pandas as pd
from joblib import Parallel, delayed
from utils.tools  import tame_text
from utils.db import DBConnection
from utils.db import DBConfiguration
import logging



class BaseReader:
    pass

class ExcelToDB(BaseReader):
    EXCEL_EXTENTIONS = ["*.xlsx", "*.xls", "*.xlsb"]

    def __init__(self, dir_file, db_configuration : DBConfiguration):
        self.dir_file = dir_file
        self.db_configuration = db_configuration
        self.data = {}

    def read_excel(self):
        """Reads all the excel sheets at an excel file
        """
        logging.debug('Started reading excels')

        sheet_names_of_excel = pd.ExcelFile(self.dir_file).sheet_names  
              
        list_excel = Parallel(n_jobs=-1)(delayed(pd.read_excel)(self.dir_file, 
                                                        sheet_name = name,
                                                        keep_default_na=False,
                                                        na_values='',
                                                        dtype=str, 
                                                        )
                                                        for name in sheet_names_of_excel)

        for j, sheet_name in enumerate(sheet_names_of_excel):
            self.data[ "{}_{}".format(tame_text(self.dir_file.split('/')[-1]), tame_text(sheet_name))] = list_excel[j]

        logging.debug('Finished reading excels')

    def ingest_data_to_mssql_database(self):
        """Transfer the dictionary of data to database
        """        
        logging.debug('Started ingesting data to db')

        for table_name, data in self.data.items():
            db_conn = DBConnection(db_configuration=self.db_configuration)
            db_conn.add_table_to_schema(data=data, table_name=table_name)
            logging.debug(f'Finished ingesting {table_name}')

        logging.debug(f'Finished ingesting all tables.')
        