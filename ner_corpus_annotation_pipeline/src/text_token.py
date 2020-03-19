class TextToken(object):
    """ A token of a section of the text """
    
    def __init__(self, text, start_index, end_index, tags_dict = None):

        if end_index < start_index or end_index > len(text) - 1 or start_index < 0:
            raise Exception("Invalid segment specification")

        self._section = text[start_index: end_index + 1]
        self._start_index = start_index
        self._end_index = end_index
        if tags_dict:
            tags_dict = tags_dict.copy()
        self._tags_dict = tags_dict

    @property
    def section(self):
        return self._section
    
    @property
    def start_index(self):
        return self._start_index
    
    @property
    def end_index(self):
        return self._end_index
    
    @property
    def tags_dictionary(self):
        return self._tags_dict

    def get_tag_value(self, key):
        if key in self._tags_dict:
            return self._tags_dict[key]
        return None

    def set_tag_value(self, key, value):
        self._tags_dict[key] = value
        
    def encloses(self, i):
        """
        Returns a bool indicating if 'i' is in the token boundaries
        
        Args:
            i (int): The value that will be searched inside the token boundaries
        
        Returns:
            bool: True if inside the token boundaries, false otherwise
        """
        if self._start_index <= i <= self._end_index:
            return True
        return False

def check_intersect(token1, token2):

    t1_start_in_t2 = _check_intersection_aux(token1.start_index, token2.start_index, token2.end_index)
    t1_end_in_t2 = _check_intersection_aux(token1.end_index, token2.start_index, token2.end_index)
    t2_start_in_t1 = _check_intersection_aux(token2.start_index, token1.start_index, token1.end_index)
    t2_end_in_t1 = _check_intersection_aux(token2.end_index, token1.start_index, token1.end_index)
    
    return t1_start_in_t2 or t1_end_in_t2 or t2_start_in_t1 or t2_end_in_t1

def _check_intersection_aux(point, start, end):
    return start <= point <= end