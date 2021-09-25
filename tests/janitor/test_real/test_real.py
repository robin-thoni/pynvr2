import datetime
import glob
import os
import shutil

import pytest
import yaml

from pynvr2.janitor.container import Container

testdata = [
    (
        'test1',
        [
            'cam01-2021-09-25_15-40-40.mp4',
            'cam01-2021-09-25_15-41-40.mp4',
            'cam01-2021-09-25_15-42-40.mp4',
        ],
    ),
]


def setup_function(function):
    test = function.pytestmark[0].args[1][0][0]
    shutil.rmtree('/tmp/pynvr2-test_real-data/', ignore_errors=True)
    shutil.copytree('./tests/janitor/test_real/tests/{}/data/'.format(test), '/tmp/pynvr2-test_real-data', symlinks=True)


def teardown_function(function):
    shutil.rmtree('/tmp/pynvr2-test_real-data/', ignore_errors=True)


@pytest.mark.parametrize("test,remaining_files", testdata)
def test_real(test, remaining_files):
    container = Container()
    container.datetime(value=datetime.datetime(2021, 9, 25, 15, 43, 0))
    container.options(**{
        'config': './tests/janitor/test_real/tests/{}/pynvr2.yml'.format(test)
    })
    container._io_selector.from_dict({
        'io_selector': 'io_rw'
    })

    with open(container.options().config_path, 'r') as f:
        config_dict = yaml.load(f, Loader=yaml.FullLoader)
    container.config(**config_dict)

    container.mop().sweep()

    files = [os.path.basename(f)for f in glob.glob('/tmp/pynvr2-test_real-data/*.mp4')]

    assert sorted(files) == sorted(remaining_files)
