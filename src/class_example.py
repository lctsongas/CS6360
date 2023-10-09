# SQLite is built-in to Python 3.11.5
import os, sqlite3
# pathlib used for reading in database files
from pathlib import Path

EXAMPLE_DATABASE_SCHEMA_FILE = 'base_database_schema.txt'
EXAMPLE_DATABASE_VALUES_FILE = 'base_database_values.txt'
EXAMPLE_DATABASE_QUERIES_FILE = 'base_database_queries.txt'

class Example:
    """
    # Using :memory: keyword so database ONLY exists
    # in RAM. This will avoid issues when storing class
    # database in actual memory and opening multiple times
    # This also means you can have multiple instances of the
    # class database so be mindful of that!
    """
    def __init__(self):
        self.company_db = sqlite3.connect(':memory:')

    """
    Creates base database used in class with all names, SSNs,
    Constraints, etc.
    """
    def initialize_default_database(self):
        # cursor seems to be correct way to begin accessing SQLite DB
        # Reference: https://docs.python.org/3.8/library/sqlite3.html
        cur = self.company_db.cursor()
        # Will use the executescript function to build entire table
        # by reading in the file EXAMPLE_DATABASE_SCHEMA_FILE
        schema_path = os.path.join(os.path.dirname(__file__), EXAMPLE_DATABASE_SCHEMA_FILE)
        database_schema_in_text = Path(schema_path).read_text()
        cur.executescript(database_schema_in_text)
        # read in the values to initialize default data from
        # file EXAMPLE_DATABASE_VALUES_FILE
        values_path = os.path.join(os.path.dirname(__file__), EXAMPLE_DATABASE_VALUES_FILE)
        database_values_in_text = Path(values_path).read_text()
        cur.executescript(database_values_in_text)
        # Commit the db so our changes are seen by references
        self.company_db.commit()
        # Close the cursor object. Seems correct based on documentation
        cur.close()

    """
    @return the sqlite3.connect object (aka the database)
    """
    def get_db(self):
        return self.company_db


    """
    @return a list of SQL queries from EXAMPLE_DATABASE_QUERIES_FILE
    """
    def get_class_query_examples(self):
        queries_path = os.path.join(os.path.dirname(__file__), EXAMPLE_DATABASE_QUERIES_FILE)
        database_query_list = Path(queries_path).read_text()
        # split file into separate queries
        # NOTE: Add-in the ';' when executing the query
        query_list_split = database_query_list.split(';')
        query_list = []
        # add the semi-colon to each statement
        for query in query_list_split:
            query_list.append(query + ';')
        return query_list

    """
    @return list of tuples with (query, result)
    """
    def run_queries(self):
        query_result_list = []
        # Read in the whole file
        database_query_list = self.get_class_query_examples()
        # Iterate over the queries
        for query in database_query_list:
            cur = self.company_db.cursor()
            # run the query
            cur.execute(query)
            # fetchall will return all rows from query (if any)
            result = cur.fetchall()
            query_result_list.append((query, result))
        return query_result_list
            
        
        
        
    
