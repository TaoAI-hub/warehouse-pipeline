from sqlalchemy import create_engine, MetaData

# local imports
from constants import DATABASE_URL


engine = create_engine(DATABASE_URL)
metadata = MetaData()

# Reflect the schema from the database
metadata.reflect(bind=engine)

# Iterate over all tables and print their names and column details
for table in metadata.tables.values():
    print(f"Table: {table.name}")
    for column in table.c:
        print(f"  {column.name}: {column.type}")
