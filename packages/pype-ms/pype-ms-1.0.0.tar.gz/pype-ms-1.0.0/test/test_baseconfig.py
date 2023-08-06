import os

import pytest
import yaml

from pype import BaseConfig


class MockConfig(BaseConfig):
    script_path = "/mock/path"
    params = {"param"}
    optional_params = {"optional_param"}
    inputs = {"input"}
    optional_inputs = {"optional_input"}
    outputs = {"result": "result.ext"}


params = {"param": 1, "optional_param": 2}
inputs = {"input": 1, "optional_input": 2}


def test_mockconfig_can_instantiate(tmpdir):
    MockConfig(job_id="bla", pipeline_dir=tmpdir, params=params, inputs=inputs)


def test_mockconfig_can_has_attributes(tmpdir):
    config = MockConfig(job_id="bla", pipeline_dir=tmpdir, params=params, inputs=inputs)

    for key in ["inputs", "params", "outputs", "job_id"]:
        assert key in config.config


def test_mockconfig_can_instantiate_twice(tmpdir):
    MockConfig(job_id="foo", pipeline_dir=tmpdir, params=params, inputs=inputs)
    config = MockConfig(job_id="bar", pipeline_dir=tmpdir, params=params, inputs=inputs)

    assert config["outputs"]["result"].endswith("bar/output/result.ext")


def test_mock_config_creates_the_right_paths(tmpdir):
    config = MockConfig(job_id="bla", pipeline_dir=tmpdir, params=params, inputs=inputs)

    assert os.path.exists(os.path.join(tmpdir, config["job_id"], "output"))
    assert os.path.exists(os.path.join(tmpdir, config["job_id"], "git_sha.txt"))
    assert os.path.exists(os.path.join(tmpdir, config["job_id"], "config.yaml"))


def test_cant_instantiate_when_missing_input(tmpdir):
    with pytest.raises(RuntimeError):
        MockConfig(params=params, pipeline_dir=tmpdir, inputs=dict())


def test_cant_instantiate_when_missing_param(tmpdir):
    with pytest.raises(RuntimeError):
        MockConfig(params=dict(), inputs=inputs, pipeline_dir=tmpdir)


def test_cant_instantiate_with_unexpected_input(tmpdir):
    with pytest.raises(RuntimeError):
        inputs.update({"unexpected_input": "2"})
        MockConfig(params=params, inputs=inputs, pipeline_dir=tmpdir)


def test_cant_instantiate_with_unexpected_param(tmpdir):
    with pytest.raises(RuntimeError):
        params.update({"unexpected_param": "2"})
        MockConfig(params=params, inputs=inputs, pipeline_dir=tmpdir)


def test_cant_create_class_with_wrong_attributes(tmpdir):
    class WrongConfig(BaseConfig):
        script_path = "script/path"
        wrong_name_for_inputs = {"hello"}

    with pytest.raises(AttributeError):
        WrongConfig(pipeline_dir=tmpdir)


# def mock_job(config):
#     f = open(config["output_paths"]["result"], "w")
#     f.write(config["params"]["string"])
#
#
# def test_integration(tmpdir):
#     params = {"string": "Hello World!"}
#     config = MockConfig(pipeline_dir=tmpdir, job_id="bla", params=params)
#     config.save()
#
#     loaded_config = yaml.load(
#         open(os.path.join(config.output_dir, "config.yaml")), Loader=yaml.FullLoader
#     )
#
#     mock_job(loaded_config)
#
# def test_script_path_in_dict(tmpdir):
#     params = {"string": "Hello World!"}
#     config = MockConfig(pipeline_dir=tmpdir, job_id="bla", params=params)
#     assert "script_path" in config.__dict__
#
#
# def test_config_throws_error_without_script_path(tmpdir):
#     class MockConfigWithoutScriptPath(BaseConfig):
#         pass
#
#     with pytest.raises(Exception):
#         _ = MockConfigWithoutScriptPath(tmpdir)
#
# class MockConfigDefault(BaseConfig):
#     default_params = {"default_param": 1}
#     default_inputs = {"default_input": 2}
#     outputs = {"result": "result"}
#     script_path = "/bla/bla"
#
#
# def test_instantiate_default_config_without_values(tmpdir):
#     mockconfig = MockConfigDefault(pipeline_dir=tmpdir, job_id="bla", )
#
#     assert "default_param" in mockconfig.params
#     assert mockconfig.params["default_param"] == 1
#     assert "default_input" in mockconfig.inputs
#     assert mockconfig.inputs["default_input"] == 2
#
#
# def test_instantiate_default_config_with_values(tmpdir):
#     params = {"default_param": 3}
#     inputs = {"default_input": 4}
#     mockconfig = MockConfigDefault(pipeline_dir=tmpdir, job_id="bla", params=params, inputs=inputs)
#
#     assert "default_param" in mockconfig.params
#     assert mockconfig.params["default_param"] == 3
#     assert "default_input" in mockconfig.inputs
#     assert mockconfig.inputs["default_input"] == 4
