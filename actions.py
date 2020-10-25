from argparse import Action

from repo import Repo
from utils import ConfigParser
from version import Version


class RepositoryCreator(Action):
    def __call__(self, parser, namespace, value, option_string=None):
        if option_string in self.option_strings:
            setattr(namespace, self.dest, Repo(option_string))


class VersionCreator(Action):
    def __call__(self, parser, namespace, value, option_string=None):
        if option_string in self.option_strings:
            setattr(namespace, self.dest, Version().parse(value))


class ConfigReader(Action):
    def __call__(self, parser, namespace, value, option_string=None):
        if option_string in self.option_strings:
            setattr(namespace, self.dest, ConfigParser.parse(value))
