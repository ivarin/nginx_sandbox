import pytest
from tools.remote import Remote
from tools import conf

host = conf.get('environment', 'host_ip')


def pytest_addoption(parser):
    parser.addoption("--name", action="store")


@pytest.fixture
def name(request):
    addr = request.config.option.name
    if not addr.startswith('http://'):
        addr = 'http://%s' % addr
    yield addr


@pytest.fixture(scope='session')
def remote():
    with Remote(host) as remote:
        yield remote
