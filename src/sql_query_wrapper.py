from difflib import SequenceMatcher
from sqlglot_wrapper import *
import re, sqlite3

sql_wrapper = sqlglot_wrapper()
DEPTH_INDEX = 0
VALUE_INDEX = 1
LAST_VALUE_IN_LIST = -1
class Tree:
    
    def __init__(self, tree_tuple):
        self.children = []
        self.depth = tree_tuple[DEPTH_INDEX]
        self.value = tree_tuple[VALUE_INDEX]
    
    def add_child(self, tree_elem):
        if ( tree_elem.depth -1 == self.depth ):
            self.children.append(tree_elem)
        else:
            self.children[LAST_VALUE_IN_LIST].add_child(tree_elem)

    """
    @param bfs : Set to True when using Breadth-first traversal
                 Set to False for Depth-first traversal
    @return list of elements in dfs or bfs ordering"""
    def traverse(self, bfs=True):
        # recursion check on base-case (leaf node)
        if ( len(self.children) == 0 ):
            return [(self.depth, self.value)]
        else:
            family = []
            for idx in range(len(self.children)):
                siblings = self.children[idx].traverse(bfs)
                family.extend(siblings)
            if ( bfs ):
                family.insert(0, (self.depth, self.value))
            else:
                family.append((self.depth, self.value))
            return family
                
        
    
    def __repr__(self, depth=0):
        ret = "\t"*depth+repr(self.value)+"\n"
        for child in self.children:
            ret += child.__repr__(depth+1)
        return ret
    
class query_object:

    TABLE_AND_ALIAS_REGEX = r"TABLE this: \(IDENTIFIER this: [a-zA-Z_0-9]*, quoted: (False|True)\), alias: \(TABLEALIAS this: \(IDENTIFIER this: [a-zA-Z_0-9]*, quoted: (False|True)\)\)"
    

    def __init__(self, query_str, goal_str):
        self.sql_goal_string = goal_str
        self.goal_string = ' '.join(repr(sql_wrapper.analyze_query(goal_str)).split())
        self.create_goal_objects()

        self.sql_query_string = query_str
        self.query_string = ' '.join(repr(sql_wrapper.analyze_query(query_str)).split())
        self.create_query_objects()

        self.new_commit = []  
        self.modified_query_string = [self.query_string]
    
    def create_goal_objects(self):
        self.goal_query_tree = self.create_flat_tree(self.goal_string)
        self.goal_family_tree = self.create_family_tree(self.goal_query_tree)
        self.goal_aliases = self.get_aliases(self.goal_family_tree)

    def create_query_objects(self):
        self.query_tree = self.create_flat_tree(self.query_string)
        self.family_tree = self.create_family_tree(self.query_tree)
        self.aliases = self.get_aliases(self.family_tree)
    
    def sqlglot_remove(self, AST_step):
        AST_step_str = str(AST_step).split('Remove(expression=')[1][:-1]
        AST_step_str = ' '.join(AST_step_str.split())
        new_modified_query_string = []
        old_modified_query_string = list(self.modified_query_string)
        for idx in enumerate(old_modified_query_string):
            idx = idx[0]
            if ( AST_step_str in old_modified_query_string[idx] ):
                new_modified_query_string.extend(old_modified_query_string[idx].split(AST_step_str))
            else:
                new_modified_query_string.append(old_modified_query_string[idx])
        self.modified_query_string = new_modified_query_string
        self.add_commit(''.join(self.modified_query_string))
        return self.modified_query_string
    
    def sqlglot_insert(self, AST_step):
        AST_step_str = str(AST_step).split('Insert(expression=')[1][:-1]
        AST_step_str = ' '.join(AST_step_str.split())
        new_modified_query_string = []
        old_modified_query_string = list(self.modified_query_string)
        if ( len(old_modified_query_string) < 2):
            print('Issue!')
            return None
        else:
            new_element = old_modified_query_string[-2] + AST_step_str + old_modified_query_string[-1]
            if ( len(old_modified_query_string) != 2 ):
                new_modified_query_string.extend(old_modified_query_string[:-2])
                new_modified_query_string.append(new_element)
                
                self.modified_query_string = new_modified_query_string
                self.add_commit(''.join(self.modified_query_string))
            else:
                new_modified_query_string.append(new_element)
                self.query_string = new_modified_query_string[0]
                self.modified_query_string = new_modified_query_string[0]
                self.add_commit(''.join(self.modified_query_string))
                self.commit()

            return self.modified_query_string

    def sqlglot_transform(self):
        new_sql_query_string = self.sql_query_string
        for step in self.steps_to_match_goal_string:
            transform_step = {
                INSTANCE_ID : None,
                NAME_ID : None,
                TRANSFORM_ID : None,
                EXPRESSION_ID : None
            }
            if ( TRANSFORM_REMOVE in str(step) ):
                transform_step[TRANSFORM_ID] = TRANSFORM_REMOVE
            if ( TRANSFORM_INSERT in str(step) ):
                transform_step[TRANSFORM_ID] = TRANSFORM_INSERT
            transform_step[INSTANCE_ID] = type(step.expression)
            transform_step[NAME_ID] = step.expression.name
            transform_step[EXPRESSION_ID] = step.expression
            new_sql_query_string = sql_wrapper.transform(new_sql_query_string, transform_step)
        return None

    def sqlglot_optimize(self, database):
        db = database.get_db()
        db.row_factory = sqlite3.Row
        cur = db.cursor()
        cur.execute("SELECT * FROM sqlite_master WHERE type='table'")
        result = [dict(row) for row in cur.fetchall()]
        tables = {}
        for i in result:
            tableName=i['name']
            columnQuery = "PRAGMA table_info('%s')" % tableName
            cur.execute(columnQuery)
            tables[tableName] = dict([(col['name'], col['type']) for col in cur.fetchall()])
            # Sanitize the types
            sanitize_to = {'numeric' : 'INT',
                           'INT' : 'INT',
                           'VARCHAR' : 'STIRNG',
                           'TIMESTAMP' : 'STRING',
                           'CHAR' : 'STRING',
                           'BLOBSUBTYPETEXT' : 'STRING',
                           'BLOB' : 'STRING',
                           'DECIMAL' : 'DOUBLE',
                           'SMALLINT' : 'INT'}
            for column in tables[tableName].keys():
                original_type = tables[tableName][column]
                original_type = re.sub('[^a-zA-Z]+', '', original_type)
                y = sanitize_to[original_type]
                tables[tableName][column] = sanitize_to[original_type]
        dict_db = {'db' : tables}
        sqlglot_optimized = sql_wrapper.optimize_query(self.sql_query_string, dict_db)
        sql_diff = sql_wrapper.diff(str(sqlglot_optimized), self.sql_goal_string)
        sql_query_to_goal = sql_wrapper.diff(self.sql_goal_string, self.sql_query_string)
        self.steps_to_match_goal_string = sql_query_to_goal

        

    """
    @param tree_obj : a sql_query_wrapper.Tree object root node 
    @return a dictionary of aliases in the format of: { alias : table name }
    """
    def get_aliases(self, tree_obj):
        aliases = {}
        alias_re = re.compile(self.TABLE_AND_ALIAS_REGEX)
        for node in tree_obj.traverse(bfs=False):
            if ( alias_re.match(node[VALUE_INDEX]) ):
                node_split = node[VALUE_INDEX].split(" ")
                table_alias = node_split[12].replace(',', '')
                table = node_split[4].replace(',', '')
                aliases[table_alias] = table
        return aliases

    """
    Calling this will have query identify all alises and move them around the 
    tree to match the goal_query
    """
    def translate_aliases(self):
        regex_iter = re.finditer(self.TABLE_AND_ALIAS_REGEX, self.query_string, re.MULTILINE)
        goal_iter = re.finditer(self.TABLE_AND_ALIAS_REGEX, self.goal_string, re.MULTILINE)
        query_alias_ordering = [item for item in regex_iter]
        goal_alias_ordering = [item for item in goal_iter]
        ordering = []
        compiled_regex_str = r''
        spacer_idx = 2
        # Identify the goal ordering and save into ordering 
        for goal_match in goal_alias_ordering:
            for item_idx, item in enumerate(query_alias_ordering):
                if goal_match.group() == item.group():
                    ordering.append((2*item_idx)+1)
                    ordering.append(spacer_idx)
                    spacer_idx += 2
        compiled_regex_str = r''
        for query_match in query_alias_ordering:
            compiled_regex_str += '(' + query_match.group().replace('(','\(').replace(')','\)') + ')(.*)'
        # create the new ordering regex substring
        ordering_regex_str = r''
        for o in ordering:
            ordering_regex_str += '\\' + str(o)
        compiled_regex = re.compile(compiled_regex_str)
        translated_query = compiled_regex.sub(ordering_regex_str, self.query_string)
        self.add_commit(translated_query)
    
    def add_commit(self, updated_query):
        new_commit_match = self.compare(x=updated_query)
        self.new_commit.append((new_commit_match, updated_query))
    
    def get_recent_commit(self):
        return self.new_commit[-1]
    
    def commit(self):
        self.query_string = self.new_commit[LAST_VALUE_IN_LIST][VALUE_INDEX]
        self.create_query_objects()
        
        

    """
    @param x : string or query_object in sqlglot representation. If left as None, then compares to own goal string
    @param y : requires x to be populated, will compare x to y instead of to the calling object's information

    @return : float between [0,1.0] which is percent matching the compared object
    """
    def compare(self, x=None, y=None):
        if ( x == None):
            x = y
            y = None
        a = not isinstance(x, query_object)
        b = not isinstance(x, str)
        c = x != None
        if ((not isinstance(x, query_object) and not isinstance(x, str)) and (x != None)):
            return NotImplemented
        # x XOR y -> covers 1,0 and 0,1 cases
        elif (x != None and y == None):
            if ( isinstance(x, query_object) ):
                return SequenceMatcher(None, self.goal_string, x.query_string).ratio()
            if ( isinstance(x, str) ):
                return SequenceMatcher(None, self.goal_string, x).ratio()
        # x_bar AND y_bar -> covers 0,0 case
        elif ( x == None and y == None):
            return SequenceMatcher(None, self.query_string, self.goal_string).ratio()
        # last case covered 1,1
        else:
            if ( isinstance(x, query_object) ):
                return SequenceMatcher(None, x.query_string, y.query_string).ratio()
            if ( isinstance(x, str) ):
                return SequenceMatcher(None, x, y).ratio()
    
    """
    @param query_str is a repr(sqlglot) object format
    @return Creates a 'tree' structure based on the parenthesis in the repr-string
    """
    def create_flat_tree(self, query_str):
        lifo = []
        new_query_tree = []
        for idx, char in enumerate(query_str):
            if ( char == '(' ):
                lifo.append(idx)
            elif ( char == ')' and len(lifo) != 0 ):
                sub_str = query_str[lifo.pop()+1:idx]
                new_query_tree.append((len(lifo), sub_str))
        return new_query_tree

    """
    Used to establish parent-child relationship
    create_flat_tree traverses by depth-first-search. Exploiting this allows to know children are visited
    BEFORE parents. 

    So: 
    so going through list created BACKWARDS would mean we encounter ROOT node first
    then the first sibling each time
    """
    def create_family_tree(self, dfs_tree):
        # No parent stop all calculations
        if ( len(dfs_tree) == 0  ):
            return None
        new_tree = Tree(dfs_tree[LAST_VALUE_IN_LIST])
        for elem in reversed(dfs_tree[:LAST_VALUE_IN_LIST]):
            child = Tree(elem)
            new_tree.add_child(child)
        return new_tree


    def __repr__(self):
        return repr(self.family_tree)

    def __str__(self):
        return self.query_string.replace('\n', '') + \
        '\n' + self.goal_string .replace('\n','')



    """ x > y """
    def __lt__(self, other):
        if ( not isinstance(other, query_object)):
            return NotImplemented
        else:
            # x and y are equal. Is not less than
            if ( self.goal_string == None and other.goal_string == None):
                return False
            # x is None, y is something so x IS LESS THAN y
            elif ( self.goal_string == None):
                return True
            # x is something, y is None. x IS GREATER THAN y
            elif ( other.goal_string == None):
                return False
            else:
                return self.compare(self.goal_string) > other.compare(other.goal_string)
    
    """ x < y """
    def __gt__(self, other):
        return not self.__lt__(other)
    
    """ x >= y """
    def __le__(self, other):
        return self.__lt__(other) or self.__eq__(other)

    """ x != y """
    def __ne__(self, other):
        return not self.__eq__(other)
    
    """ x == y """
    def __eq__(self, other):
        if not isinstance(other, query_object):
            return NotImplemented
        else:
            return self.query_string == other.query_string

    """ x <= y """
    def __ge__(self, other):
        return self.__gt__(other) or self.__eq__(other)
