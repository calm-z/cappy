import pytest
from lib.executor1 import Executor
import json
import yaml
from util.log import Logger


def read_file():
    file = open("case.yaml", "r", encoding="utf-8")
    case_file = yaml.load(file, Loader=yaml.FullLoader)
    print(case_file)
    case_data = []
    case_name = []
    for key, value in case_file.items():
        data = json.load(open(value))
        for i in data:
            case_name.append(i["id"])
            case_data.append(i)
    return case_data, case_name


cases_data, cases_name = read_file()


@pytest.mark.parametrize("cases_data", cases_data, ids=cases_name)
def test_run(cases_data):
    result = Executor().execute1(cases_data)
    assert result == "用例执行成功"

if __name__ == '__main__':
    pytest.main()
