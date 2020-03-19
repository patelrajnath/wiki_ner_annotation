class Entity():
    def __init__(self, names, tag):
        self._names = names
        self._tag = tag
    
    @property
    def names(self):
        return self._names

    @property
    def tag(self):
        return self._tag