# SQLite is built-in to Python 3.11.5
import sqlite3, sys
from database_wrapper import *
from sql_query_wrapper import query_object
import sqlglot_wrapper as sqlanalyzer
"""
# Main function that we should alter depending on what we want to do.
# Set the _Switch you want enabled to True and disable by False
# Running Class_Example will load up the default DB we are using in-class
# Running Class_Query will read the sql_queries.txt and return the results
"""
def main():
    Class_Run_Query = False
    Class_Query_Analyzer = False

    Project_Run_Query = True
    Project_Query_Analyzer = True

    database_object = None
    # Only create Class/Textbook example database if required
    if ( Class_Run_Query or
         Class_Query_Analyzer ):
        database_object = run_class_example_create()
        
        
    if Class_Run_Query:
        run_class_queries(database_object)
    
    if Class_Query_Analyzer:
        run_class_analyzer(database_object)

    # Only create Project example database if required
    if ( Project_Run_Query or 
         Project_Query_Analyzer):
        database_object = run_project_example_create()
    
    if Project_Run_Query:
        run_project_queries(database_object)

    if Project_Query_Analyzer:
        run_project_analyzer(database_object)
    

"""
@param database : project_example.py->VHS_Example object
Run the optimized and unoptimized queries and compare execution times
"""
def run_project_queries(database):
    query_result_list = database.run_queries(database.get_query_examples())
    f = open("output.txt", "w")
    #f = sys.stdout
    for original, optimized in query_result_list:
        print('ORIGINAL QUERY:', file=f)
        print(original[0].strip(), file=f)
        print('\n', file=f)
        print('OPTIMIZED QUERY:', file=f)
        print(optimized[0].strip(), file=f)
        print('\n', file=f)
        match = "NOT EQUIVALENT RESULT!"
        if ( original[1] == optimized[1] ):
            match = ""
        print('RESULT:' + match, file=f)
        # some results may be multiple rows so print out individually
        for row in original[1]:
            print(row, file=f)
        print('\n', file=f)
        print('#########################################', file=f)
    f.close()

"""
@param database : project_example.py->VHS_Example object
Repeats the steps done in run_project_queries but does 
query manipulation to try and match optimized query
"""
def run_project_analyzer(database):
    query_result_list = database.run_queries(database.get_query_examples())
    for original, optimized in query_result_list:
        analyzer_obj = query_object(original[0], optimized[0])
        result = begin_query_manipulation(analyzer_obj, 1000)
        f = open("example.txt", "w")
        print(str(analyzer_obj), file=f)
        f.close()
        return


def begin_query_manipulation(analyzer, iterations=100):
    result = False
    #analyzer.query_tree.sort(key=lambda x: x[0])
    for i in range(iterations):
        if(len(analyzer.query_tree) > i):
            print(analyzer.query_tree[i])
    return result




"""        
# Setup Example Relationship Database from class as example
@return database_wrapper.ClassExample object
"""
def run_class_example_create():
    # Call __init__ function here so x = Object reference
    # x is not a SQLite DB that exists ONLY in RAM
    x = ClassExample()
    # Create the basic Schema and values for the database
    x.initialize_default_database()
    # pass-back the Example database object fully created
    return x

"""        
# Setup Example Relationship Database from project
@return database_wrapper.ProjectExample object
"""
def run_project_example_create():
    # Call __init__ function here so x = Object reference
    # x is not a SQLite DB that exists ONLY in RAM
    db_path = os.path.join(os.path.dirname(__file__), "../sakila/sakila-sqlite3-main/sakila_master.db")
    x = ProjectExample(db_path)
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
    query_result_list = database.run_queries(database.get_query_examples())
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
        analyzed_query = analyzer.analyze_query(query)
        print(repr(analyzed_query))
        print('#####################################')
        print('')

    




# main function main entry-point to the file when executed
if __name__ == "__main__":
    main()
