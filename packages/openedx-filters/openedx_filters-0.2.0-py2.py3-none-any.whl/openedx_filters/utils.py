"""
Utilities for the hooks module.
"""
from logging import getLogger

from django.conf import settings
from django.utils.module_loading import import_string

log = getLogger(__name__)


def get_functions_for_pipeline(pipeline):
    """
    Get function objects from paths.

    Helper function that given a pipeline with functions paths gets
    the objects related to each path.

    Example usage:
        functions = get_functions_for_pipeline(
            [
                '1st_path_to_function',
                ...
            ]
        )
        >>> functions
        [
            <function 1st_function at 0x00000000000>,
            <function 2nd_function at 0x00000000001>,
            ...
        ]

    Arguments:
        pipeline (list): paths where functions are defined.

    Returns:
        function_list (list): function objects defined in pipeline.
    """
    function_list = []
    for function_path in pipeline:
        try:
            function = import_string(function_path)
            function_list.append(function)
        except ImportError:
            log.exception("Failed to import '%s'.", function_path)

    return function_list


def get_pipeline_configuration(hook_name):
    """
    Get pipeline configuration from filter settings.

    Helper function used to get the configuration needed to execute
    the Pipeline Runner. It will take from the hooks configuration
    the list of functions to execute and how to execute them.

    Example usage:
        pipeline_config = get_pipeline_configuration('trigger')
        >>> pipeline_config
            (
                [
                    'my_plugin.hooks.filters.test_function',
                    'my_plugin.hooks.filters.test_function_2nd',
                ],
            )

    Arguments:
        hook_name (str): determines which is the trigger of this
        pipeline.

    Returns:
        pipeline (list): paths where functions for the pipeline are
        defined.
        raise_exception (bool): defines whether exceptions are raised while
        executing the pipeline associated with a filter. It's determined by
        fail_silently configuration, True meaning it won't raise exceptions and
        False the opposite.
    """
    hook_config = get_filter_config(hook_name)

    if not hook_config:
        return [], False

    pipeline, raise_exception = [], False

    if isinstance(hook_config, dict):
        pipeline, raise_exception = (
            hook_config.get("pipeline", []),
            not hook_config.get("fail_silently", True),
        )

    elif isinstance(hook_config, list):
        pipeline = hook_config

    elif isinstance(hook_config, str):
        pipeline.append(hook_config)

    return pipeline, raise_exception


def get_filter_config(hook_name):
    """
    Get filters configuration from settings.

    Helper function used to get configuration needed for using
    Hooks Extension Framework.

    Example usage:
            configuration = get_filter_config('trigger')
            >>> configuration
            {
                'pipeline':
                    [
                        'my_plugin.hooks.filters.test_function',
                        'my_plugin.hooks.filters.test_function_2nd',
                    ],
                'fail_silently': False,
            }

            Where:
                - pipeline (list): paths where the functions to be executed by
                the pipeline are defined.
                - fail_silently (bool): determines whether the pipeline can
                raise exceptions while executing. If its value is True then
                exceptions (HookFilterException) are caught and the execution
                continues, if False then exceptions are re-raised and the
                execution fails.

    Arguments:
        hook_name (str): determines which configuration to use.

    Returns:
        hooks configuration (dict): taken from Django settings
        containing hooks configuration.
    """
    hooks_config = getattr(settings, "HOOK_FILTERS_CONFIG", {})

    return hooks_config.get(hook_name, {})
