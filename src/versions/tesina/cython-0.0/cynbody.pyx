import core.constants

GRAVITY = core.constants.GRAVITY
SOFT = core.constants.SOFT
DT = core.constants.DT


def nbody(
    N, D,
    positions_x, positions_y, positions_z,
    masses,
    velocities_x, velocities_y, velocities_z,
    dp_x, dp_y, dp_z,
):

    for _ in range(D):

        # For every body that experiences a force
        for i in range(N):
            # Initialize the force of the body i
            forces_x = 0.0
            forces_y = 0.0
            forces_z = 0.0

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
                dsquared = (dpos_x ** 2.0) + (dpos_y ** 2.0) + (dpos_z ** 2.0) + SOFT
                # Calculate the mass factor:
                # (G * mi * mj)
                gm = GRAVITY * masses[j] * masses[i]
                # Calculate the Fi denominator:
                # 1 / |qj - qi| ^ 3
                d32 = dsquared ** -1.5
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
            velocities_x[i] += aceleration_x * DT / 2.0
            velocities_y[i] += aceleration_y * DT / 2.0
            velocities_z[i] += aceleration_z * DT / 2.0
            # Save the differential position of body i
            dp_x[i] = velocities_x[i] * DT
            dp_y[i] = velocities_y[i] * DT
            dp_z[i] = velocities_z[i] * DT

        # Update positions of the bodies
        for i in range(N):
            positions_x[i] += dp_x[i]
            positions_y[i] += dp_y[i]
            positions_z[i] += dp_z[i]
