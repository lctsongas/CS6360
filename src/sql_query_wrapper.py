from difflib import SequenceMatcher

class query_object:

    def __init__(self, query_str, goal_str = None):
        self.query_string = query_str
        self.goal_string = goal_str
        self.create_flat_tree(query_str)

    def compare(self, other):
        if not isinstance(other, query_object):
            return NotImplemented
        else:
            return SequenceMatcher(None, self.query_string, other.query_string).ratio()
    
    def create_flat_tree(self, query_str):
        lifo = []
        self.query_tree = []

        for idx, char in enumerate(query_str):
            if ( char == '(' ):
                lifo.append(idx)
            elif ( char == ')' and len(lifo) != 0 ):
                sub_str = query_str[lifo.pop()+1:idx]
                self.query_tree.append((len(lifo), sub_str))
        return self.query_tree



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
