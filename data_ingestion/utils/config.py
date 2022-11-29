'''
The model for the configuration file which will be the input for the app
'''
import json
from typing import List
from pydantic import BaseModel
import logging
from typing import Optional


class DBConfiguration(BaseModel):
    username: str
    password: str
    host: str
    port: int
    database: str
    schema_name : Optional[str]


class ConfigModel(BaseModel):
    db_configuration: DBConfiguration
    dir_files: List[str]
    clean_schema: Optional[str] = "False"

def configmodel(dir_config):
    
    with open(dir_config) as file:
        raw_config = json.load(file)

    config = ConfigModel(**raw_config)

    logging.debug('Config is created')
    return config 


