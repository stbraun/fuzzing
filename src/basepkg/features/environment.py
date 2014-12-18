# coding=utf-8
"""General settings for feature tests."""

from gp_tools.log import LoggerFactory


def before_all(context):
    """Setup before all tests.

    Initialize the logger framework.

    :param context: test context.
    """
    lf = LoggerFactory('gp_tools', config_file='../features/resources/test_config.yaml')
    lf.initialize()
    ll = lf.get_instance('environment')
    ll.info('Logger initialized: {}'.format(lf.config))
