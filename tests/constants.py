import os
from dotenv import load_dotenv
load_dotenv()

DATABASE_URL = os.environ.get('DATABASE_URL')
TABLE_NAME = os.environ.get('TABLE_NAME')
REDSHIFT_DB_NAME = os.environ.get('REDSHIFT_DB_NAME')
REDSHIFT_PASSWORD = os.environ.get('REDSHIFT_PASSWORD')
REDSHIFT_USER = os.environ.get('REDSHIFT_USER')
REDSHIFT_HOST = os.environ.get('REDSHIFT_HOST')
REDSHIFT_PORT = os.environ.get('REDSHIFT_PORT')
PRODUCTNAME = os.environ.get('PRODUCTNAME')