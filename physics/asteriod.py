class Asteriod:
    def __init__(self, mass, radius, x, y, vx = 0.0, vy = 0.0, name: str = "Asteroid"):
        self.mass = mass
        self.radius = radius
        self.x = x
        self.y = y
        self.vx = vx 
        self.vy = vy
        self.name = name

        self.exists = True
        self.rebound_particle = None 