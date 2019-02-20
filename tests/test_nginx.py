import requests
import re


def test_nginx_accessible():
    """
    Nginx is accessible through external DNS
    """
    r = requests.get('http://terraform-example-elb-40329900.us-west-2.elb.amazonaws.com')
    assert 'Welcome to nginx!' in r.text


def test_nginx_ssg(remote):
    out = remote.run('ps aux | grep nginx')
    assert 'master process' in out['stdout']
    assert 'worker process' in out['stdout']


def test_nginx_port(remote):
    out = remote.run('netstat -tulpn | grep :80')['stdout']
    assert re.search(r'(tcp\s .*/nginx).*\n(tcp6).*(nginx)', out)


def test_worker_config(remote):
    out = remote.run('cat /etc/nginx/nginx.conf')['stdout']
    assert re.search(r'\nworker_processes auto;', out)
    # TODO: config parser

def test_nginx_log(remote):
    pass
