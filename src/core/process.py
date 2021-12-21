import shutil
import subprocess
from pathlib import Path

import jsons as serializer

from core import config

NUMBA_CONFIG_FILENAME = ".numba_config.yaml"

# TODO - Do it another way
# Numba needs the config file in the cwd
# and not allow parameterizing it
def load_envs(execute):
    def decorate(*args, **kwargs):
        script_path = config.script_path(*args)

        config_file = script_path.parent / NUMBA_CONFIG_FILENAME
        copy_file = Path.cwd() / NUMBA_CONFIG_FILENAME

        if config_file.exists():
            shutil.copy(config_file, copy_file)

        try:
            results = execute(*args, **kwargs)
        except Exception as e:
            raise e
        finally:
            copy_file.unlink(missing_ok=True)

        return results

    return decorate


@load_envs
def execute(executor, *, size, duration, threads):
    binary = config.binary_path(executor)
    script = config.script_path(executor)

    process = subprocess.run(
        [binary, script, f"{size}", f"{duration}", f"{threads}"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    print(process.stderr.decode())

    if results := process.stdout:
        return serializer.loads(results)
