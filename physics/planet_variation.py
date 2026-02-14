#This is to create a variety of planet objs w a variety of random sizes
from planet import Planet
import random


def mass_to_radius(mass):
    """
    changes the multiplier to fit the screen 
    """
    return max(5, int((mass ** (1/3)) * 20))

#spawn size in comparison to planets size 
def spawn_planet_rel(player_mass):
    """
    Creates a planet -- random mass and dist to Sun
    """
    p_small = 0.70
    smaller_min = 0.15
    smaller_max = 0.95
    bigger_min = 1.05
    bigger_max = 2.5

    #For inc the size of either body -- player or planet  
    if random.random() < p_small:
        mass = random.uniform(player_mass * smaller_min, player_mass * smaller_max)
    else:
        mass = random.uniform(player_mass * bigger_min, player_mass * bigger_max)

    radius = mass_to_radius(mass)

    #placeholder for distance to Sun
    distToSun = random.uniform(1.0, 10.0)

     name = f"planet_{index}"

    return Planet(mass, radius, distToSun, name)

def spawn_batch(player_mass, n=10):
    planets = []
    """
    Creates n planets
    """
    for i in range(n):
        planet = spawn_planet_rel(player_mass, i)
        planets.append(planet)

    return planets



