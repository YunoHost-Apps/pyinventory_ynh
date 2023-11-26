from pathlib import Path

from bx_py_utils.auto_doc import assert_readme_block
from manageprojects.test_utils.click_cli_utils import invoke_click
from manageprojects.tests.base import BaseTestCase

from pyinventory_ynh.cli.dev import CLI_EPILOG, PACKAGE_ROOT, cli


def assert_cli_help_in_readme(text_block: str, marker: str, readme_path: Path):
    text_block = text_block.replace(CLI_EPILOG, '')
    text_block = f'```\n{text_block.strip()}\n```'
    assert_readme_block(
        readme_path=readme_path,
        text_block=text_block,
        start_marker_line=f'[comment]: <> (✂✂✂ auto generated {marker} start ✂✂✂)',
        end_marker_line=f'[comment]: <> (✂✂✂ auto generated {marker} end ✂✂✂)',
    )


class ReadmeTestCase(BaseTestCase):
    def test_main_help(self):
        stdout = invoke_click(cli, '--help')
        self.assert_in_content(
            got=stdout,
            parts=(
                'Usage: ./dev-cli.py [OPTIONS] COMMAND [ARGS]...',
                ' local-test ',
                CLI_EPILOG,
            ),
        )
        assert_cli_help_in_readme(
            text_block=stdout,
            marker='help',
            readme_path=PACKAGE_ROOT / 'doc' / 'ADMIN.md',
        )
