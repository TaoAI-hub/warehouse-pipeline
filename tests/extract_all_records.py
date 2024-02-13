from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from show_columns import generate_create_table_statement, insert_records_to_table, create_table
import psycopg2
from constants import *



def table_exists(connection, table_name, productname):
    try:
        print("Checking if table exists...")
        query = f"""
        SELECT EXISTS (
            SELECT 1 
            FROM information_schema.tables 
            WHERE table_name = '{productname}_{table_name}'
        );
        """
        cursor = connection.cursor()
        cursor.execute(query)
        exists = cursor.fetchone()[0]
        cursor.close()
        print(f"Table {table_name} exists: {exists}")
        return exists
    except Exception as e:
        print(f"Error checking if table exists: {e}")
        return False

def load_to_redshift(records, database_url, redshift_user, redshift_password, redshift_host, redshift_port, redshift_db_name):
    try:
        print("Connecting to Redshift...")
        connection = psycopg2.connect(
            user=redshift_user, 
            password=redshift_password,
            host=redshift_host, 
            port=redshift_port, 
            database=redshift_db_name
        )
        print("<<<===== Connection succeeded ====>>>")
        if not table_exists(connection, table_name=TABLE_NAME, productname=PRODUCTNAME):
            create_table_query = generate_create_table_statement(database_url=database_url, table_name=TABLE_NAME, productname=PRODUCTNAME)
            print("CREATE TABLE STATEMENT: \n", create_table_query)
            create_table(connection, create_table_query)

        print(f"<----- Inserting records into {TABLE_NAME} ---->")
        query = insert_records_to_table(connection=connection, table_name=TABLE_NAME, productname=PRODUCTNAME, records=records)
        print("<----- Records added successfully ---->")
            
    except Exception as e:
        print(f"Error loading records to Redshift: {e}")

def extract_all_user_data(DATABASE_URL, table_name):
    try:
        print("Extracting all user data...")
        # SQLAlchemy engine connection string
        engine = create_engine(DATABASE_URL)
        
        # Create a Session
        Session = sessionmaker(bind=engine)
        session = Session()

        # Fetch all records from the table
        query = str(f"""SELECT * FROM public.{table_name}""")
        print("select query: ", query)
        select_query = text(query)
        
        
        # Execute the query
        records = session.execute(select_query).fetchall()
        print(records)

        # Close the session
        session.close()
        
        print("User data extraction completed.")
        return records
    except Exception as e:
        print(f"Error extracting user data: {e}")
        return []

# Fetch and print the records
all_user_data = extract_all_user_data(DATABASE_URL=DATABASE_URL, table_name=TABLE_NAME)
print("<---- Loading into redshift cluster ---->")
try:
    load_to_redshift(
        all_user_data,
        database_url=DATABASE_URL,
        redshift_user=REDSHIFT_USER, 
        redshift_password=REDSHIFT_PASSWORD, 
        redshift_host=REDSHIFT_HOST, 
        redshift_port=REDSHIFT_PORT, 
        redshift_db_name=REDSHIFT_DB_NAME
    )
    print("<---- Completed ---->")
except Exception as e:
    print(f"<---- An error has occured: {str(e)}")
