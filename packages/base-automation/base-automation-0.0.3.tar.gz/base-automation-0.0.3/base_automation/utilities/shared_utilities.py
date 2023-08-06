import ast
import json
import os
from base_automation import report


# ---------------------------- terminal ------------------------------------#

@report.utils.step('send terminal command: {command}')
def terminal_command(command):
    try:
        step_data(f"send command to terminal:\n{command}")
        return os.system(command)
    except Exception as e:
        step_data(e)


# ---------------------------- environment ------------------------------------#

@report.utils.step("get environment items")
def get_environment_items(key):
    return os.environ.items()


@report.utils.step("get environment variable: {key}")
def get_environment_variable(key):
    return os.environ.get(key)


@report.utils.step("set environment variable: {key}, {value}")
def set_environment_variable(key, value):
    os.environ.setdefault(key, value)


# ---------------------------- report data ------------------------------------#

@report.utils.step('{step_description}')
def step_data(step_description):
    pass


@report.utils.step("assert validation - {step_description}")
def compare_data(first_condition, second_condition, step_description=None, positive_test=True):
    if positive_test:
        assert first_condition == second_condition
    else:
        assert first_condition != second_condition


# ---------------------------- files actions ------------------------------------#

@report.utils.step("dict to json")
def dict_to_json(string_content):
    return json.dumps(str_to_dict(string_content))


@report.utils.step("str to dict")
def str_to_dict(string_content):
    return ast.literal_eval(str(string_content))


@report.utils.step("load json")
def load_json(json_content):
    return json.loads(json_content)


@report.utils.step("create temp json")
def create_temp_json(file_path, data):
    json_file = open(file_path, "w")
    json_file.write(data)
    json_file.close()
