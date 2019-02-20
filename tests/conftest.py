import configparser
import pytest
from fixtures.remote import Remote

conf = configparser.ConfigParser()
conf.read('config.ini')
host = conf.get('environment', 'host_ip')


@pytest.fixture
def remote():
    with Remote(host) as remote:
        yield remote
