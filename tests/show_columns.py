from sqlalchemy import create_engine, inspect
import uuid
from sqlalchemy.dialects.postgresql import UUID, VARCHAR, TIMESTAMP, BOOLEAN
import psycopg2
from psycopg2.extensions import AsIs

def ensure_uuid_extension(connection):
    cursor = connection.cursor()
    cursor.execute("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";")
    connection.commit()
    cursor.close()

def insert_records_to_table(connection, table_name, productname, records):
    """
    Inserts records into a specified table.

    :param connection: A psycopg2 connection object to the database.
    :param table_name: The name of the table where records will be inserted.
    :param records: A list of tuples, where each tuple represents a record to insert.
    """
    cursor = connection.cursor()

    if records:
        # Dynamically generate the placeholders for the values (%s, %s, ...)
        placeholders = ', '.join(['%s'] * len(records[0]))
        
        # Quote the table name in the INSERT query
        insert_query = f'INSERT INTO "{productname}_{table_name}" VALUES ({placeholders})'

        for record in records:
            # Ensure all UUIDs (or any other special types) are converted to strings
            record = tuple(str(value) if isinstance(value, uuid.UUID) else value for value in record)

            try:
                cursor.execute(insert_query, record)
            except Exception as e:
                print(f"Error inserting record: {e}")
                connection.rollback()  # Rollback the transaction for this record
                continue  # Skip to the next record

        connection.commit()  # Commit the transaction if all inserts succeed
    cursor.close()

    
def generate_create_table_statement(database_url, table_name, productname):
    # Create an engine
    engine = create_engine(database_url)

    # Create an inspector object
    inspector = inspect(engine)

    # Retrieve the columns of the table
    columns = inspector.get_columns(table_name)

    # Start constructing the CREATE TABLE statement, ensuring the table name is quoted if it's a reserved keyword
    create_table_statement = f'CREATE TABLE "{productname}_{table_name}" (\n'

    for column in columns:
        col_name = column['name']
        col_type = column['type']

        # Convert UUID type to VARCHAR
        if str(col_type).lower() == 'uuid':
            col_type = "VARCHAR(36)"  # UUIDs are 36 characters long including hyphens

        # For other types, maintain their definitions, possibly adjusting for specific needs
        elif isinstance(col_type, VARCHAR):
            col_type = "VARCHAR"
        elif isinstance(col_type, TIMESTAMP):
            col_type = "TIMESTAMP"
        elif isinstance(col_type, BOOLEAN):
            col_type = "BOOLEAN"
        else:
            col_type = str(col_type).upper()

        # Quote column names and construct the column definition part of the statement
        create_table_statement += f'    "{col_name}" {col_type},\n'

    # Remove the last comma and add closing parenthesis
    create_table_statement = create_table_statement.rstrip(',\n') + '\n);'

    # Close the engine
    engine.dispose()
    print("<--- create table statement ---> \n", create_table_statement)

    return create_table_statement

def create_table(connection, query):
    try:
        # ensure_uuid_extension(connection)
        create_table_query = query
        cursor = connection.cursor()
        cursor.execute(create_table_query)
        connection.commit()
        cursor.close()
        print("Table created.")
    except Exception as e:
        print(f"Error creating table: {e}")
