# coding=utf-8
"""Feature test steps for logging."""

from behave import *
import logging

from fuzzing.log import LoggerFactory


@given("a logger called {logger_name}")
def step_impl(context, logger_name):
    """Create a logger.

    :param context: test context.
    :param logger_name: name of logger to create.
    """
    package = __package__
    logger = LoggerFactory(package, config_file="").get_instance(logger_name)
    assert logger is not None
    logger.fatal("package: -{}-".format(package))
    assert logger.isEnabledFor(logging.ERROR)
    context.logger = logger


@given("no specific configuration.")
def step_impl(context):
    """

    :param context:
    """
    logger = context.logger
    assert not logger.isEnabledFor(logging.DEBUG)
    logger.warning(logger.getEffectiveLevel())
    logger.warning("-warning-" + str(logging.WARNING))
    logger.debug("-debug-" + str(logging.DEBUG))
    logger.info("-info-" + str(logging.INFO))
    # assert False


@when('logging {log_message} to {log_level}')
def step_impl(context, log_message, log_level):
    """

    :param context:
    :param log_message:
    :param log_level:
    """
    logger = context.logger


@then('{log_message} is written to standard error with {severity_marker}.')
def step_impl(context, log_message, severity_marker):
    """

    :param context:
    :param log_message:
    :param severity_marker:
    """
    assert False

