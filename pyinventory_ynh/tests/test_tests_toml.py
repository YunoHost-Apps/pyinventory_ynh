import tomllib

from bx_py_utils.path import assert_is_file
from django.test.testcases import TestCase
from django_yunohost_integration.path_utils import get_project_root


class TestsTomlTestCase(TestCase):
    def test_load_tests_toml(self):
        tests_toml_file = get_project_root() / 'tests.toml'
        assert_is_file(tests_toml_file)

        # Just test if it can be loaded without errors:
        tomllib.load(tests_toml_file.open('rb'))
