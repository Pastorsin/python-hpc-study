from dataclasses import dataclass
from typing import List

import numpy as np

# Time differential of 1 second
DT = 1

# Universal gravitational constant
GRAVITY = 6.674e-11

# Softing squared to prevent numerical divergences when force goes to infinity
SOFT = 1e-20


@dataclass
class Body:
    position: np.ndarray
    mass: float
    velocity: np.ndarray
