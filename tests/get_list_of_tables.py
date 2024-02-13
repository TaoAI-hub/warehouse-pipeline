from sqlalchemy import create_engine, inspect
from constants import DATABASE_URL

def list_db_tables(database_url):
    # Replace with your PostgreSQL connection details
    DATABASE_URL = database_url
    engine = create_engine(DATABASE_URL)

    # Create an inspector
    insp = inspect(engine)

    # Get list of tables
    table_names = insp.get_table_names()
    print("Tables in the database:")
    for table in table_names:
        print(table)

    # Close the connection
    engine.dispose()

# Execute the function to list tables
list_db_tables(DATABASE_URL)
