import argparse
import json
import math
import timeit

import jsons as serializer

from core.constants import Body


def run(ArrayBuilder, datatype):
    def decorate(setup):
        stdin_args = parse_args()
        bodies = init_bodies(stdin_args.N)

        builder = ArrayBuilder(bodies, datatype)
        arrays = builder.get_arrays()

        fn, args = setup(stdin_args, arrays)
        time = take_time(fn, args)

        bodies = builder.get_bodies()
        display(bodies, time, verbose=stdin_args.verbose)

    return decorate


def take_time(fn, args, repeats=1):
    times = timeit.repeat(lambda: fn(*args), number=1, repeat=repeats)
    return min(times)


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("N", type=int, help="set number of bodies")
    parser.add_argument(
        "D", type=int, help="set number of iterations (duration)"
    )
    parser.add_argument("T", type=int, help="set number of threads")
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="display positions of the bodies",
    )

    args = parser.parse_args()

    N, T, D = args.N, args.T, args.D

    if not (N > 0 and D > 0 and T > 0):
        parser.error("N, D and T must be positive")

    return args


def init_bodies(N):
    DISTANCE = 100_000
    MASS = 5.97e20

    bodies = []

    int_sqrt_n = math.ceil(math.sqrt(N))

    for i in range(N):
        x_pos = (i % int_sqrt_n) * DISTANCE
        y_pos = DISTANCE * i
        z_pos = 5_000

        body = Body(
            position=[x_pos, y_pos, z_pos],
            mass=MASS,
            velocity=([0.0, 0.0, 0.0]),
        )

        bodies.append(body)

    return bodies


def display(bodies, time, verbose=True):
    results = {"bodies": [], "time": time}

    content = bodies if verbose else get_positions(bodies)
    results["bodies"].extend(content)

    serialized_results = serializer.dump(results)
    pretty_results = json.dumps(serialized_results, indent=4)

    print(pretty_results)


def get_positions(bodies):
    return [body.position for body in bodies]
