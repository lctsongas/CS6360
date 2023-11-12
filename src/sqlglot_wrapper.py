import sqlglot, sqlite3
from sqlglot.optimizer import optimize

class sqlglot_wrapper:

    def __init__(self):
        return

    # actor_schema = {"db" : {
    #     "actor" : {
    #         "actor_id" : "INT", 
    #         "first_name" : "STRING", 
    #         "last_name" : "STRING", 
    #         "last_update" : "STRING"
    #     },
    #     "country" :{
    #         "country_id" : "INT",
    #         "country" : "STRING",
    #         "last_update" : "STRING"
    #     },
    #     }}
    #def import_db(self, db):

    """
    @param : sql_query_string = single-string SQL query
    Steps done:
     - checks syntax of statement
     - translates statement to sqlite 
    @return :  
    """
    def analyze_query(self, sql_query_string):
        try:
            sql = sqlglot.transpile(sql_query_string, None, 
                sqlglot.Dialects.SQLITE, True, sqlglot.ErrorLevel.WARN)
            return sqlglot.parse_one(sql[0], read=sqlglot.Dialects.SQLITE)
        except sqlglot.ParseError as e:
            return str(e.errors)

    def optimize_query(self, sql_query_string, schema):

        try:
            sql = sqlglot.transpile(sql_query_string, None, 
                sqlglot.Dialects.SQLITE, True, sqlglot.ErrorLevel.WARN)
            return optimize(sqlglot.parse_one(sql[0], read=sqlglot.Dialects.SQLITE),schema)
        except sqlglot.ParseError as e:
            return str(e.errors)

    def diff(self, sqlglot_query, sql_goal_query):
        try:
            sql_goal = sqlglot.transpile(sql_goal_query, None, 
                sqlglot.Dialects.SQLITE, True, sqlglot.ErrorLevel.WARN)
            sql_glot = sqlglot.transpile(sqlglot_query, None, 
                sqlglot.Dialects.SQLITE, True, sqlglot.ErrorLevel.WARN)
            return sqlglot.diff(sqlglot.parse_one(sql_goal[0]), sqlglot.parse_one(sql_glot[0]))
        except sqlglot.ParseError as e:
            return str(e.errors)
