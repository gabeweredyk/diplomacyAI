class Country(object):
    def __init__(self, n, a, f):
        self.name = n
        self.armies = a
        self.fleets = f

class Army(object):
    def __init__(self, loc):
        self.location = loc

class Fleet(object):
    def __init__(self, loc):
        self.location = loc
    
