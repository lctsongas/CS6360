# SQLite is built-in to Python 3.11.5
import os, sqlite3
# pathlib used for reading in database files
from pathlib import Path
from base_db_builder import db_builder

EXAMPLE_DATABASE_SCHEMA_FILE = 'base_database_schema.txt'
EXAMPLE_DATABASE_VALUES_FILE = 'base_database_values.txt'
EXAMPLE_DATABASE_QUERIES_FILE = 'base_database_queries.txt'

class Example(db_builder):
    # No need for init function, use db_builder's default

    """
    Creates base database used in class with all names, SSNs,
    Constraints, etc.
    """
    def initialize_default_database(self):
        # Statements below are good way to ensure any way you execute python will find the 
        # filepath and .txt file with-respect-to the python file running this function
        schema_path = os.path.join(os.path.dirname(__file__), EXAMPLE_DATABASE_SCHEMA_FILE)
        values_path = os.path.join(os.path.dirname(__file__), EXAMPLE_DATABASE_VALUES_FILE)
        # Call the parent class' Schema builder function
        self.initialize_database(schema_path)
        # Call the parent class' Values function
        self.add_values_to_database(values_path)

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

    
            
        
        
        
    
