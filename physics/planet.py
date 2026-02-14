class Planet:
    def __init__(self, mass, radius, distToSun, name, rebound_particle=None):
        self.mass = mass
        self.radius = radius
        self.distToSun = distToSun
        self.name = name
        self.exists = True
        self.rebound_particle = rebound_particle # link to the particle in the simulation
    
