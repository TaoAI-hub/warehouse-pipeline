from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from constants import DATABASE_URL, TABLE_NAME

def extract_all_user_data(database_url, table_name):
    try:
        print(f"Extracting all user data from {table_name}...")
        # SQLAlchemy engine connection string
        engine = create_engine(database_url)
        
        # Create a Session
        Session = sessionmaker(bind=engine)
        session = Session()

        # Fetch all records from the specified table
        select_query = text(f"SELECT * FROM {table_name}")
        print("Select query:", select_query)
        
        # Execute the query
        records = session.execute(select_query).fetchall()
        for record in records:
            print(record)

        # Close the session
        session.close()
        
        print("User data extraction completed.")
        return records
    except Exception as e:
        print(f"Error extracting user data: {e}")
        return []

# Use the function
all_user_data = extract_all_user_data(database_url=DATABASE_URL, table_name=TABLE_NAME)
