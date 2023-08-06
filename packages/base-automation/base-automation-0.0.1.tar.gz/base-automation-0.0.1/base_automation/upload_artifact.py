import os
import shutil
from base_automation import report
from base_automation.utilities import shared_utilities


@report.step('delete dist directory')
def delete_dist_dir(dist_dir):
    if os.path.exists(dist_dir) and os.path.isdir(dist_dir):
        shutil.rmtree(dist_dir)
    else:
        print("The dist directory does not exist")


@report.step("build")
def build():
    build_commands = ["python setup.py develop",
                      "python -m pip install --upgrade pip",
                      "python -m pip install --upgrade build", "python -m build"]
    for command in build_commands:
        shared_utilities.terminal_command(command)


@report.step("upload artifact to {azure_feed_name}")
def upload_azure_artifact(azure_feed_name):
    upload_commands = ["python setup.py sdist bdist_wheel", f"twine upload -r {azure_feed_name} dist/*"]

    for command in upload_commands:
        shared_utilities.terminal_command(command)


@report.step("upload artifact to {azure_feed_name}")
def upload_azure_artifact(azure_feed_name):
    upload_commands = ["python setup.py sdist bdist_wheel", f"twine upload -r {azure_feed_name} dist/*"]

    for command in upload_commands:
        shared_utilities.terminal_command(command)


@report.feature('Build & Upload New Artifact To Azure')  # A sub-function function at large
@report.severity("normal")  # Priority of test cases - 'blocker', 'critical', 'normal', 'minor', 'trivial'
def run_process(dist_dir, azure_feeds: list):
    delete_dist_dir(dist_dir)
    build()
    # upload artifact to a specific feeds
    for feed in azure_feeds:
        upload_azure_artifact(feed)
