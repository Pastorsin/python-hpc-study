import itertools
import logging

import pandas as pd
from core import config, process

from benchmarker.summary import Summary
from benchmarker.plot import Plotter
from benchmarker.store import Benchmark, Store


class Benchmarker:
    def __init__(self):
        self.batches = config.get_batches_to_run()
        self.store = Store(self)
        self.current_batch_id = None

    def start(self):
        for batch_id in self.batches:
            self.current_batch_id = batch_id

            try:
                logging.info(f"Starting batch {batch_id}")
                self.start_batch(benchmarks=[])
            except Exception:
                logging.error(f"Batch {batch_id}", exc_info=True)
                continue

    def start_batch(self, benchmarks):
        logging.info("Running")

        for executor, duration, threads, size in self.get_batch_tasks():
            language = executor["name"]

            process_time = self.execute(executor, threads, size, duration)
            sequential_time = self.sequential_time(benchmarks, size, language)

            benchmark = Benchmark(
                threads=threads,
                size=size,
                iterations=duration,
                time=process_time,
                sequential_time=sequential_time,
                language=language,
                label=executor["label"],
            )

            benchmarks.append(benchmark)
            logging.info(benchmark)

        logging.info("Finish")
        self.finish_batch(benchmarks)

    def get_batch_tasks(self):
        batch = self.current_batch()

        return itertools.product(
            batch["executors"],
            batch["durations"],
            batch["threads"],
            batch["sizes"],
        )

    def current_batch(self):
        return self.batches[self.current_batch_id]

    def execute(self, executor, threads, size, duration):
        result = process.execute(
            executor, size=size, duration=duration, threads=threads
        )

        return result["time"]

    def sequential_time(self, benchmarks, size, language):
        find = list(
            filter(
                lambda b: b.size == size and b.language == language,
                self.sequential_benchmarks(benchmarks),
            )
        )

        return find[0].time if find else None

    def sequential_benchmarks(self, benchmarks):
        return [b for b in benchmarks if b.is_sequential()]

    def finish_batch(self, benchmarks):
        table = pd.DataFrame(benchmarks)
        logging.info(table)

        self.store.save(benchmarks)

    def build_plots(self, benchmarks):
        batch = self.current_batch()
        plotter = Plotter(batch["plot"], benchmarks)

        plots = (
            plotter.plot_times()
            + plotter.plot_gflops()
            + plotter.plot_metrics()
        )

        return plots

    def build_summaries(self, benchmarks):
        summaries = (
            Summary(benchmarks, metric="time").generate()
            + Summary(benchmarks, metric="gflops").generate()
        )

        return summaries
