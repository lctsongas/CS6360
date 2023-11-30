import sqlglot, sqlite3
from sqlglot.optimizer import optimize
from sqlglot import transforms, exp

INSTANCE_ID = 'instance'
NAME_ID = 'name'
TRANSFORM_ID = 'transform_type'
EXPRESSION_ID = 'expression'
TRANSFORM_REMOVE = 'Remove'
TRANSFORM_INSERT = 'Insert'

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
    
    def remove(self, sqlglot_obj, instance_id, name_id):
        def remove_fun(node):
            if (isinstance(node, instance_id) and node.name == name_id):
                return None
            return node
        return sqlglot_obj.transform(remove_fun)
    
    def insert(self, sqlglot_obj, expression_id):
        sql_original = sqlglot_obj.sql()
        sqlglot_obj.append(expression_id.arg_key, expression_id.sql())
        sql_new = sqlglot_obj.sql()
        x = 1
        return sqlglot_obj

    def transform(self, sql_query_string, transform_func):
        sqlglot_obj = sqlglot.parse_one(sql_query_string)
        transform_type = transform_func[TRANSFORM_ID]
        new_sql_string = ''
        if (transform_type == TRANSFORM_REMOVE):
            new_sql_string = self.remove(sqlglot_obj, transform_func[INSTANCE_ID], transform_func[NAME_ID]).sql()
        if ( transform_type == TRANSFORM_INSERT):
            new_sql_string = self.insert(sqlglot_obj, transform_func[EXPRESSION_ID]).sql()
        return new_sql_string