from bx_py_utils.test_utils.unittest_utils import BaseDocTests

import pyinventory_ynh


class DocTests(BaseDocTests):
    def test_doctests(self):
        self.run_doctests(
            modules=(pyinventory_ynh,),
        )
