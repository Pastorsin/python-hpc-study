import json
from pathlib import Path
from string import Template

import toml

# Load config
ROOT = Path(__file__).parents[2]
CONFIG_FILE = ROOT / "config.toml"
config = toml.load(CONFIG_FILE)

# Config fields
PATHS = config["paths"]
BATCHES = config["batches"]
EXECUTION = config["execution"]
VENV = Template(PATHS["venv"])

# Project paths
SRC = ROOT / "src"
TESTS_DIR = SRC / "tests"
VERSIONS_DIR = SRC / PATHS["versions"] / PATHS["problem"]

# Utility functions
def binary_path(executor):
    return ROOT / VENV.substitute(**executor)


def script_path(executor):
    return VERSIONS_DIR / executor["name"] / PATHS["script"]


def get_batches_to_run():
    batches_to_run = EXECUTION["batches_to_run"]

    if batches_to_run == []:
        return {}

    if batches_to_run == "all":
        return BATCHES

    return {
        name: data
        for name, data in BATCHES.items()
        if any(name.startswith(b) for b in batches_to_run)
    }


def all_executors():
    executors = []

    for batch in get_batches_to_run().values():
        executors += batch["executors"]

    return executors


def executors_by_version():
    return {e["name"]: e for e in all_executors()}


def get_expected_positions():
    with open(TESTS_DIR / "expected.json") as expected:
        return json.load(expected)
