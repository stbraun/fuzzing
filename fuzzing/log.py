# coding=utf-8
"""Logging support.

More convenient logging support built on top of logging package.
"""

import logging
import logging.config
import pkgutil
import yaml

from gp_decorators.singleton import singleton


# noinspection PyArgumentList
@singleton
class LoggerFactory(object):
    """Create and manage logger instances.

    It is important to initialize the logging framework before
    the first call to a logger.
    """
    def __init__(self, package_name='fuzzing', config_file='resources/log_config.yaml'):
        self.package_name = package_name
        self.config_file = config_file
        self.config = None

    def initialize(self):
        """Initialize logging framework.

        Must be called before first logging attempt!
        """
        self.config = self.__read_configuration()
        logging.config.dictConfig(self.config)

    @staticmethod
    def get_instance(identifier):
        """Get a logger instance.

        :param identifier: identifier of logger as addressed in configuration.
        :return: the requested logger.
        """
        logger = logging.getLogger(identifier)
        return logger

    def __read_configuration(self):
        """Read the logging configuration from file.

        :return: configuration dictionary
        :rtype: dict
        """
        cfg = pkgutil.get_data(self.package_name, self.config_file)
        conf_dict = yaml.load(cfg)
        return conf_dict
