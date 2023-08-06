import os
import shutil
from base_automation import report
from base_automation.utilities import shared_utilities


@report.utils.step('delete dist directory')
def delete_dist_dir(dist_dir):
    if os.path.exists(dist_dir) and os.path.isdir(dist_dir):
        shutil.rmtree(dist_dir)
    else:
        print("The dist directory does not exist")


@report.utils.step("build")
def build():
    build_commands = ["python setup.py develop",
                      "python -m pip install --upgrade pip",
                      "python -m pip install --upgrade build", "python -m build"]
    for command in build_commands:
        shared_utilities.terminal_command(command)


@report.utils.step("upload artifact to {azure_feed_name}")
def upload_azure_artifact(azure_feed_name):
    upload_commands = ["python setup.py sdist bdist_wheel", f"twine upload -r {azure_feed_name} dist/*"]

    for command in upload_commands:
        shared_utilities.terminal_command(command)


@report.utils.step("upload pypi artifact")
def upload_pypi_artifact():
    upload_commands = ["python setup.py sdist bdist_wheel",
                       f"twine upload -u {shared_utilities.get_environment_variable('pypi-user')} -p {shared_utilities.get_environment_variable('pypi-password')} --repository-url https://upload.pypi.org/legacy/ dist/*"]
    for command in upload_commands:
        shared_utilities.terminal_command(command)


@report.utils.feature('Build & Upload New Artifact To Azure')  # A sub-function function at large
@report.utils.severity("normal")  # Priority of test cases - 'blocker', 'critical', 'normal', 'minor', 'trivial'
def run_process(dist_dir, azure_feeds: list = None, azure_artifact: bool = False, pypi_artifact: bool = False):
    # delete_dist_dir(dist_dir)
    # build()
    if pypi_artifact:
        upload_pypi_artifact()
    if azure_artifact:
        for feed in azure_feeds:
            upload_azure_artifact(feed)
