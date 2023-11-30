# SQLite is built-in to Python 3.11.5
import sqlite3, sys, collections
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
    idx = 0
    for original, optimized in query_result_list:
        analyzer_obj = query_object(original[0], optimized[0])
        analyzer_obj.sqlglot_optimize(database)
        #analyzer_obj.sqlglot_transform()
        #print(analyzer_obj.steps_to_match_goal_string)
        print('Query ' + str(idx))
        print('  ORIGINAL TIME: ' + str(database.latest_time_results[original[0]]))
        print('  OPTIMIZE TIME: ' + str(database.latest_time_results[optimized[0]]))
        # Ayo
        # This is a list of transformations to get from goal to optimized
        for step in analyzer_obj.steps_to_match_goal_string:
            # There are a lot of items we do NOT need to change so skip printing those
            if ( 'Keep' in str(step)):
                continue
            else:
                if ( 'Remove' in str(step)):
                    # do somethin
                    analyzer_obj.sqlglot_remove(step)
                elif ( 'Insert' in str(step)):
                    # do somethin
                    analyzer_obj.sqlglot_insert(step)
                else:
                    print(step)
            # uncomment for lots of print statements
            #print(step)
        result = begin_query_manipulation(analyzer_obj, 1000)
        idx += 1
        f = open("example.txt", "w")
        print(str(analyzer_obj), file=f)
        f.close()
        #return


def begin_query_manipulation(analyzer, iterations=100):
    result = False
    for i in range(iterations):
        query_aliases = analyzer.aliases
        goal_aliases = analyzer.goal_aliases
        # base-case check
        if ( analyzer.compare() == 1.0 ):
            if ( i == 0 ):
                print('  Basic translations and JOIN optimizations done to match goal query!')
            print('  SQL query optimized! Steps taken')
            print('    Steps:')
            for matching, step in analyzer.new_commit:
                print('    Step ' + str(i) + ' match to goal: %' + str(matching*100))
                print('    ' + step[0:10] + '...' + step[-10:])
                i+=1

            break
        if ( len(analyzer.steps_to_match_goal_string) != 0 ):
            for idx, step in enumerate(analyzer.steps_to_match_goal_string):
                if ( 'Keep' in str(step) or 'Move' in str(step)):
                    break
            analyzer.steps_to_match_goal_string = analyzer.steps_to_match_goal_string[0:idx-1]
            for step in analyzer.steps_to_match_goal_string[:-1]:
                matching = analyzer.new_commit[i][0]
                print('    Step ' + str(i) + ' match to goal: %' + str(matching*100))
                print('      ' + str(step)[0:50] + '...')
                i+=1
            matching = 1.0
            step = analyzer.steps_to_match_goal_string[-1]
            print('    Step ' + str(i) + ' match to goal: %' + str(matching*100))
            print('      ' + str(step)[0:50] + '...')
            break
                
        # the aliases are output in-order based on DFS search
        # so compare the two and decide if we need to simply
        # TRNASLATE the query
        if ( check_for_translations(query_aliases, goal_aliases) ):
            # we have a 1:1 mapping of aliases but they may be out of order.
            # manipulate the query to match the goal
            print("Query can be optimized by TRANSLATION property...")
            original_matching_flt = analyzer.compare()
            original_matching = '{:.2%}'.format(original_matching_flt)
            analyzer.translate_aliases()
            translated_matching_flt = analyzer.get_recent_commit()[0]
            translated_matching = '{:.2%}'.format(translated_matching_flt)
            print("    Original Query Match to goal: " + original_matching)
            print("  Translated Query Match to goal: " + translated_matching)
            if ( translated_matching_flt > original_matching_flt ):
                analyzer.commit()
            else:
                print("    Translation not optimal. NO TRANSLATION")
        else:
            print("Query cannot be optimized by TRANSLATION")
    return result

def check_for_translations(aliases_a, aliases_b):
    if (aliases_a == aliases_b):
        count = 0
        for ka, kb in zip(aliases_a.keys(), aliases_b.keys()):
            if ( ka == kb ):
                count += 1
        if ( count != len(aliases_a)):
            return True
    return False



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
