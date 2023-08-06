import os
from base_automation import report
from base_automation.utilities import shared_utilities
import subprocess
import sys


@report.utils.step("run on windows")
def windows(ps_windows_path):
    subprocess.Popen(['powershell.exe', ps_windows_path], stdout=sys.stdout)


@report.utils.step("run on linux")
def linux():
    commands = [
        'curl -o allure-2.14.0.tgz -OLs https://repo.maven.apache.org/maven2/io/qameta/allure/allure-commandline/2.14.0/allure-commandline-2.14.0.tgz',
        'sudo tar -zxvf allure-2.14.0.tgz -C /opt/',
        'sudo ln -s /opt/allure-2.14.0/bin/allure /usr/bin/allure']

    for command in commands:
        shared_utilities.terminal_command(command)


@report.utils.step("run process")
def run_process(ps_windows_path):
    system = shared_utilities.get_system()
    if 'Windows' in system:
        windows(ps_windows_path=ps_windows_path)
    else:
        linux()

    shared_utilities.terminal_command('allure --version')
