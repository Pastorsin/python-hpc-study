import logging
from datetime import datetime
from pathlib import Path

import cpuinfo
from core.config import ROOT

from benchmarker.models import Benchmark


class Store:
    DATE_FORMAT = "%d-%m-%Y-%H:%M:%S"
    BENCHMARK_FILENAME = "benchmark.json"
    PLOT_DIR_NAME = "plots"
    SUMMARY_DIR_NAME = "summaries"

    def __init__(self, benchmarker):
        self.BENCHMARKS_ROOT = ROOT / "benchmarks"
        self.CPU = cpuinfo.get_cpu_info()["brand_raw"].lower()

        self.benchmarker = benchmarker
        self.batches_path = self._create_batches_dir()

    def _create_batches_dir(self):
        created_at = datetime.now()
        path = self.cpu_path() / created_at.strftime(self.DATE_FORMAT)

        path.mkdir(parents=True, exist_ok=True)

        return path

    def cpu_path(self):
        return self.BENCHMARKS_ROOT / self.CPU

    def save(self, benchmarks):
        self.version_path().mkdir()

        self.save_benchmarks(benchmarks)
        self.save_plots(benchmarks)
        self.save_summaries(benchmarks)

    def save_benchmarks(self, benchmarks):
        filename = self.benchmark_path()

        with open(filename, "w") as benchmark_file:
            data = Benchmark.schema().dumps(benchmarks, many=True)
            benchmark_file.write(data)

        logging.info(f"Data saved in {filename}")

    def benchmark_path(self):
        return self.version_path() / self.BENCHMARK_FILENAME

    def version_path(self):
        return self.batches_path / self.benchmarker.current_batch_id

    def save_summaries(self, benchmarks):
        summaries = self.benchmarker.build_summaries(benchmarks)

        path = self.summaries_path()
        path.mkdir()

        for summary in summaries:
            df = summary["df"]

            save_path = path / self.summaries_filename(summary)
            df.to_csv(save_path)

            logging.info(f"Summary saved in {save_path}")

    def summaries_path(self):
        return self.version_path() / self.SUMMARY_DIR_NAME

    def summaries_filename(self, summary):
        metric, language = summary["metric"], summary["language"]

        return f"{metric}-{language}.csv"

    def save_plots(self, benchmarks):
        plots = self.benchmarker.build_plots(benchmarks)

        root = self.plots_path()
        root.mkdir()

        for plot in plots:
            save_path = root / self.plot_filename(plot)

            plot.get("figure").savefig(save_path)

        logging.info(f"Plots saved in {root}")

    def plots_path(self):
        return self.version_path() / self.PLOT_DIR_NAME

    def plot_filename(self, plot):
        metric, size = plot["metric"], plot["size"]

        return f"{metric}-{size}.jpg"

    def log_path(self, filename="benchmarker.log"):
        return self.batches_path / filename
