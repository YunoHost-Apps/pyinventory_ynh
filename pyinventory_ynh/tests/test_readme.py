from pathlib import Path

from bx_py_utils.auto_doc import assert_readme_block
from cli_base.cli_tools.test_utils.rich_test_utils import NoColorEnvRichClick, invoke
from django_yunohost_integration.path_utils import get_project_root
from manageprojects.tests.base import BaseTestCase

from pyinventory_ynh import constants


def assert_cli_help_in_readme(text_block: str, marker: str, readme_path: Path):
    text_block = text_block.replace(constants.CLI_EPILOG, '')
    text_block = f'```\n{text_block.strip()}\n```'
    assert_readme_block(
        readme_path=readme_path,
        text_block=text_block,
        start_marker_line=f'[comment]: <> (✂✂✂ auto generated {marker} start ✂✂✂)',
        end_marker_line=f'[comment]: <> (✂✂✂ auto generated {marker} end ✂✂✂)',
    )


class ReadmeTestCase(BaseTestCase):
    def test_dev_help(self):
        project_root = get_project_root()
        with NoColorEnvRichClick():
            stdout = invoke(cli_bin=project_root / 'dev-cli.py', args=['--help'], strip_line_prefix='usage: ')
        self.assert_in_content(
            got=stdout,
            parts=(
                'usage: ./dev-cli.py [-h]',
                ' check-code-style ',
                ' coverage ',
                constants.CLI_EPILOG,
            ),
        )
        assert_cli_help_in_readme(
            text_block=stdout,
            marker='help',
            readme_path=project_root / 'doc' / 'ADMIN.md',
        )
