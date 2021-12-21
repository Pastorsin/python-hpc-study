import math

import numba
import numpy as np
from core.builders import NumpyBuilder1D
from core.constants import DT, GRAVITY, SOFT
from core.runner import run
from numba import double, int64, njit, prange, void

DATATYPE = np.float64
POW = math.pow

_0 = DATATYPE(0.0)
_2 = DATATYPE(2.0)
_1_5 = DATATYPE(-1.5)

_DT = DATATYPE(DT)
_DT_2 = DATATYPE(_DT / 2.0)
_GRAVITY = DATATYPE(GRAVITY)
_SOFT = DATATYPE(SOFT)


@njit(
    void(
        int64,
        double[::1], double[::1], double[::1],
        double[::1],
        double[::1], double[::1], double[::1],
        double[::1], double[::1], double[::1],
    ),
    fastmath=True,
    parallel=True,
    error_model="numpy",
)
def calculate_positions(
    N,
    positions_x, positions_y, positions_z,
    masses,
    velocities_x, velocities_y, velocities_z,
    dp_x, dp_y, dp_z,
):
    # For every body that experiences a force
    for i in prange(N):
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
            dsquared = (
                POW(dpos_x, _2) + POW(dpos_y, _2) + POW(dpos_z, _2) + _SOFT
            )
            # Calculate the mass factor:
            # (G * mi * mj)
            gm = _GRAVITY * masses[j] * masses[i]
            # Calculate the Fi denominator:
            # 1 / |qj - qi| ^ 3
            d32 = POW(dsquared, _1_5)
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
        int64,
        double[::1], double[::1], double[::1],
        double[::1], double[::1], double[::1],
    ),
    fastmath=True,
    parallel=True,
    error_model="numpy",
)
def update_positions(
    N,
    positions_x, positions_y, positions_z,
    dp_x, dp_y, dp_z,
):
    # Update positions of the bodies
    for i in prange(N):
        positions_x[i] += dp_x[i]
        positions_y[i] += dp_y[i]
        positions_z[i] += dp_z[i]


@njit(
    void(
        int64, int64,
        double[::1], double[::1], double[::1],
        double[::1],
        double[::1], double[::1], double[::1],
        double[::1], double[::1], double[::1],
    ),
    fastmath=True,
    error_model="numpy",
)
def nbody(
    N, D,
    positions_x, positions_y, positions_z,
    masses,
    velocities_x, velocities_y, velocities_z,
    dp_x, dp_y, dp_z,
):
    # For each discrete instant of time
    for _ in range(D):
        calculate_positions(
            N,
            positions_x, positions_y, positions_z,
            masses,
            velocities_x, velocities_y, velocities_z,
            dp_x, dp_y, dp_z,
        )

        update_positions(
            N, 
            positions_x, positions_y, positions_z, 
            dp_x, dp_y, dp_z,
        )


@run(NumpyBuilder1D, DATATYPE)
def setup(stdin_args, arrays):
    N, D, T = stdin_args.N, stdin_args.D, stdin_args.T

    numba.set_num_threads(T)

    return nbody, (N, D, *arrays)
