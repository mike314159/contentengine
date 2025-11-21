# import loggerfactory as lf
import os
from uilib import formathelpers as fh

# #create the folder if not exist
# log_path = '/var/log/app'
# if not(os.path.exists(log_path)):
#     os.mkdir(log_path, 0o755)
#
# log = lf.LoggerFactory.get_logger(__name__)
#
#
# def test_log_info():
#     log.info("This is to test info logging")
#
# def test_log_warning():
#     log.warning("This is to test warning logging")
#
# def test_log_error():
#     log.error("This is to test error logging")
#
#
# test_log_info()
# test_log_warning()
# test_log_error()


def test_format_usd():
    s = fh.format_value_usd(123.456)
    assert s == "123.46"


test_format_usd()
