from dataclasses import dataclass, field

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class Benchmark:
    language: str
    label: str
    threads: int
    size: int
    time: float
    iterations: int
    sequential_time: float
    speedup: float = field(init=False)
    efficiency: float = field(init=False)
    gflops: float = field(init=False)

    def __post_init__(self):
        self.speedup = self._speedup()
        self.efficiency = self._efficiency()
        self.gflops = self._gflops()

    def _speedup(self):
        if self.sequential_time is None:
            return None

        return self.sequential_time / self.time

    def _efficiency(self):
        if self.sequential_time is None:
            return None

        return self._speedup() / self.threads

    def _gflops(self):
        FLOPS = 20
        GIGA = 10 ** 9

        total_flops = FLOPS * (self.size ** 2) * self.iterations
        gigaseconds = self.time * GIGA

        return total_flops / gigaseconds

    def is_sequential(self):
        return self.threads == 1
