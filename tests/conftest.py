import configparser
import pytest
from fixtures.remote import Remote

conf = configparser.ConfigParser()
conf.read('config.ini')
host = conf.get('environment', 'host_ip')


@pytest.fixture(scope='session')
def remote():
    with Remote(host) as remote:
        yield remote
