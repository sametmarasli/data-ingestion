import pytest 
from utils.db import DBConnection
from utils.db import DBConfiguration

@pytest.fixture
def create_db():

    with DBConnection(DBConfiguration(**{ 
        "username":"sa",
        "password":"Test_password_123",
        "host":"test_db",
        "port":"1433",
        "database":"master"})).managed_cursor() as conn:
        
        conn.execute("DROP DATABASE IF EXISTS pytest_ingestion_db")
        conn.execute("CREATE DATABASE pytest_ingestion_db")
    
    with DBConnection(DBConfiguration(**{ 
        "username":"sa",
        "password":"Test_password_123",
        "host":"test_db",
        "port":"1433",
        "database":"pytest_ingestion_db"})).managed_cursor() as conn:

        conn.execute("CREATE SCHEMA test_schema")


