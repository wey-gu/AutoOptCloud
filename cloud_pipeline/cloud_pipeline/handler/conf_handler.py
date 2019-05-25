from string import Template
import os
import subprocess
import numpy as np
from ..config import APPLY_CONF_TEMPLATE_PATH, ARG_KEYS
from ..utils.logger import Logger

logger = Logger(__name__)
_ = logger.get_logger()


class PuppetTemplate(Template):
    """
    PuppetTemplate

    It inherits from string.Template

    reference: https://docs.python.org/3.4/library/string.html#format-examples

    This Template will treat %foo as variable named foo.

    For example:
        PuppetTemplate(abc.txt).substitute(foo="bar") will render abc.txt
        with '%foo' replaced by 'bar'

    :param template: template of string to be renderred
    :type template: str

    """
    delimiter = '%'


class ConfHandler():
    """
    ConfHandler

    :param arg: argument dict to be applied
    :type arg: dict

    arg = dict(zip(ARG_KEYS, values))
    """

    def __init__(self, arg_dict):
        self.arg_validator(arg_dict)
        arg = {key: str(arg_dict[key]) for key in arg_dict}
        try:
            self.apply_command = self._build_command(arg)
        except FileNotFoundError as e:
            _.error(str(e))

    def apply(self):
        return self._issue_command(self.apply_command)

    def arg_validator(self, arg):
        for key in ARG_KEYS:
            try:
                assert (
                    key in arg), "Invalid arg: missing %s in arguments" % (key)
                assert (
                    type(arg[key]) in [float, np.float32, np.float64]
                ), "Invalid tye: %s should be float" % (key)
            except AssertionError as e:
                _.error(str(e))
                raise
        _.info("Arguments is valid: %s" % (str(arg)))

    def _build_command(self, arg):
        template_path = os.path.join(
            os.path.dirname(__file__),
            '..',
            APPLY_CONF_TEMPLATE_PATH)
        with open(template_path, 'r') as template_file:
            template_string = template_file.read()
        puppet_string = PuppetTemplate(template_string).substitute(**arg)
        command_string = "/usr/bin/puppet apply -e '" + puppet_string + "'"
        return command_string

    def _issue_command(self, command):
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
