from abc import ABC, abstractmethod

import numpy as np

from core.constants import Body


class ArrayBuilder(ABC):
    """The builders are mappers that map simulation data to data used by the visualization."""

    @abstractmethod
    def get_arrays(self):
        pass

    @abstractmethod
    def get_bodies(self):
        pass


class NumpyBuilder2D(ArrayBuilder):
    def __init__(self, bodies, datatype, order="C"):
        self.positions = np.array(
            [body.position for body in bodies], dtype=datatype, order=order
        )
        self.masses = np.array(
            [body.mass for body in bodies], dtype=datatype, order=order
        )
        self.velocities = np.array(
            [body.velocity for body in bodies], dtype=datatype, order=order
        )
        self.dp = np.empty(self.positions.shape, dtype=datatype, order=order)

    def get_bodies(self):
        body_fields = zip(self.positions, self.masses, self.velocities)
        return [Body(*fields) for fields in body_fields]

    def get_arrays(self):
        return (self.positions, self.masses, self.velocities, self.dp)


class NumpyBuilder1D(ArrayBuilder):
    def __init__(self, bodies, datatype, order="C"):
        self.N = len(bodies)

        self.positions_x = np.array(
            [body.position[0] for body in bodies], dtype=datatype, order=order
        )
        self.positions_y = np.array(
            [body.position[1] for body in bodies], dtype=datatype, order=order
        )
        self.positions_z = np.array(
            [body.position[2] for body in bodies], dtype=datatype, order=order
        )

        self.masses = np.array(
            [body.mass for body in bodies], dtype=datatype, order=order
        )

        self.velocities_x = np.array(
            [body.velocity[0] for body in bodies], dtype=datatype, order=order
        )
        self.velocities_y = np.array(
            [body.velocity[1] for body in bodies], dtype=datatype, order=order
        )
        self.velocities_z = np.array(
            [body.velocity[2] for body in bodies], dtype=datatype, order=order
        )

        self.dp_x = np.empty(self.N, dtype=datatype, order=order)
        self.dp_y = np.empty(self.N, dtype=datatype, order=order)
        self.dp_z = np.empty(self.N, dtype=datatype, order=order)

    def get_arrays(self):
        return (
            self.positions_x,
            self.positions_y,
            self.positions_z,
            self.masses,
            self.velocities_x,
            self.velocities_y,
            self.velocities_z,
            self.dp_x,
            self.dp_y,
            self.dp_z,
        )

    def get_bodies(self):
        bodies = []
        for i in range(self.N):
            bodies.append(
                Body(
                    position=np.array(
                        [
                            self.positions_x[i],
                            self.positions_y[i],
                            self.positions_z[i],
                        ],
                        dtype=np.float64,
                    ),
                    mass=np.array(
                        self.masses[i],
                        dtype=np.float64,
                    ),
                    velocity=np.array(
                        [
                            self.velocities_x[i],
                            self.velocities_y[i],
                            self.velocities_z[i],
                        ],
                        dtype=np.float64,
                    ),
                )
            )
        return bodies


class CythonBlockBuilder(NumpyBuilder1D):
    def __init__(self, bodies, datatype, order="C"):
        super().__init__(bodies, datatype, order=order)
        self.forces_x = np.zeros(self.N, dtype=datatype, order=order)
        self.forces_y = np.zeros(self.N, dtype=datatype, order=order)
        self.forces_z = np.zeros(self.N, dtype=datatype, order=order)

    def get_arrays(self):
        return (
            *super().get_arrays(),
            self.forces_x,
            self.forces_y,
            self.forces_z,
        )


class ListBuilder:
    def __init__(self, bodies, datatype):
        self.N = len(bodies)

        self.positions_x = [datatype(body.position[0]) for body in bodies]
        self.positions_y = [datatype(body.position[1]) for body in bodies]
        self.positions_z = [datatype(body.position[2]) for body in bodies]

        self.masses = [datatype(body.mass) for body in bodies]

        self.velocities_x = [datatype(body.velocity[0]) for body in bodies]
        self.velocities_y = [datatype(body.velocity[1]) for body in bodies]
        self.velocities_z = [datatype(body.velocity[2]) for body in bodies]

        self.dp_x = [datatype(0)] * self.N
        self.dp_y = [datatype(0)] * self.N
        self.dp_z = [datatype(0)] * self.N

    def get_arrays(self):
        return (
            self.positions_x,
            self.positions_y,
            self.positions_z,
            self.masses,
            self.velocities_x,
            self.velocities_y,
            self.velocities_z,
            self.dp_x,
            self.dp_y,
            self.dp_z,
        )

    def get_bodies(self):
        bodies = []
        for i in range(self.N):
            bodies.append(
                Body(
                    position=[
                        self.positions_x[i],
                        self.positions_y[i],
                        self.positions_z[i],
                    ],
                    mass=self.masses[i],
                    velocity=[
                        self.velocities_x[i],
                        self.velocities_y[i],
                        self.velocities_z[i],
                    ],
                )
            )
        return bodies
