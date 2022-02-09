import pytest
from lib.executor1 import Executor
import json


class aTestRun():

    data = json.load(open('casedata/data02.json'))
    @pytest.mark.parametrize("casedata", data)
    def atest_01(self, data):
        Executor().execute1(data)



