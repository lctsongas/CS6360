# SQLite is built-in to Python 3.11.5
import sqlite3
from class_example import Example
import sqlglot_wrapper as sqlanalyzer
"""
# Main function that we should alter depending on what we want to do.
# Set the _Switch you want enabled to True and disable by False
# Running Class_Example will load up the default DB we are using in-class
# Running Class_Query will read the sql_queries.txt and return the results
"""
def main():
    Class_Example_Switch = True
    Class_Query_Switch = True
    Class_Query_Analyzer = True

    tmp_example = Example()
    if ( Class_Example_Switch ):
        # Read the function below and checkout class_example.py->initialize_default_database
        # Note: tmp_example is empty if Class_Example_Switch = False
        tmp_example = run_class_example_create()
        
    if ( Class_Query_Switch ):
        # Basic warning will print if Class_Query_Switch is run
        # WITHOUT Class_Example_Switch is not enabled. It is valid,
        # but may not be what you want.
        if ( Class_Example_Switch == False ):
            print('WARNING: Queries are running on EMPTY DATABASE\n')
        run_class_queries(tmp_example)
    
    if ( Class_Query_Analyzer ):
        run_class_analyzer(tmp_example)

"""        
# Setup Example Relationship Database from class as example
@return class_example.Example object
"""
def run_class_example_create():
    # Call __init__ function here so x = Object reference
    # x is not a SQLite DB that exists ONLY in RAM
    x = Example()
    # Create the basic Schema and values for the database
    x.initialize_default_database()
    # pass-back the Example database object fully created
    return x
    

"""
@type database : class_example.py->Example object
@param database : class_example.py->Example object from whatever db was initialized
Function will split each query based on the ';' at the end of a query
NOTE: Do not run ALTER/DELETE/UPDATE/ETC. This is for QUERIES
@return list of tuples where each tuple is (query string, result string)
"""
def run_class_queries(database):
    query_result_list = database.run_queries(database.get_class_query_examples())
    for query, result in query_result_list:
        print('QUERY:')
        print(query.strip())
        print('\n')
        print('RESULT:')
        # some results may be multiple rows so print out individually
        for row in result:
            print(row)
        print('\n')
    
    

def run_class_analyzer(database):
    analyzer = sqlanalyzer.sqlglot_wrapper()
    list_of_queries = database.get_class_query_examples()
    for query in list_of_queries:
        print('Query: ')
        print(query.strip())
        print('')
        print('Expression: ')
        print(repr(analyzer.analyze_query(query)))
        print('#####################################')
        print('')

    




# main function main entry-point to the file when executed
if __name__ == "__main__":
    main()
