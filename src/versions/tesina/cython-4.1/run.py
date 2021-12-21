import numpy as np
from core.builders import CythonBlockBuilder
from core.runner import run
from cynbody import nbody

DATATYPE = np.float64


@run(CythonBlockBuilder, DATATYPE)
def setup(stdin_args, arrays):
    N, D, T = stdin_args.N, stdin_args.D, stdin_args.T

    return nbody, (N, D, T, *arrays)
