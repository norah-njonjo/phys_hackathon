import random
from physics import planet
import numpy as np
import rebound

class SolarSystem:
    def __init__(self, simulation):
        self.sim = simulation
        self.planets = [] # list of planets in the simulation

    def add_planet(self, planet):
        theta = random.uniform(0, 2*np.pi)
        particle = self.sim.add(
            m=planet.mass,
            a=planet.distToSun,
            e=0,
            f=theta   # random true anomaly
        )

        planet.rebound_particle = particle
        self.planets.append(planet)



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
    
