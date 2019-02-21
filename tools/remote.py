from paramiko import SSHClient, AutoAddPolicy
import time
from tools import conf, logger
import os


class Remote:
    def __init__(self, host):
        self.host = host
        self.tries = 5
        self.connection = None
        pass

    def connect(self):
        client = SSHClient()
        client.set_missing_host_key_policy(AutoAddPolicy)
        logger.info('\nConnecting to %s' % self.host)
        for _ in range(self.tries):
            try:
                client.connect(
                    hostname=self.host,
                    username='ubuntu',
                    key_filename=os.path.expanduser(conf.get('environment', 'ssh_key'))
                )
                return client
            except Exception as e:
                logger.info('%s occurred') % e
                time.sleep(10)

    def run(self, cmd, sudo=True):
        if sudo:
            cmd = 'sudo %s' % cmd
        logger.info('\nRunning %s' % cmd)
        _, stdout, stderr = self.connection.exec_command(cmd, get_pty=True)
        out = {
            'stdout': stdout.read().decode('utf-8'),
            'stderr': stderr.read().decode('utf-8'),
            'es': stdout.channel.recv_exit_status()
        }
        if out['stderr']:
            logger.info(out['stderr'])
        return out

    def __enter__(self):
        self.connection = self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.connection:
            self.connection.close()
            self.connection = None
