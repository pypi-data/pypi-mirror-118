import os
import json
from base_automation import report
from base_automation.utilities import shared_utilities
from genson import SchemaBuilder
from jsonschema import validate


class JsonSchema:

    def __init__(self):
        self._builder = SchemaBuilder()
        self._json_instance = None
        self._schema = None
        self._temp_schema = None
        self._result = None

    @report.step("create schema")
    def initiate_schema(self, file_path=None, json_content_is_exists=None, save_file_name_path=None):
        if file_path is not None:
            with open(file_path, 'r') as file:
                self._json_instance = shared_utilities.load_json(file.read())
        else:
            self._json_instance = json.dumps(json_content_is_exists)

        if save_file_name_path is not None and not os.path.exists(save_file_name_path):
            with open(save_file_name_path, 'w') as file:
                self._builder.add_object(self._json_instance)
                self._temp_schema = self._builder.to_schema()
                file.write(json.dumps(self._temp_schema))
                file.close()

        self.__read_schema(file_path=save_file_name_path, schema_content=json_content_is_exists)

    @report.report.step("read schema")
    def __read_schema(self, file_path=None, schema_content=None):
        if file_path is not None:
            with open(file_path, 'r') as file:
                self._schema = shared_utilities.load_json(file.read())

        else:
            self._schema = schema_content

    @report.report.step("validate schema")
    def validate_schema(self):
        try:
            self._result = validate(instance=self._json_instance, schema=self._schema)
            shared_utilities.step_data("The schema test finish with success")
        except Exception as e:
            shared_utilities.step_data(f"Exception:\n{e.__str__()}")
            assert False
