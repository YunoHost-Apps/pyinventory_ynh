import shutil
import subprocess
from pathlib import Path


BASE_PATH = Path(__file__).parent.parent


def test_lint():
    assert Path(BASE_PATH, 'Makefile').is_file()
    make_bin = shutil.which('make')
    assert make_bin is not None
    subprocess.check_call([make_bin, 'lint'], cwd=BASE_PATH)
