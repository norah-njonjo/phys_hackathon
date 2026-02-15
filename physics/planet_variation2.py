from physics.planet import Planet
import random

def mass_to_radius(mass):
    return max(5, int((mass ** (1/3)) * 20))

def spawn_batch(player_mass, sun_mass, n=10):

    planets = []

    for i in range(n):

        mass = random.uniform(player_mass * 0.2, player_mass * 2.0)

        # Cap mass below Sun
        mass = min(mass, sun_mass * 0.5)

        radius = mass_to_radius(mass)

        # Spread orbits near Earth
        dist = random.uniform(0.8, 1.5)

        planet = Planet(
            mass=mass,
            radius=radius,
            distToSun=dist,
            name=f"Planet_{i}"
        )

        planets.append(planet)

    return planets
