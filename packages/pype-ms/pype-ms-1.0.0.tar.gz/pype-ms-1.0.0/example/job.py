from pype.baseconfig import BaseConfig


class ExampleJobConfig(BaseConfig):
    script_path = "example/job.py"

def main(config):
    _ = config
