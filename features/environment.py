# coding=utf-8
"""General settings for feature tests."""

from fuzzing.log import LoggerFactory


def before_all(context):
    """Setup before all tests.

    Initialize the logger framework.

    :param context: test context.
    """
    lf = LoggerFactory(config_file='../features/resources/test_config.yaml')
    lf.initialize()
    ll = lf.get_instance('environment')
    ll.info('Logger initialized: {}'.format(lf.config))
    ll.info('Initial test context: {}'.format(context))
