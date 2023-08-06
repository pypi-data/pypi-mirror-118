
import importlib
from .plugins import script, mvn, git, docker
from . import logger

# predefined plugins
plugin_register = {
    'script': script,
    'mvn': mvn,
    'git': git,
    'docker': docker
}


def import_plugin(plugin_name):
    """
    import a plugin from PYTHONPATH.
    happyci plugins are already imported, and aliased with a simple name
    without the dot between module and submodules

    for user provided plugins, they must be in a submodule, not top level ones.
    plugin_name without a dot will be treated as happyci plugins

    :param plugin_name: the plugin's module name
    :return: the plugin module
    """
    if plugin_name in plugin_register:
        p = plugin_register[plugin_name]
    else:
        if '.' in plugin_name:
            p = importlib.import_module(plugin_name)
        else:
            p = importlib.import_module('happyci.plugins.' + plugin_name)
        plugin_register[plugin_name] = p
    return p


def run_stage(stage, ctx):
    """
    run a stage, a stage is a single step in the ci/cd pipeline

    :param stage: the stage definition
    :param ctx: the HappyCiContext
    :return: None
    """

    # first get the plugin that will run this stage
    plugin_name = stage.get('plugin', 'script')
    logger.debug('\nRun stage %s with plugin %s' % (stage['name'], plugin_name))

    plugin = import_plugin(plugin_name)

    try:
        plugin.run(stage, ctx)
    except Exception as e:
        fail_on_error = stage.get('fail-on-error', 'true')
        if fail_on_error == 'true':
            raise Exception('Failed running stage %(name)s' % stage)
        else:
            import sys
            logger.fail('running stage %(name)s' % stage, file=sys.stderr)

