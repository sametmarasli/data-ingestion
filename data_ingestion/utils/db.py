'''
Database connector helper class for different operations with DB
'''
from contextlib import contextmanager
from pydantic import BaseModel
from sqlalchemy import create_engine
from typing import Optional
from sqlalchemy.engine.url import URL
import logging
import pandas as pd

class DBConfiguration(BaseModel):
    username: str
    password: str
    host: str
    port: int
    database: str
    schema_name : Optional[str]

class DBConnection:
    def __init__(self, db_configuration:DBConfiguration ):
        self.conn_url  = URL.create(
            'mssql+pyodbc',
            username= db_configuration.username,
            password= db_configuration.password,
            database= db_configuration.database,
            host= db_configuration.host,
            port= db_configuration.port,
            query=dict(driver='ODBC Driver 17 for SQL Server'))

        self.schema_name = db_configuration.schema_name


    @contextmanager
    def managed_cursor(self):
        self.engine = create_engine(self.conn_url,connect_args = {'autocommit':True})

        try:
            yield self.engine
        finally:
            self.engine


    def create_clean_db(self, db_name):
        '''for test purposes'''
        q_dropdb = f"DROP DATABASE IF EXISTS {db_name}"
        q_createdb = f"CREATE DATABASE {db_name}"

        with self.managed_cursor() as conn:
            conn.execute(q_dropdb)
            conn.execute(q_createdb)
            print('database_add')
        
        logging.debug('Clean DB is run.')
        

    def create_clean_schema(self):
        '''for initializing a clean schema without tables'''

        q_droptables_atschema=f"EXEC sp_MSforeachtable @command1 = 'DROP TABLE ?' , @whereand = 'AND SCHEMA_NAME(schema_id) = ''{self.schema_name}'' '; "
        q_dropschema=f"DROP SCHEMA IF EXISTS {self.schema_name} ;"
        q_createschema=f"CREATE SCHEMA {self.schema_name}"

        with self.managed_cursor() as conn:
                conn.execute(q_droptables_atschema)
                conn.execute(q_dropschema)
                conn.execute(q_createschema)
        logging.debug('Finished cleaning the schema')


    def add_table_to_schema(self, data, table_name):
        '''adds a pandas df to a given db and schema'''
        with self.managed_cursor() as conn:
                data.to_sql(table_name, con=conn ,schema=self.schema_name, if_exists='replace', index=False)
    
    def read_table_from_schema(self, table_name):
        
        with self.managed_cursor() as conn:
                data = pd.read_sql_table(table_name,con=conn,schema=self.schema_name)
        return data
