import pytest

def pytest_addoption(parser):
    parser.addoption("--browser", action="store", help="Select Browser")


option = None


def pytest_configure(config):
    global option
    option = config.option


@pytest.fixture()
def browser(request):
    request.config.getoption("--browser")
