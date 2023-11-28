class Army(object):
    def __init__(self, loc, own):
        self.loc = loc
        self.owner = own
        self.type = "a"
    
    def inSupportingLoc(self,p,paths,territories):
        if self.loc in paths[p] and territories[p]["type"] != "Sea":
            return True
        return False

class Fleet(object):
    def __init__(self, loc, own):
        self.loc = loc
        self.owner = own
        self.type = "f"
    
    def inSupportingLoc(self,p,paths,territories):
        if self.loc in paths[p] and territories[p]["type"] != "Land":
            return True
        return False
    
class Country(object):
    def __init__(self, n, a, f, t):
        self.name = n
        self.armies = a
        self.fleets = f
        self.trust = t
    
    def armyInProvince(self, p):
        for army in self.armies:
            if army.loc == p:
                return True
        return False
    
    def fleetInProvince(self, p):
        for fleet in self.fleets:
            if fleet.loc == p:
                return True
        return False
    
    def unitAtLocation(self, p):
        for army in self.armies:
            if army.loc == p:
                return army
        for fleet in self.fleets:
            if fleet.loc == p:
                return fleet
        return None