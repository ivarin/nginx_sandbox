import pytest
from tools.remote import Remote
from tools import conf

host = conf.get('environment', 'host_ip')


def pytest_addoption(parser):
    parser.addoption("--address", action="store")


@pytest.fixture
def address(request):
    addr = request.config.option.address
    if not addr.startswith('http://'):
        addr = 'http://%s' % addr
    yield addr


@pytest.fixture(scope='session')
def remote():
    with Remote(host) as remote:
        yield remote
