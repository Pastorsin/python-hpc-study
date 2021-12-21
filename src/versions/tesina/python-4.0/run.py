import numpy as np
from core.builders import NumpyBuilder2D
from core.constants import DT, GRAVITY, SOFT
from core.runner import run
from threading import Barrier, Thread

DATATYPE = np.float64

_2 = DATATYPE(2.0)
_1_5 = DATATYPE(-1.5)

_DT = DATATYPE(DT)
_DT_2 = DATATYPE(_DT / 2.0)
_GRAVITY = DATATYPE(GRAVITY)
_SOFT = DATATYPE(SOFT)


def nbody(N, D, positions, masses, velocities, dp, chunk, barrier):
    # For each discrete instant of time
    for _ in range(D):
        # For every body that experiences a force
        for i in chunk:
            # Newton's Law of Universal Attraction:
            # Fi = (G * mi * mj * (qj - qi)) / (|qj - qi| ^ 3)
            # Calculate the distances to the body i:
            # (qj - qi)
            dpos = np.subtract(positions, positions[i], order="F")
            # Calculate the distance magnitudes:
            # |qj - qi|
            dsquared = (dpos ** _2).sum(axis=1) + _SOFT
            # Calculate the mass factors:
            # (G * mi * mj)
            gm = masses * (masses[i] * _GRAVITY)
            # Calculate the Fi denominator:
            # 1 / |qj - qi| ^ 3
            d32 = dsquared ** _1_5
            # (G * mi * mj) / |qj - qi| ^ 3
            gm_d32 = (gm * d32).reshape(N, 1, order="F")
            # Calculate the forces:
            # (G * mi * mj * (qj - qi)) / |qj - qi| ^ 3
            forces = np.multiply(gm_d32, dpos, order="F").sum(axis=0)

            # Calculate the acceleration vector of body i:
            # |M = F * A|  |A = F / M|
            acceleration = forces / masses[i]
            # Velocity Verlet integrator
            # V = V' + ((A * h) / 2) ; h = 1
            velocities[i] += acceleration * _DT_2
            # Save the differential position of body i
            dp[i] = velocities[i] * _DT

        barrier.wait()

        # Update positions of the bodies
        for i in chunk:
            positions[i] += dp[i]

        barrier.wait()


def run_threads(threads):
    for t in threads:
        t.start()

    for t in threads:
        t.join()


@run(NumpyBuilder2D, DATATYPE)
def setup(stdin_args, arrays):
    N, T, D = stdin_args.N, stdin_args.T, stdin_args.D

    barrier = Barrier(T)
    chunks = np.array_split(np.arange(N), T)

    threads = [
        Thread(target=nbody, args=(N, D, *arrays, chunk, barrier))
        for chunk in chunks
    ]

    return run_threads, (threads,)
