import requests
import re
from tools import conf

addr = 'http://terraform-example-elb-40329900.us-west-2.elb.amazonaws.com'


def test_nginx_accessible(address):
    """
    Nginx is accessible through external DNS
    """
    r = requests.get(address)
    assert r.status_code == 200
    assert 'Welcome to nginx!' in str(r.content)


def test_nginx_workers(remote):
    out = remote.run('ps aux | grep nginx')
    assert 'master process' in out['stdout']
    assert 'worker process' in out['stdout']


def test_nginx_port(remote):
    out = remote.run('netstat -tulpn | grep :80')['stdout']
    assert re.search(r'(tcp\s .*/nginx).*\n(tcp6).*(nginx)', out)


def test_worker_config(remote):
    conf_file = conf.get('nginx', 'config')
    out = remote.run('cat %s' % conf_file)['stdout']
    assert re.search(r'\nworker_processes auto;', out)
    # TODO: config parser


def test_nginx_log(remote):
    access_log = conf.get('nginx', 'access_log')
    last_access = remote.run('tail -1 %s' % access_log)['stdout']
    r = requests.get(addr)
    access = remote.run('tail -1 %s' % access_log)['stdout']
    assert access != last_access
    assert 'python-requests' in access
