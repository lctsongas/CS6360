from difflib import SequenceMatcher
from sqlglot_wrapper import sqlglot_wrapper
import re

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

    TABLE_AND_ALIAS_REGEX = "TABLE this: \(IDENTIFIER this: [a-zA-Z_0-9]*, quoted: (False|True)\), alias: \(TABLEALIAS this: \(IDENTIFIER this: [a-zA-Z_0-9]*, quoted: (False|True)\)\)"
    

    def __init__(self, query_str, goal_str = None):
        self.query_string = ' '.join(repr(sql_wrapper.analyze_query(query_str)).split())
        if ( goal_str != None):
            self.goal_string = ' '.join(repr(sql_wrapper.analyze_query(goal_str)).split())
        
        self.query_tree = self.create_flat_tree(self.query_string)

        self.family_tree = self.create_family_tree(self.query_tree)
        self.aliases = self.get_aliases(self.family_tree)

    """
    @param tree_obj : a sql_query_wrapper.Tree object root node 
    @return a dictionary of aliases in the format of: { alias : object }
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
            # Regex expressions used here to mark the table aliases



    def compare(self, other):
        if not isinstance(other, query_object):
            return NotImplemented
        else:
            return SequenceMatcher(None, self.query_string, other.query_string).ratio()
    
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
