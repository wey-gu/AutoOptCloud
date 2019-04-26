from string import Template
from ..config import APPLY_CONF_TEMPLATE_PATH, ARG_KEYS
import os
import subprocess


class puppetTemplate(Template):
    """
    puppetTemplate

    It inherits from string.Template

    reference: https://docs.python.org/3.4/library/string.html#format-examples

    This Template will treat %foo as variable named foo.

    For example:
        puppetTemplate(abc.txt).substitute(foo="bar") will render abc.txt
        with '%foo' replaced by 'bar'

    :param template: template of string to be renderred
    :type template: str

    """
    delimiter = '%'


class ConfHandler:
    """
    ConfHandler

    :param arg: argument dict to be applied
    :type arg: dict

    ARG_KEYS = [
        "w_disk",
        "w_user_percent",
        "w_user_p",
        "w_iowait_p",
        "w_frequency",
        "w_idle_p",
        "w_p",
        "w_kernel_p"]
    arg = dict(zip(ARG_KEYS, values))
    """
    def __init__(self, arg):
        self.apply_command = self._build_command(arg)

    def apply(self):
        return self._issue_command(self.apply_command)

    def _build_command(arg):
        templatePath = os.path.join(
            os.path.dirname(__file__),
            '..',
            APPLY_CONF_TEMPLATE_PATH)
        with open(templatePath, 'r') as file:
            templateString = file.read()
        puppetString = puppetTemplate(templateString).substitute(**arg)
        commandString = "/usr/bin/puppet apply -e '" + puppetString + "'"
        return commandString

    def _issue_command(command):
        output, error = subprocess.Popen(
            command,
            universal_newlines=True,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
            ).communicate()
        return output, error

    def cleanup(self):
        values = [0] * len(ARG_KEYS)
        arg = dict(zip(ARG_KEYS, values))
        restore_command = self._build_command(arg)
        return self._issue_command(restore_command)
