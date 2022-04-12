# Configure logging

import pytest, os
from pathlib import Path


@pytest.hookimpl(hookwrapper=True,tryfirst=True)
def logs_info_file_test(item):
    config=item.config
    logging_plugin=config.pluginmanager.get_plugin("logging-plugin")
    filename=Path('info', item._request.node.name+".log")
    logging_plugin.set_log_path(str(filename))
    assert os.path.exists(filename) == True

@pytest.hookimpl(hookwrapper=True,tryfirst=True)
def logs_debug_file_test(item):
    config=item.config
    logging_plugin=config.pluginmanager.get_plugin("logging-plugin")
    filename=Path('debug', item._request.node.name+".log")
    logging_plugin.set_log_path(str(filename))
    assert os.path.exists(filename) == True
