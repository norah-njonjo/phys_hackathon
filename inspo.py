import rebound
import pygame
import numpy as np

# ---------------------------
# Planet Classes
# ---------------------------
class Planet:
    def __init__(self, sim_particle, color=(0,0,255)):
        self.particle = sim_particle
        self.color = color
        self.radius = self.mass_to_radius()

    def mass_to_radius(self):
        return max(5, int(self.particle.m**(1/3)*1000))

    def update(self):
        self.radius = self.mass_to_radius()

    def draw(self, screen, scale=200, offset=(400,300)):
        x = int(self.particle.x * scale + offset[0])
        y = int(self.particle.y * scale + offset[1])
        pygame.draw.circle(screen, self.color, (x,y), self.radius)

class Player(Planet):
    def __init__(self, sim_particle, color=(0,255,0)):
        super().__init__(sim_particle, color)
        self.thrust = 0.001

    def apply_input(self, keys):
        if keys[pygame.K_UP]:
            self.particle.vy += self.thrust
        if keys[pygame.K_DOWN]:
            self.particle.vy -= self.thrust
        if keys[pygame.K_LEFT]:
            self.particle.vx -= self.thrust
        if keys[pygame.K_RIGHT]:
            self.particle.vx += self.thrust

# ---------------------------
# Game Manager
# ---------------------------
class Game:
    def __init__(self):
        # Initialize simulation
        self.sim = rebound.Simulation()
        self.sim.integrator = "ias15"
        self.sim.dt = 0.01

        # Add Sun (final boss)
        sun_particle = self.sim.add(m=1.0, x=0, y=0)
        self.sun = Planet(sun_particle, color=(255,255,0))

        # Add Player (Earth)
        player_particle = self.sim.add(m=3e-6, x=1.0, vy=1.0)
        self.player = Player(player_particle)

        # Add 9 other planets
        other_particles = [self.sim.add(m=1e-6*(i+1), x=1.5+i*0.3, vy=0.8) for i in range(9)]
        self.planets = [Planet(p) for p in other_particles]

        # Combine for drawing
        self.objects = [self.sun, self.player] + self.planets

    def update(self):
        self.sim.integrate(self.sim.t + self.sim.dt)
        for obj in self.objects:
            obj.update()
        self.check_collisions()

    def check_collisions(self):
        for planet in self.planets.copy():
            dx = planet.particle.x - self.player.particle.x
            dy = planet.particle.y - self.player.particle.y
            dist = np.sqrt(dx**2 + dy**2)
            if dist < (planet.radius + self.player.radius)/200:  # scale
                self.player.particle.m += planet.particle.m  # assimilate mass
                self.planets.remove(planet)
                self.objects.remove(planet)

        # Final boss collision
        dx = self.sun.particle.x - self.player.particle.x
        dy = self.sun.particle.y - self.player.particle.y
        dist = np.sqrt(dx**2 + dy**2)
        if dist < (self.sun.radius + self.player.radius)/200:
            if self.player.particle.m > self.sun.particle.m*0.1:
                print("You win! Earth has assimilated the Sun!")
            else:
                print("Too small! The Sun is too massive!")
            pygame.quit()
            exit()

# ---------------------------
# Initialize Pygame
# ---------------------------
pygame.init()
screen = pygame.display.set_mode((800,600))
pygame.display.set_caption("Gravitational Dating Game")
clock = pygame.time.Clock()

game = Game()

# ---------------------------
# Main Loop
# ---------------------------
running = True
while running:
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    game.player.apply_input(keys)
    game.update()

    # Draw
    screen.fill((0,0,0))
    for obj in game.objects:
        obj.draw(screen)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
