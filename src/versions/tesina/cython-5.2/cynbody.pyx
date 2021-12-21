import core.constants
from cython import boundscheck, wraparound, nonecheck, cdivision
from cython.parallel import prange

cdef float GRAVITY = core.constants.GRAVITY
cdef float SOFT = core.constants.SOFT
cdef float DT = core.constants.DT

cdef extern from "constant.h":
    cdef const float _1_5
    cdef const float _0
    cdef const float _2


@boundscheck(False)
@wraparound(False)
@nonecheck(False)
@cdivision(True)
cpdef void nbody(
    int N, int D, int T,
    float[::1] positions_x, float[::1] positions_y, float[::1] positions_z,
    float[::1] masses,
    float[::1] velocities_x, float[::1] velocities_y, float[::1] velocities_z,
    float[::1] dp_x, float[::1] dp_y, float[::1] dp_z,
):
    cdef float forces_x, forces_y, forces_z
    cdef float aceleration_x, aceleration_y, aceleration_z
    cdef float dpos_x, dpos_y, dpos_z
    cdef float dsquared, gm, d32

    cdef int i, j

    for _ in range(D):

        # For every body that experiences a force
        for i in prange(N, nogil=True, schedule="static", num_threads=T):
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
                dsquared = (dpos_x ** _2) + (dpos_y ** _2) + (dpos_z ** _2) + SOFT
                # Calculate the mass factor:
                # (G * mi * mj)
                gm = GRAVITY * masses[j] * masses[i]
                # Calculate the Fi denominator:
                # 1 / |qj - qi| ^ 3
                d32 = dsquared ** _1_5
                # Calculate the force:
                # (G * mi * mj * (qj - qi)) / |qj - qi| ^ 3
                forces_x = forces_x + gm * d32 * dpos_x
                forces_y = forces_y + gm * d32 * dpos_y
                forces_z = forces_z + gm * d32 * dpos_z

            # Calculate the acceleration vector of body i:
            # |M = F * A|  |A = F / M|
            aceleration_x = forces_x / masses[i]
            aceleration_y = forces_y / masses[i]
            aceleration_z = forces_z / masses[i]
            # Velocity Verlet integrator
            # V = V' + ((A * h) / 2) ; h = 1
            velocities_x[i] += aceleration_x * DT / _2
            velocities_y[i] += aceleration_y * DT / _2
            velocities_z[i] += aceleration_z * DT / _2
            # Save the differential position of body i
            dp_x[i] = velocities_x[i] * DT
            dp_y[i] = velocities_y[i] * DT
            dp_z[i] = velocities_z[i] * DT

        # Update positions of the bodies
        for i in prange(N, nogil=True, schedule="static", num_threads=T):
            positions_x[i] += dp_x[i]
            positions_y[i] += dp_y[i]
            positions_z[i] += dp_z[i]
