import rebound
class SolarSystem:
    def __init__(self):
        self.sim = rebound.Simulation()
        
        self.sim.collision = None # we will handle collisions manually (in gamerules.py)
        self.sim.units = ('AU', 'yr', 'Msun')
        self.sim.integrator = "ias15"

        self.planets = [] # list of planets in the simulation

    def add_planet(self, planet, x=0, y=0, vx=0, vy=0):
        # adding planet to the simulation
        particle = self.sim.add(
            m=planet.mass,
            x=x, y=y,
            vx=vx, vy=vy,
            r=planet.radius
        )

        # linking planet to the particle in the simulation
        planet.rebound_particle = particle
        self.planets.append(planet)

    def step(self, dt):
        self.sim.integrate(self.sim.t + dt)

    def get_planet_positions(self):
        positions = {}
        for planet in self.planets:
            p = planet.rebound_particle
            positions[planet.name] = (p.x, p.y)
        return positions
    
    def get_planet_velocities(self):
        velocities = {}
        for planet in self.planets:
            p = planet.rebound_particle
            velocities[planet.name] = (p.vx, p.vy)
        return velocities
    
    def get_planet_masses(self):
        masses = {}
        for planet in self.planets:
            p = planet.rebound_particle
            masses[planet.name] = p.m
        return masses
    
    def remove_planet(self, planet):
        if (not planet.exists) : 
            # Removing planet from the simulation
            self.sim.remove(planet.rebound_particle)
            self.planets.remove(planet)

            # Marking planet as non-existent
            planet.exists = False

            # Unlinking the particle from the planet
            planet.rebound_particle = None

            print(f"{planet.name} has been removed from the simulation.")
    
