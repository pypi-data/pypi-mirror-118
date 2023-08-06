
import os
import argparse
import yaml
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

NAME = 'happy-ci'

from . import logger
from .stage_runner import run_stage
from ._version import __version__

BANNER = r'''
     _    _                            _____ _____ 
    | |  | |                          / ____|_   _|
    | |__| | __ _ _ __  _ __  _   _  | |      | |  
    |  __  |/ _` | '_ \| '_ \| | | | | |      | |  
    | |  | | (_| | |_) | |_) | |_| | | |____ _| |_ 
    |_|  |_|\__,_| .__/| .__/ \__, |  \_____|_____|
                 | |   | |     __/ |               
                 |_|   |_|    |___/        
'''


class HappyCiContext:
    """
    the running context of happy ci
    the main purpose is to manage environment variables
    """
    def __init__(self, envs={}):
        self.envs = envs

    def set_env(self, key, val):
        self.envs[key] = val


def run_stages(stages, ctx):
    for stage in stages:
        run_stage(stage, ctx)


def run(args):
    """
    start to run the file
    :param args: options parsed from command line args
    :return: None
    """

    run_file = args.run_file
    if run_file.startswith('http://') or run_file.startswith('https://'):
        import urllib.request
        run_file_stream = urllib.request.urlopen(run_file)
    else:
        if os.path.exists(run_file) and os.path.isfile(run_file):
            run_file_stream = open(run_file)
        else:
            print('run file %s does not exist or is not readable' % run_file)
            exit(1)

    run_conf = yaml.load(run_file_stream, Loader=Loader)
    envs_overrides = {}
    if args.envs:
        print('Environment variables overrides')
        print('\n'.join(args.envs))
        envs_overrides = dict([tuple(e.split('=')) for e in args.envs])

    envs = run_conf.get('envs', {})
    envs.update(dict(envs_overrides))

    if args.config_file:
        ctx = yaml.load(open(args.config_file), Loader=Loader)
    else:
        ctx = {}

    local_dir = os.path.abspath(args.local_dir)
    if os.path.exists(local_dir):
        if os.path.isfile(local_dir):
            logger.fail('local dir', local_dir, 'is a file')
            return
        else:
            print('using work directory %s' % local_dir)
            os.chdir(local_dir)
    else:
        try:
            os.makedirs(local_dir, mode=0o755)
            os.chdir(local_dir)
        except Exception as e:
            logger.fail('local dir', local_dir, 'does not exist and can not be created', str(e))
            return

    if envs:
        os.environ.update(envs)

    run_stages(run_conf['stages'], ctx)


def parse_options():
    class ShowVersion(argparse.Action):
        def __call__(self, parser, namespace, values, option_string):
            parser.exit(message=__version__)

    parser = argparse.ArgumentParser(prog='happyci', description='Happy CI')
    parser.add_argument('--conf', '-c', dest='config_file', help='configuration file path')
    parser.add_argument('--file', '-f', dest='run_file', required=True,
                        help='file to run on. it can be a normal file or an http(s) url')
    parser.add_argument('--directory', '-d', dest='local_dir', required=True,
                        help='local_dir to run in, must be empty')
    parser.add_argument('--verbose', '-v', action='store_const', const=True, default=False, dest='verbose',
                        help='verbose')
    parser.add_argument('--environment', '-e', dest='envs', action='append',
                        help='envs to override that is defined in run_file')
    parser.add_argument('--version', '-V', nargs=0, dest='version', action=ShowVersion,
                        help='show version and exit')

    args = parser.parse_args()

    logger.debug('happy ci started on file %s' % args.run_file)
    return args


def main():
    happy_ci_args = parse_options()
    if not happy_ci_args.version:
        print(BANNER)
        run(happy_ci_args)
