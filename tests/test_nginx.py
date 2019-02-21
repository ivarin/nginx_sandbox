import requests
import re
from tools import conf


def test_nginx_accessible(name):
    """
    Nginx is accessible through external DNS
    """
    r = requests.get(name)
    assert r.status_code == 200
    assert 'Welcome to nginx!' in str(r.content)


def test_nginx_workers(remote):
    """
    nginx workers are running
    """
    out = remote.run('ps aux | grep nginx')
    assert 'master process' in out['stdout']
    assert 'worker process' in out['stdout']


def test_nginx_port(remote):
    """
    check nginx listens on port 80
    """
    out = remote.run('netstat -tulpn | grep :80')['stdout']
    assert re.search(r'(tcp\s .*/nginx).*\n(tcp6\s .*/nginx)', out)


def test_worker_config(remote):
    """
    validate uncommented setting in config file
    """
    conf_file = conf.get('nginx', 'config')
    out = remote.run('cat %s' % conf_file)['stdout']
    assert re.search(r'\nworker_processes auto;', out)
    # TODO: config parser


def test_nginx_log(remote, name):
    """
    check proper access logging
    """
    access_log = conf.get('nginx', 'access_log')
    last_access = remote.run('tail -1 %s' % access_log)['stdout']
    r = requests.get(name)
    access = remote.run('tail -1 %s' % access_log)['stdout']
    assert re.search(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', access)
    assert access != last_access
    assert 'python-requests' in access
