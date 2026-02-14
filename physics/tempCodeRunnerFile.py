
def step(self, dt):
    self.sim.integrate(self.sim.t + dt)