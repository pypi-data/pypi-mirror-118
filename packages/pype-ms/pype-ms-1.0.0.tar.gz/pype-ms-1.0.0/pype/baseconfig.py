import os
import logging
import pprint
from uuid import uuid4
import yaml
from pype import utils

class BaseConfig:
    _expected_attributes = {
        "inputs",
        "optional_inputs",
        "params",
        "optional_params",
        "script_path",
        "outputs",
    }

    def __init__(
        self,
        pipeline_dir=None,
        job_id=None,
        inputs=None,
        params=None,
    ):
        """
        Inherit from this config class to create configs for jobs.

        class ExampleConfig(BaseConfig):
            script_path = 'path/to/script/that/configured/by/this/config'
            inputs = {'input_key'}
            params = {'param_key'}
            outputs = {'output_1': 'path/to/where_output_is_saved'}
            optional_params = {'optional_param'}
            optional_inputs = {'optional_input'}

        script pth has to be set so that the config knows where to find the

        To set an optional parameter/input use the default value None.
            outputs has to be a dictionary as it is name of what to save and where to save it
            inputs and params are sets as the user has to specify themselves what there values re
            inputs are always paths to data or outputs from other jobs
            params are the parameters needed to run a job and does not necessarily come from
            outside

        To set an optional parameter/input use the default value None.
        """

        # Verify construcion of child
        assert hasattr(
            self, "script_path"
        ), f"Configuration class for f{type(self)} must include script_path"

        for attr_name in self._expected_attributes:
            if not hasattr(self, attr_name):
                setattr(self, attr_name, set())

        self._verify_attributes()

        # Initialise config
        _verify(inputs, self.inputs, self.optional_inputs)  # pylint: disable=no-member
        _verify(params, self.params, self.optional_params)  # pylint: disable=no-member

        job_id = str(uuid4()) if not job_id else job_id
        if not pipeline_dir:
            pipeline_dir = utils.get_pipeline_dir()
        job_dir = os.path.join(pipeline_dir, job_id)
        output_dir = os.path.join(job_dir, "output")

        outputs = dict()
        for key in self.outputs:  # pylint:disable=no-member
            outputs[key] = os.path.join(
                output_dir, self.outputs[key]  # pylint: disable=no-member
            )

        self.config = {}
        self.config["script_path"] = self.script_path  # pylint: disable=no-member
        self.config["job_id"] = job_id

        self.config["job_dir"] = job_dir

        if inputs:
            self.config["inputs"] = inputs

        if params:
            self.config["params"] = params

        self.config['outputs'] = outputs

        os.makedirs(output_dir, exist_ok=True)
        print(f"Created dirs for {job_id}")

        yaml.dump(self.config, open(os.path.join(job_dir, "config.yaml"), "w"))

        if utils.GIT_CONTROL:
            utils.save_git_sha(job_dir)

    def _verify_attributes(self):
        attrs = set(filter(lambda x: not x.startswith("_"), dir(self)))
        unexpected_attributes = attrs - self._expected_attributes
        if unexpected_attributes:
            raise AttributeError(
                f"Got unexpected attributes {unexpected_attributes}, allowed "
                f"attributes are {self._expected_attributes}"
            )


    def __getitem__(self, key):
        return self.config[key]

    def __str__(self):
        return pprint.pformat(self.__dict__, indent=3)


def _verify(data, expected_keys, optional_keys):
    if not data:
        data = dict()

    missing_keys = expected_keys - data.keys()
    unexpected_keys = data.keys() - expected_keys - optional_keys

    if unexpected_keys:
        raise RuntimeError(f"Got unexpected_keys inputs/params: {unexpected_keys}")
    if missing_keys:
        raise RuntimeError(f"Missing inputs/params: {missing_keys}")
