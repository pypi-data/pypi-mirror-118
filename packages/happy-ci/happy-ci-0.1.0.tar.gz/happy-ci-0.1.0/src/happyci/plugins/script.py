
from . import command


def run(stage, ctx):
    cmd = stage['script']
    return command.run_script(cmd)
