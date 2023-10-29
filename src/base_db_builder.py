import sys, os, sqlite3
# pathlib used for reading in database files
from pathlib import Path
import sqlglot

class db_builder:
    """
    Base constructor class for all databases. 
    Also can be used to take any db and compare to others
    with common functions
    """
    def __init__(self, database_file = None):
        # Using :memory: keyword so database ONLY exists
        # in RAM. This will avoid issues when storing class
        # database in actual memory and opening multiple times
        # This also means you can have multiple instances of the
        # class database so be mindful of that!
        if ( database_file != None):
            self.db = sqlite3.connect(database_file)
        else:    
            self.db = sqlite3.connect(':memory:')
        self.db_file = database_file
    
    
    """
    @param path_to_db_file : direct,full file-path to a .txt file of 
        commands that create the database structure
    @return : True if successful
    """
    def initialize_database(self, path_to_schema_file):
        try:
            # cursor seems to be correct way to begin accessing SQLite DB
            # Reference: https://docs.python.org/3.8/library/sqlite3.html
            cur = self.db.cursor()
            # read in the file as a whole
            database_schema_in_text = Path(path_to_schema_file).read_text()
            # Will use the executescript function to build entire table
            # by reading in the file path_to_db_file
            cur.executescript(database_schema_in_text)
            # Commit the db so our changes are seen by references
            self.db.commit()
            # Close the cursor object. Seems correct based on documentation
            cur.close()
            return True
        except Exception as e:
            print("Error in reading/parsing the SCHEMA...")
            print(e)
            sys.exit(0)
            return False


    """
    @param path_to_values_file : direct,full file-path to a .txt file of
        data-manupulation SQL statements to add values to the database
    @param return : True if successful
    """
    def add_values_to_database(self, path_to_values_file):
        try:
            # cursor seems to be correct way to begin accessing SQLite DB
            # Reference: https://docs.python.org/3.8/library/sqlite3.html
            cur = self.db.cursor()
            # read in the file as a whole
            database_values_in_text = Path(path_to_values_file).read_text()
            # Will use the executescript function to build entire table
            # by reading in the file path_to_db_file
            cur.executescript(database_values_in_text)
            # Commit the db so our changes are seen by references
            self.db.commit()
            # Close the cursor object. Seems correct based on documentation
            cur.close()
            return True
        except Exception as e:
            print("Error in adding VALUES to the database...")
            print(e)
            sys.exit(0)
            return False

    """
    @return the sqlite3.connect object (aka the database)
    """
    def get_db(self):
        return self.db

    
    """
    @param queries : list of string queries to database

    @return list of tuples with (query, result)
    """
    def run_queries(self, queries_list):
        query_result_list = []
        # cursor seems to be correct way to begin accessing SQLite DB
        # Reference: https://docs.python.org/3.8/library/sqlite3.html
        cur = self.db.cursor()
        # Iterate over the queries
        for query in queries_list:    
            # run the query
            cur.execute(query)
            # fetchall will return all rows from query (if any)
            result = cur.fetchall()
            query_result_list.append((query, result))
        # Close the cursor object. Seems correct based on documentation
        cur.close()
        return query_result_list