import numpy as np

def spawn_asteriods(sim, WIDTH, HEIGHT, SCALE,
                    ASTERIOD_COUNT=100,
                    AST_RADIUS_MIN=0.002,
                    AST_RADIUS_MAX=0.006,
                    SAFE_BUFFER_AU=0.05,
                    MASS_K=5e-19):
    # bounds in AU (spawn on-screen)
    X_MIN_AU = -(WIDTH / 2) / SCALE
    X_MAX_AU =  (WIDTH / 2) / SCALE
    Y_MIN_AU = -(HEIGHT / 2) / SCALE
    Y_MAX_AU =  (HEIGHT / 2) / SCALE

    bodies_to_avoid = sim.particles[:]  # sun + earth + planets already in sim

    asteriods = []

    for _ in range(ASTERIOD_COUNT):
        placed = False
        while not placed:
            r = float(np.random.uniform(AST_RADIUS_MIN, AST_RADIUS_MAX))
            x = float(np.random.uniform(X_MIN_AU, X_MAX_AU))
            y = float(np.random.uniform(Y_MIN_AU, Y_MAX_AU))

            ok = True
            for b in bodies_to_avoid:
                dx = x - b.x
                dy = y - b.y
                if dx*dx + dy*dy < (SAFE_BUFFER_AU + r) ** 2:
                    ok = False
                    break

            if ok:
                m = MASS_K * (r ** 3)
                p = sim.add(m=m, x=x, y=y, vx=0.0, vy=0.0)
                asteriods.append({"p": p, "r": r})
                placed = True

    return asteriods
