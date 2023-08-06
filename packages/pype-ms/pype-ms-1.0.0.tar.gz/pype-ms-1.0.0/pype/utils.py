import os
import logging

import __main__


GIT_CONTROL = os.system('git rev-parse') == 0

def save_git_sha(job_dir):
    cmd = f"echo $(git rev-parse --short HEAD) > {job_dir}/git_sha.txt"
    os.system(cmd)


def get_pipeline_dir():
    pipeline_dir = os.path.dirname(__main__.__file__)
    if not os.path.exists(pipeline_dir):
        os.makedirs(pipeline_dir, exist_ok=True)
        logging.info(f"Created pipeline directory {pipeline_dir}")

    return pipeline_dir
