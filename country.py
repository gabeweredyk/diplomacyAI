class Army(object):
    def __init__(self, loc):
        self.location = loc

class Fleet(object):
    def __init__(self, loc):
        self.location = loc
    
class Country(object):
    def __init__(self, n, a, f, t):
        self.name = n
        self.armies = a
        self.fleets = f
        self.trust = t