from threading import Barrier, Thread

import numpy as np
from core.builders import NumpyBuilder1D
from core.constants import DT, GRAVITY, SOFT
from core.runner import run
from numba import float32, int64, njit, void

DATATYPE = np.float32

_0 = DATATYPE(0.0)
_2 = DATATYPE(2.0)
_1_5 = DATATYPE(-1.5)

_DT = DATATYPE(DT)
_DT_2 = DATATYPE(_DT / 2.0)
_GRAVITY = DATATYPE(GRAVITY)
_SOFT = DATATYPE(SOFT)


@njit(
    void(
        int64, int64[::1],
        float32[::1], float32[::1], float32[::1],
        float32[::1],
        float32[::1], float32[::1], float32[::1],
        float32[::1], float32[::1], float32[::1],
    ),
    nogil=True,
    fastmath=True,
    error_model="numpy",
)
def calculate_positions(
    N, chunk,
    positions_x, positions_y, positions_z,
    masses,
    velocities_x, velocities_y, velocities_z,
    dp_x, dp_y, dp_z,
):
    # For every body that experiences a force
    for i in chunk:
        # Initialize the force of the body i
        forces_x = _0
        forces_y = _0
        forces_z = _0

        # Calculate gravitational force to the rest of the bodies
        # Newton's Law of Universal Attraction:
        # Fi = (G * mi * mj * (qj - qi)) / (|qj - qi| ^ 3)
        for j in range(N):
            # Calculate the distance to the body i:
            # (qj - qi)
            dpos_x = positions_x[j] - positions_x[i]
            dpos_y = positions_y[j] - positions_y[i]
            dpos_z = positions_z[j] - positions_z[i]
            # Calculate the distance magnitude:
            # |qj - qi|
            dsquared = (dpos_x ** _2) + (dpos_y ** _2) + (dpos_z ** _2) + _SOFT
            # Calculate the mass factor:
            # (G * mi * mj)
            gm = _GRAVITY * masses[j] * masses[i]
            # Calculate the Fi denominator:
            # 1 / |qj - qi| ^ 3
            d32 = dsquared ** _1_5
            # Calculate the force:
            # (G * mi * mj * (qj - qi)) / |qj - qi| ^ 3
            forces_x += gm * d32 * dpos_x
            forces_y += gm * d32 * dpos_y
            forces_z += gm * d32 * dpos_z

        # Calculate the acceleration vector of body i:
        # |M = F * A|  |A = F / M|
        aceleration_x = forces_x / masses[i]
        aceleration_y = forces_y / masses[i]
        aceleration_z = forces_z / masses[i]
        # Velocity Verlet integrator
        # V = V' + ((A * h) / 2) ; h = 1
        velocities_x[i] += aceleration_x * _DT_2
        velocities_y[i] += aceleration_y * _DT_2
        velocities_z[i] += aceleration_z * _DT_2
        # Save the differential position of body i
        dp_x[i] = velocities_x[i] * _DT
        dp_y[i] = velocities_y[i] * _DT
        dp_z[i] = velocities_z[i] * _DT


@njit(
    void(
        int64[::1],
        float32[::1], float32[::1], float32[::1],
        float32[::1], float32[::1], float32[::1],
    ),
    nogil=True,
    fastmath=True,
)
def update_positions(
    chunk,
    positions_x, positions_y, positions_z,
    dp_x, dp_y, dp_z,
):
    # Update positions of the bodies
    for i in chunk:
        positions_x[i] += dp_x[i]
        positions_y[i] += dp_y[i]
        positions_z[i] += dp_z[i]


def nbody(
    N, D, chunk,
    positions_x, positions_y, positions_z,
    masses,
    velocities_x, velocities_y, velocities_z,
    dp_x, dp_y, dp_z,
    barrier,
):
    # For each discrete instant of time
    for _ in range(D):
        calculate_positions(
            N, chunk,
            positions_x, positions_y, positions_z,
            masses,
            velocities_x, velocities_y, velocities_z,
            dp_x, dp_y, dp_z,
        )

        barrier.wait()

        update_positions(
            chunk, 
            positions_x, positions_y, positions_z, 
            dp_x, dp_y, dp_z,
        )

        barrier.wait()


def run_threads(threads):
    for t in threads:
        t.start()

    for t in threads:
        t.join()


@run(NumpyBuilder1D, DATATYPE)
def setup(stdin_args, arrays):
    N, T, D = stdin_args.N, stdin_args.T, stdin_args.D

    barrier = Barrier(T)
    chunks = np.array_split(np.arange(N), T)

    threads = [
        Thread(target=nbody, args=(N, D, chunk, *arrays, barrier))
        for chunk in chunks
    ]

    return run_threads, (threads,)