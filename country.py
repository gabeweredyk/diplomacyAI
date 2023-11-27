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
    
    def armyInProvince(self, p):
        for army in self.armies:
            if army.location == p:
                return True
        return False
    
    def fleetInProvince(self, p):
        for fleet in self.fleets:
            if fleet.location == p:
                return True
        return False