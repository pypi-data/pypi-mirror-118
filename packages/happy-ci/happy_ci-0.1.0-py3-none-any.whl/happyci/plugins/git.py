
import urllib.parse
from .command import run_script


def run(stage, ctx):
    options = stage['options']
    username = options.get('username', '')
    password = options.get('password', '')

    auth = ''
    if username:
        auth = urllib.parse.quote(username)
        if password:
            auth += ':' + urllib.parse.quote(password)

    url = options['repository']
    if auth:
        scheme_pos = url.find('://')
        if scheme_pos > 0:
            url = url[:scheme_pos + 3] + auth + '@' + url[scheme_pos+3:]

    branch = options.get('branch', 'master')

    git_script = '''
    git init
    git remote add origin "%s"
    git fetch
    git checkout %s
    ''' % (url, branch)

    run_script(git_script)
