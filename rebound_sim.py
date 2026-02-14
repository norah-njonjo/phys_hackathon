import rebound
import numpy as np
import matplotlib.pyplot as plt

sim = rebound.Simulation()
sim.units = ['mearth', 'day', 'AU']


## print(sim.G)

sim.add(m=40000)
sim.add(m=.25, P=5, e=.04)
sim.add(m=1.6, P=11)
# sim.add(m=1.4, x pos, y pos, velocity)
# Easier to implement for forces !!

# Arrays for position
x_pos = np.empty((3,10))
y_pos = np.empty((3,10))

# Array for time
times = np.linspace(0,100,num=10)
for i,t in enumerate(times):
    sim.integrate(t)
    x_pos[0,i] = sim.particles[0].x
    y_pos[0,i] = sim.particles[0].y

    x_pos[1,i] = sim.particles[1].x
    y_pos[1,i] = sim.particles[1].y

    x_pos[2,i] = sim.particles[2].x
    y_pos[2,i] = sim.particles[2].y

plt.scatter(x_pos, y_pos)
plt.show()









## Status of particles

print("N =", sim.N)
print("G =", sim.G)
print("t =", sim.t)
i=0
for p in sim.particles:
    print("Particle " + str(i))
    i += 1
    print( p.x, p.y, p.vx, p.vy)