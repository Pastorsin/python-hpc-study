import numpy as np
from core.builders import NumpyBuilder1D
from core.runner import run
from cynbody import nbody

DATATYPE = np.float64


@run(NumpyBuilder1D, DATATYPE)
def setup(stdin_args, arrays):
    N, D = stdin_args.N, stdin_args.D

    return nbody, (N, D, *arrays)
