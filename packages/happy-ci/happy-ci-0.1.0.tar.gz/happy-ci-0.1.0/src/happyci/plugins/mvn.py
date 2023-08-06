from . import command


def run(stage, ctx):
    options = stage['options']
    command_line = ['mvn']
    mvn_opts = options.get('mvn_opts', '')
    command_line.append(mvn_opts)
    command_line.append(options['goal'])

    cmd = ' '.join(command_line)
    print('running maven command: %s' % cmd)
    command.run_command(cmd, True)
