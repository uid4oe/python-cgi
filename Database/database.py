from Database.create import create_tables
from Database.populate import populate_tables


# this script first creates tables and then populates them with sample data

def generate_database():
    try:
        create_tables()
        populate_tables()
    except:
        pass
