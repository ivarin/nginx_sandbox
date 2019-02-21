import pytest
from tools.remote import Remote
from tools import conf


def pytest_addoption(parser):
    parser.addoption('--name', action='store', default=conf.get('environment', 'name'))
    parser.addoption('--address', action='store', default=conf.get('environment', 'host_ip'))


@pytest.fixture
def name(request):
    addr = request.config.option.name
    if not addr.startswith('http://'):
        addr = 'http://%s' % addr
    yield addr


@pytest.fixture(scope='session')
def remote(request):
    with Remote(request.config.option.address) as remote:
        yield remote
