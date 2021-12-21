import logging
from .benchmarker import Benchmarker

if __name__ == "__main__":
    benchmarker = Benchmarker()

    log_filename = benchmarker.store.log_path()

    logging.basicConfig(
        format="%(asctime)s [%(levelname)s] \n%(message)s\n",
        level=logging.INFO,
        handlers=[logging.StreamHandler(), logging.FileHandler(log_filename)],
    )

    benchmarker.start()
