"""
Tests for utilities used by the filters tooling.
"""
from unittest.mock import patch

import ddt
from django.test import TestCase, override_settings

from ..utils import get_filter_config, get_functions_for_pipeline, get_pipeline_configuration


def test_function():
    """
    Utility function used when getting functions for pipeline.
    """


@ddt.ddt
class TestUtilityFunctions(TestCase):
    """
    Test class to verify standard behavior of utility functions.
    """

    def test_get_empty_function_list(self):
        """
        This method is used to verify the behavior of
        get_functions_for_pipeline when an empty pipeline is
        passed as argument.

        Expected behavior:
            Returns an empty list.
        """
        pipeline = []

        function_list = get_functions_for_pipeline(pipeline)

        self.assertEqual(function_list, pipeline)

    def test_get_non_existing_function(self):
        """
        This method is used to verify the behavior of
        get_functions_for_pipeline when a non-existing function
        path is passed inside the pipeline argument.

        Expected behavior:
            Returns a list without the non-existing function.
        """
        pipeline = [
            "openedx_filters.tests.test_utils.test_function",
            "openedx_filters.tests.test_utils.non_existent",
        ]
        log_message = "Failed to import '{}'.".format(
            "openedx_filters.tests.test_utils.non_existent"
        )

        with self.assertLogs() as captured:
            function_list = get_functions_for_pipeline(pipeline)

        self.assertEqual(
            captured.records[0].getMessage(), log_message,
        )
        self.assertEqual(function_list, [test_function])

    def test_get_non_existing_module_func(self):
        """
        This method is used to verify the behavior of
        get_functions_for_pipeline when a non-existing module
        path is passed inside the pipeline argument.

        Expected behavior:
            Returns a list without the non-existing function.
        """
        pipeline = [
            "openedx_filters.tests.test_utils.test_function",
            "openedx_filters.non_existent.test_utils.test_function",
        ]
        log_message = "Failed to import '{}'.".format(
            "openedx_filters.non_existent.test_utils.test_function"
        )

        with self.assertLogs() as captured:
            function_list = get_functions_for_pipeline(pipeline)

        self.assertEqual(captured.records[0].getMessage(), log_message)
        self.assertEqual(function_list, [test_function])

    def test_get_function_list(self):
        """
        This method is used to verify the behavior of
        get_functions_for_pipeline when a list of functions
        paths is passed as the pipeline parameter.

        Expected behavior:
            Returns a list with the function objects.
        """
        pipeline = [
            "openedx_filters.tests.test_utils.test_function",
            "openedx_filters.tests.test_utils.test_function",
        ]

        function_list = get_functions_for_pipeline(pipeline)

        self.assertEqual(function_list, [test_function] * 2)

    def test_get_empty_hook_config(self):
        """
        This method is used to verify the behavior of
        get_filter_config when a trigger without a
        HOOKS_FILTER_CONFIG is passed as parameter.

        Expected behavior:
            Returns an empty dictionary.
        """
        result = get_filter_config("hook_name")

        self.assertEqual(result, {})

    @override_settings(
        HOOK_FILTERS_CONFIG={
            "openedx.service.context.location.type.vi": {
                "pipeline": [
                    "openedx_filters.tests.test_utils.test_function",
                    "openedx_filters.tests.test_utils.test_function",
                ],
                "fail_silently": False,
            }
        }
    )
    def test_get_hook_config(self):
        """
        This method is used to verify the behavior of
        get_filter_config when a trigger with
        HOOKS_FILTER_CONFIG defined is passed as parameter.

        Expected behavior:
            Returns a tuple with pipeline configurations.
        """
        expected_result = {
            "pipeline": [
                "openedx_filters.tests.test_utils.test_function",
                "openedx_filters.tests.test_utils.test_function",
            ],
            "fail_silently": False,
        }

        result = get_filter_config("openedx.service.context.location.type.vi")

        self.assertDictEqual(result, expected_result)

    @patch("openedx_filters.utils.get_filter_config")
    @ddt.data(
        (("openedx_filters.tests.test_utils.test_function",), ([], False,)),
        ({}, ([], False,)),
        (
            {
                "pipeline": [
                    "openedx_filters.tests.test_utils.test_function",
                    "openedx_filters.tests.test_utils.test_function",
                ],
                "fail_silently": False,
            },
            (
                [
                    "openedx_filters.tests.test_utils.test_function",
                    "openedx_filters.tests.test_utils.test_function",
                ],
                True,
            ),
        ),
        (
            [
                "openedx_filters.tests.test_utils.test_function",
                "openedx_filters.tests.test_utils.test_function",
            ],
            (
                [
                    "openedx_filters.tests.test_utils.test_function",
                    "openedx_filters.tests.test_utils.test_function",
                ],
                False,
            ),
        ),
        (
            "openedx_filters.tests.test_utils.test_function",
            (["openedx_filters.tests.test_utils.test_function", ], False,),
        ),
    )
    @ddt.unpack
    def test_get_pipeline_config(self, config, expected_result, get_filter_config_mock):
        """
        This method is used to verify the behavior of
        get_pipeline_configuration when a trigger with
        HOOKS_FILTER_CONFIG defined is passed as parameter.

        Expected behavior:
            Returns a tuple with the pipeline and exception handling
            configuration.
        """
        get_filter_config_mock.return_value = config

        result = get_pipeline_configuration("hook_name")

        self.assertTupleEqual(result, expected_result)
