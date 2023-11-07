# SQLite is built-in to Python 3.11.5
import os, timeit, sqlite3
# pathlib used for reading in database files
from pathlib import Path
from base_db_builder import db_builder
import sqlglot

EXAMPLE_DATABASE_SCHEMA_FILE = 'base_database_schema.txt'
EXAMPLE_DATABASE_VALUES_FILE = 'base_database_values.txt'
EXAMPLE_DATABASE_QUERIES_FILE = 'base_database_queries.txt'

PROJECT_DATABASE_SCHEMA_FILE = '..\\sakila\\sakila-sqlite3-main\\source\\sqlite-sakila-schema.sql'
PROJECT_DATABASE_VALUES_FILE = '..\\sakila\\sakila-sqlite3-main\\source\\sqlite-sakila-insert-data.sql'
PROJECT_DATABASE_ORIGINAL_QUERIES_FILE = '..\\optimized_queries\\unoptimized_query.txt'
PROJECT_DATABASE_OPTIMIZED_QUERIES_FILE = '..\\optimized_queries\\optimized_query.txt'


class ClassExample(db_builder):
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
    def get_query_examples(self):
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

    
            
        
class ProjectExample(db_builder):
    # No need for init function, use db_builder's default
    
    """
    Creates base database used in project with all data and contraints
    Constraints, etc.
    """
    def initialize_default_database(self):
        if ( self.db_file != None):
            return
        # Statements below are good way to ensure any way you execute python will find the 
        # filepath and .txt file with-respect-to the python file running this function
        schema_path = os.path.join(os.path.dirname(__file__), PROJECT_DATABASE_SCHEMA_FILE)
        values_path = os.path.join(os.path.dirname(__file__), PROJECT_DATABASE_VALUES_FILE)
        # Call the parent class' Schema builder function
        self.initialize_database(schema_path)
        # Call the parent class' Values function
        self.add_values_to_database(values_path)

    """
    @return a list of SQL queries from EXAMPLE_DATABASE_QUERIES_FILE
    """
    def get_query_examples(self):
        original_queries_path = os.path.join(os.path.dirname(__file__), PROJECT_DATABASE_ORIGINAL_QUERIES_FILE)
        optimized_queries_path = os.path.join(os.path.dirname(__file__), PROJECT_DATABASE_OPTIMIZED_QUERIES_FILE)
        original_database_query_list = Path(original_queries_path).read_text()
        optimized_database_query_list = Path(optimized_queries_path).read_text()
        # split file into separate queries
        # NOTE: Add-in the ';' when executing the query
        # assumption: there are equal numbers in both optimized and unoptimized queries
        #    so query 1 matches optimized_query 1x, etc
        original_query_list_split = original_database_query_list.split(';')
        optimized_query_list_split = optimized_database_query_list.split(';')

        original_list = []
        optimized_list = []
        # add the semi-colon to each statement
        for original_query in original_query_list_split:
            original_list.append(original_query + ';')
        for optimized_query in optimized_query_list_split:
            optimized_list.append(optimized_query + ';')
        
        query_tuples = zip(original_list, optimized_list)
        
        return query_tuples
    
    """
    @param queries : list of tuples(original string,optimized string) queries to database

    @return list of tuples with 
      ( (original query, original result), (optimized query, optimized result) )
    """
    def run_queries(self, queries_list):
        original_query_result_list = []
        optimized_query_result_list = []
        self.latest_time_results = {}
        # cursor seems to be correct way to begin accessing SQLite DB
        # Reference: https://docs.python.org/3.8/library/sqlite3.html
        cur = self.db.cursor()
        # Iterate over the queries
        for original, optimized in queries_list:    
            # run the query and time it
            cur.execute(original)
            original_duration = timeit.timeit('cur.execute(original)', globals={'cur' : cur, 'original' : original}, number=10)
            self.latest_time_results[original] = original_duration
            # fetchall will return all rows from query (if any)
            result = cur.fetchall()
            original_query_result_list.append((original, result))

            # run the query and time it
            cur.execute(optimized)
            optimized_duration = timeit.timeit('cur.execute(optimized)', globals={'cur' : cur, 'optimized' : optimized}, number=10)
            self.latest_time_results[optimized] = optimized_duration
            
            # fetchall will return all rows from query (if any)
            result = cur.fetchall()
            optimized_query_result_list.append((optimized, result))
        # Close the cursor object. Seems correct based on documentation
        cur.close()
        return zip(original_query_result_list, optimized_query_result_list)