import numpy as np
from core.builders import NumpyBuilder2D
from core.constants import DT, GRAVITY, SOFT
from core.runner import run


DATATYPE = np.float64

_2 = DATATYPE(2.0)
_1_5 = DATATYPE(-1.5)

_DT = DATATYPE(DT)
_DT_2 = DATATYPE(_DT / 2.0)
_GRAVITY = DATATYPE(GRAVITY)
_SOFT = DATATYPE(SOFT)


def nbody(N, D, positions, masses, velocities, dp):
    BLOCKSIZE = 16

    # For each discrete instant of time
    for _ in range(D):
        for first in range(0, N, BLOCKSIZE):
            last = first + BLOCKSIZE

            # Init the force
            forces = np.zeros((BLOCKSIZE, 3), dtype=DATATYPE)

            # Calculate gravitational force to the rest of the bodies
            # Newton's Law of Universal Attraction:
            # Fi = (G * mi * mj * (qj - qi)) / (|qj - qi| ^ 3)
            for j in range(N):
                # Newton's Law of Universal Attraction:
                # Fi = (G * mi * mj * (qj - qi)) / (|qj - qi| ^ 3)
                # Calculate the distances to the body i:
                # (qj - qi)
                dpos = np.subtract(
                    positions[j], positions[first:last], order="F"
                )
                # Calculate the distance magnitudes:
                # |qj - qi|
                dsquared = (dpos ** _2).sum(axis=1) + _SOFT
                # Calculate the mass factors:
                # (G * mi * mj)
                gm = masses[first:last] * (masses[j] * _GRAVITY)
                # Calculate the Fi denominator:
                # 1 / |qj - qi| ^ 3
                d32 = dsquared ** _1_5
                # (G * mi * mj) / |qj - qi| ^ 3
                gm_d32 = (gm * d32).reshape(BLOCKSIZE, 1, order="F")
                # Calculate the forces:
                # (G * mi * mj * (qj - qi)) / |qj - qi| ^ 3
                forces += np.multiply(gm_d32, dpos, order="F")

            # Calculate the acceleration vector of body i:
            # |M = F * A|  |A = F / M|
            # f_i = i - first
            aceleration = forces / masses[first:last].reshape(BLOCKSIZE, 1)
            # Velocity Verlet integrator
            # V = V' + ((A * h) / 2) ; h = 1
            velocities[first:last] += aceleration * _DT_2
            dp[first:last] = velocities[first:last] * _DT

        # Update positions of the bodies
        for first in range(0, N, BLOCKSIZE):
            last = first + BLOCKSIZE
            positions[first:last] += dp[first:last]


@run(NumpyBuilder2D, DATATYPE)
def setup(stdin_args, arrays):
    N, D = stdin_args.N, stdin_args.D

    return nbody, (N, D, *arrays)
