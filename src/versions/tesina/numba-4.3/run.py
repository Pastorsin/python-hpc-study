import numba
import numpy as np
from core.builders import NumpyBuilder1D
from core.constants import DT, GRAVITY, SOFT
from core.runner import run
from numba import prange, njit, int64, float64, void


DATATYPE = np.float64

_2 = DATATYPE(2.0)
_1_5 = DATATYPE(-1.5)

_DT = DATATYPE(DT)
_DT_2 = DATATYPE(_DT / 2.0)
_GRAVITY = DATATYPE(GRAVITY)
_SOFT = DATATYPE(SOFT)

BLOCKSIZE = 32


@njit(
    void(
        int64,
        float64[::1], float64[::1], float64[::1],
        float64[::1],
        float64[::1], float64[::1], float64[::1],
        float64[::1], float64[::1], float64[::1],
    ),
    locals={
        "forces_x": float64[::1],
        "forces_y": float64[::1],
        "forces_z": float64[::1],
    },
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
    BLOCKS = N // BLOCKSIZE
    # Init the force
    forces_x = np.zeros(N, dtype=DATATYPE)
    forces_y = np.zeros(N, dtype=DATATYPE)
    forces_z = np.zeros(N, dtype=DATATYPE)

    for b in prange(BLOCKS):
        first = b * BLOCKSIZE
        last = first + BLOCKSIZE
        # Calculate gravitational force to the rest of the bodies
        # Newton's Law of Universal Attraction:
        # Fi = (G * mi * mj * (qj - qi)) / (|qj - qi| ^ 3)
        for j in range(N):
            for i in range(first, last):
                # Calculate the distance to the body i:
                # (qj - qi)
                dpos_x = positions_x[j] - positions_x[i]
                dpos_y = positions_y[j] - positions_y[i]
                dpos_z = positions_z[j] - positions_z[i]
                # Calculate the distance magnitude:
                # |qj - qi|
                dsquared = (
                    (dpos_x ** _2) + (dpos_y ** _2) + (dpos_z ** _2) + _SOFT
                )
                # Calculate the mass factor:
                # (G * mi * mj)
                gm = _GRAVITY * masses[j] * masses[i]
                # Calculate the Fi denominator:
                # 1 / |qj - qi| ^ 3
                d32 = dsquared ** _1_5
                # Calculate the force:
                # (G * mi * mj * (qj - qi)) / |qj - qi| ^ 3
                forces_x[i] += gm * dpos_x * d32
                forces_y[i] += gm * dpos_y * d32
                forces_z[i] += gm * dpos_z * d32

        for i in range(first, last):
            # Calculate the acceleration vector of body i:
            # |M = F * A|  |A = F / M|
            # f_i = i - first
            aceleration_x = forces_x[i] / masses[i]
            aceleration_y = forces_y[i] / masses[i]
            aceleration_z = forces_z[i] / masses[i]
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
        float64[::1], float64[::1], float64[::1],
        float64[::1], float64[::1], float64[::1],
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
        float64[::1], float64[::1], float64[::1],
        float64[::1],
        float64[::1], float64[::1], float64[::1],
        float64[::1], float64[::1], float64[::1],
    )
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
