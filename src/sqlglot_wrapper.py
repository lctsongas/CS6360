import sqlglot

class sqlglot_wrapper:

    def __init__(self):
        return

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