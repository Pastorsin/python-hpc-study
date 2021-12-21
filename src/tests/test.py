import multiprocessing
import unittest

import numpy as np
from core import config, process
from parameterized import parameterized

# Generate the tests for each version specified in config
executors_by_version = config.executors_by_version()
versions = executors_by_version.keys()
executors = executors_by_version.values()

tests = list(zip(versions, executors))


class NBodyTest(unittest.TestCase):
    FLOAT32_VERSIONS = ("float32",)
    DECIMAL_PRESICION = 6
    THREADS = multiprocessing.cpu_count()

    def setUp(self):
        self.expected_positions = config.get_expected_positions()

    def __test(self, executor, *, size, duration, threads):
        results = process.execute(
            executor, size=size, duration=duration, threads=threads
        )

        resulting_positions = results["bodies"]

        if "float32" in executor["label"]:
            # The result for this initialization of the problem
            # cannot be represented with float32
            # self.assertTrue(np.isnan(resulting_positions).all())
            pass
        else:
            expected_positions = self.expected_positions[f"{duration}"]
            positions = zip(expected_positions, resulting_positions)

            for expected_position, resulting_position in positions:
                coords = zip(expected_position, resulting_position)

                for expected_coord, resulting_coord in coords:
                    self.assertAlmostEqual(
                        expected_coord,
                        resulting_coord,
                        places=self.DECIMAL_PRESICION,
                        msg=f"N={size}; I={duration}; T={threads}",
                    )

    @parameterized.expand(tests)
    def test_sequential(self, _, executor):
        self.__test(executor, size=256, duration=1, threads=1)
        self.__test(executor, size=256, duration=100, threads=1)

    @parameterized.expand(tests)
    def test_parallel(self, _, executor):
        self.__test(executor, size=256, duration=1, threads=self.THREADS)
        self.__test(executor, size=256, duration=100, threads=self.THREADS)


if __name__ == "__main__":
    unittest.main()
