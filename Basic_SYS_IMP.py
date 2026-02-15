from physics.solarsystem import SolarSystem
from physics.planet_variation2 import spawn_batch

import rebound
import pygame
import numpy as np
import sys


# ==============================
# 1. DEFINE COLLISION FUNCTION
# ==============================

def custom_merge(sim, collision):

    p1 = sim.particles[collision.p1]
    p2 = sim.particles[collision.p2]

    # If Earth involved
    if p1.hash == "earth" or p2.hash == "earth":

        earth = p1 if p1.hash == "earth" else p2
        other = p2 if earth == p1 else p1

        # Earth absorbs smaller
        if earth.m >= other.m:
            earth.m += other.m * 5
            sim.remove(other.index)
            print("♡")

        # Earth destroyed
        else:
            print("💔")
            sim.remove(earth.index)

    else:
        # Normal merge for others
        sim.merge(collision)


# ==============================
# 2. CREATE SIMULATION
# ==============================

sim = rebound.Simulation()
sim.units = ('AU', 'yr', 'Msun')
sim.integrator = "ias15"

sim.collision = "direct"
sim.collision_resolve = custom_merge


# ==============================
# 3. ADD SUN AND EARTH
# ==============================

SUN_MASS = 1.0
EARTH_MASS = 3e-6

def density(m):
    return m**(1/3)

# Sun
sim.add(m=SUN_MASS)

# Earth
sim.add(m=EARTH_MASS, a=1.0, r=density(EARTH_MASS), hash="earth")

sim.move_to_com()


# ==============================
# 4. ADD RANDOM PLANETS
# ==============================

solsys = SolarSystem(sim)

random_planets = spawn_batch(
    player_mass=EARTH_MASS,
    sun_mass=SUN_MASS,
    n=10
)

for p in random_planets:
    solsys.add_planet(p)

sim.move_to_com()


# ==============================
# 5. PYGAME SETUP
# ==============================

pygame.init()
WIDTH, HEIGHT = 1000, 1000
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

SCALE = 300
CENTER = np.array([WIDTH//2, HEIGHT//2])


# ==============================
# 6. GAME LOOP
# ==============================

dt = 0.002
thrust_accel = 15.0
running = True

while running:

    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    keys = pygame.key.get_pressed()

    # Check if Earth still exists
    if "earth" not in sim.particles:
        print("Game Over")
        running = False
        continue

    earth = sim.particles["earth"]

    # -------- THRUST --------
    thrust = np.array([0.0, 0.0])

    if keys[pygame.K_UP]:
        thrust[1] += 1
    if keys[pygame.K_DOWN]:
        thrust[1] -= 1
    if keys[pygame.K_LEFT]:
        thrust[0] -= 1
    if keys[pygame.K_RIGHT]:
        thrust[0] += 1

    if np.linalg.norm(thrust) > 0:
        thrust = thrust / np.linalg.norm(thrust)
        accel = thrust * thrust_accel * 5.0
        earth.vx += accel[0] * dt
        earth.vy += accel[1] * dt

    # -------- PHYSICS STEP --------
    sim.integrate(sim.t + dt)

    # -------- RENDER --------
    screen.fill((0, 0, 0))

    # Sun
    sun = sim.particles[0]
    sun_pos = CENTER + np.array([sun.x, -sun.y]) * SCALE
    pygame.draw.circle(screen, (255, 255, 0), sun_pos.astype(int), 10)

    # Earth
    earth_pos = CENTER + np.array([earth.x, -earth.y]) * SCALE
    pygame.draw.circle(screen, (100, 150, 255), earth_pos.astype(int), 6)

    # Other planets
    for planet in solsys.planets:
        if planet.rebound_particle:
            p = planet.rebound_particle
            pos = CENTER + np.array([p.x, -p.y]) * SCALE
            pygame.draw.circle(screen, (200, 200, 200), pos.astype(int), 4)

    pygame.display.flip()

pygame.quit()
sys.exit()
