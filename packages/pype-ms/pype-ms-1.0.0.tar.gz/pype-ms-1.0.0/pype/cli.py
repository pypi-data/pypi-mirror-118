import datetime
import importlib
import logging
import os
import shutil
import socket
import sys
import traceback

import click
import yaml

from pype import utils


logging.basicConfig(level=logging.INFO)


class Status:
    def __init__(self, dir_):
        self.dir = dir_
        self.status = "status"
        for status in ["Done", "Failed", "Running"]:
            if os.path.exists(os.path.join(dir_, status)):
                self.status = status

        self.status_path = os.path.join(dir_, self.status)

        with open(self.status_path, "w") as f:
            f.write("Host: " + socket.gethostname() + "\n")

    def done(self):
        self._set_status("Done")

    def running(self):
        self._set_status("Running")

    def failed(self):
        self._set_status("Failed")

    def _set_status(self, status):
        timestamp = datetime.datetime.now().strftime("%y/%m/%d-%H:%M:%S")

        with open(self.status_path, "a") as status_file:
            status_file.write(status + ": " + timestamp + "\n")

        status_path = os.path.join(self.dir, status)
        os.rename(self.status_path, status_path)

        self.status = status
        self.status_path = status_path


@click.group()
def cli():
    pass


@cli.command()
@click.option(
    "--rerun",
    default=False,
    is_flag=True,
    help="Delete everything in the output dir of the job and rerun the job with the specified "
    "config.yaml",
)
@click.option(
    "--allow-uncommitted",
    "-au",
    default=False,
    is_flag=True,
    help="Allow to run job even if there are uncommitted changes in the directory",
)
@click.option(
    "--log",
    "-l",
    default=False,
    is_flag=True,
    help="will log stdout and stderr to a file log.txt instead of stdout, useful when using "
    "screen for example",
)
@click.argument("config_file")
def run(config_file, rerun, allow_uncommitted, log):
    config = yaml.load(open(config_file, "r"), Loader=yaml.FullLoader)
    job_dir = config["job_dir"]

    if rerun:
        _remove_all_but_config(job_dir)

    status = Status(job_dir)

    if status.status == "Running" or status.status == "Done":
        if permission_to_continue(f"Job is {status.status}."):
            print("job aborted")
            sys.exit()

    if utils.GIT_CONTROL:
        if not allow_uncommitted >= _uncomitted():
            if permission_to_continue("You have uncomitted changes."):
                status.failed()
                logging.info("Job aborted.")
                sys.exit()

        utils.save_git_sha(job_dir)

    status.running()

    if log:
        sys.stdout = open(os.path.join(job_dir, "logs.txt"), "w")

    try:
        module = _import_module(config["script_path"])
        if not hasattr(module, "main"):
            raise RuntimeError(f"{config['script_path']} has no main function.")

        module.main(config)
        status.done()

    except Exception:  # pylint: disable=broad-except
        status.failed()
        print(traceback.format_exc())


def permission_to_continue(msg):
    return input(msg + "Type 'y' or 'yes' to continue anyways\n").lower() not in [
        "y",
        "yes",
    ]


def _remove_all_but_config(job_dir):
    for f in os.listdir(job_dir):
        if f == "config.yaml":
            continue

        full_path = os.path.join(job_dir, f)

        if os.path.isdir(full_path):
            shutil.rmtree(full_path)
        else:
            os.remove(full_path)


def _import_module(path):
    spec = importlib.util.spec_from_file_location("module.name", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    return module


def _uncomitted():
    cmd = r"git status | grep -q '\smodified:\s'"
    code = os.system(cmd)
    return code == 0
