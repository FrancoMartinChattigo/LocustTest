import os


process_number = int(
    ''.join(caracter for caracter in os.environ.get("PYTEST_XDIST_WORKER", "0") if caracter.isdigit()))


def pytest_addoption(parser):
    parser.addoption("--env", action="store", default="support-bugs", help="leones, pantera, bugs, support-bugs")


def pytest_configure(config):
    os.environ["env"] = config.getoption('env')
    os.environ["users_loading"] = config.getoption('users_loading')
    os.environ["browser"] = config.getoption('browser')
    os.environ["notification_popup"] = config.getoption('notification_popup')
    os.environ["headless"] = config.getoption('headless')
    os.environ["log_level"] = config.getoption('log_level')


