from paramiko import SSHClient, AutoAddPolicy, RSAKey
import time


class Remote:
    def __init__(self, host):
        self.host = host
        self.tries = 5
        self.connection = None
        pass

    def connect(self):
        client = SSHClient()
        client.set_missing_host_key_policy(AutoAddPolicy)
        for _ in range(self.tries):
            try:
                client.connect(
                    hostname=self.host,
                    username='ubuntu',
                    key_filename='/Users/ivarin/.ssh/terraform',
                )
                return client
            except Exception as e:
                print(e)
                time.sleep(10)

    def run(self, cmd, sudo=True):
        if sudo:
            cmd = 'sudo %s' % cmd
        _, stdout, stderr = self.connection.exec_command(cmd, get_pty=True)
        out = {
            'stdout': stdout.read().decode('utf-8'),
            'stderr': stderr.read().decode('utf-8'),
            'es': stdout.channel.recv_exit_status()
        }
        return out

    def __enter__(self):
        self.connection = self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.connection:
            self.connection.close()
            self.connection = None
