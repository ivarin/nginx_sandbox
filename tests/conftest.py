import pytest
from fixtures.remote import Remote
from fixtures import conf

host = conf.get('environment', 'host_ip')


@pytest.fixture(scope='session')
def remote():
    with Remote(host) as remote:
        yield remote
