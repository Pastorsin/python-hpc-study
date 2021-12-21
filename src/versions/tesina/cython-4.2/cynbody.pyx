import core.constants
from cython import boundscheck, wraparound, nonecheck, cdivision
from cython.parallel import prange

cdef int BLOCKSIZE = 16
cdef double GRAVITY = core.constants.GRAVITY
cdef double SOFT = core.constants.SOFT
cdef double DT = core.constants.DT


@boundscheck(False)
@wraparound(False)
@nonecheck(False)
@cdivision(True)
cpdef void nbody(
    int N, int D, int T,
    double[::1] positions_x, double[::1] positions_y, double[::1] positions_z,
    double[::1] masses,
    double[::1] velocities_x, double[::1] velocities_y, double[::1] velocities_z,
    double[::1] dp_x, double[::1] dp_y, double[::1] dp_z,
    double[::1] forces_x, double[::1] forces_y, double[::1] forces_z,
):
    cdef double aceleration_x, aceleration_y, aceleration_z
    cdef double dpos_x, dpos_y, dpos_z
    cdef double dsquared, gm, d32

    cdef int i, j, b_i

    for _ in range(D):

        # For every body that experiences a force
        for b_i in prange(0, N, BLOCKSIZE, nogil=True, schedule="static", num_threads=T):
            # Initialize forces
            for i in range(b_i, b_i + BLOCKSIZE):
                forces_x[i] = 0.0
                forces_y[i] = 0.0
                forces_z[i] = 0.0

            # Calculate gravitational force to the rest of the bodies
            # Newton's Law of Universal Attraction:
            # Fi = (G * mi * mj * (qj - qi)) / (|qj - qi| ^ 3)
            for j in range(N):
                for i in range(b_i, b_i + BLOCKSIZE):
                    # Calculate the distance to the body i:
                    # (qj - qi)
                    dpos_x = positions_x[j] - positions_x[i]
                    dpos_y = positions_y[j] - positions_y[i]
                    dpos_z = positions_z[j] - positions_z[i]
                    # Calculate the distance magnitude:
                    # |qj - qi|
                    dsquared = (dpos_x ** 2.0) + (dpos_y ** 2.0) + (dpos_z ** 2.0) + SOFT
                    # Calculate the mass factor:
                    # (G * mi * mj)
                    gm = GRAVITY * masses[j] * masses[i]
                    # Calculate the Fi denominator:
                    # 1 / |qj - qi| ^ 3
                    d32 = dsquared ** -1.5
                    # Calculate the force:
                    # (G * mi * mj * (qj - qi)) / |qj - qi| ^ 3
                    forces_x[i] += gm * d32 * dpos_x
                    forces_y[i] += gm * d32 * dpos_y
                    forces_z[i] += gm * d32 * dpos_z
            
            for i in range(b_i, b_i + BLOCKSIZE):
                # Calculate the acceleration vector of body i:
                # |M = F * A|  |A = F / M|
                aceleration_x = forces_x[i] / masses[i]
                aceleration_y = forces_y[i] / masses[i]
                aceleration_z = forces_z[i] / masses[i]
                # Velocity Verlet integrator
                # V = V' + ((A * h) / 2) ; h = 1
                velocities_x[i] += aceleration_x * DT / 2.0
                velocities_y[i] += aceleration_y * DT / 2.0
                velocities_z[i] += aceleration_z * DT / 2.0
                # Save the differential position of body i
                dp_x[i] = velocities_x[i] * DT
                dp_y[i] = velocities_y[i] * DT
                dp_z[i] = velocities_z[i] * DT

        # Update positions of the bodies
        for i in prange(N, nogil=True, schedule="static", num_threads=T):
            positions_x[i] += dp_x[i]
            positions_y[i] += dp_y[i]
            positions_z[i] += dp_z[i]
