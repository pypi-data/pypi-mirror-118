import os
import time
import tempfile
import subprocess


def run_script(cmd):
    print('running script:')
    print(cmd)
    with tempfile.TemporaryDirectory() as tmpdirname:
        if os.name == 'nt':
            ext, shell = '.bat', 'cmd.exe /C'
        else:
            ext, shell = '.sh', 'sh'

        script_file = os.path.join(tmpdirname, '%s%s' % (time.time(), ext))
        with open(script_file, 'w') as fp:
            fp.write(cmd)

        proc = subprocess.Popen(shell + ' ' + script_file, shell=True)
        return proc.wait()


def run_command(command, shell=False):
    print('running command:')
    print(command)
    proc = subprocess.Popen(command, shell=shell)
    return proc.wait()
