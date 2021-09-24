from unittest import mock

import pytest

from pynvr2.janitor.container import Container
from pynvr2.janitor.mopdata import RecordSegmentData, CameraData
from pynvr2.janitor.policies.policyresult import PolicyResult
from pynvr2.models.config.configmodel import CameraModel
from pynvr2.models.config.janitorpolicies.storageconfigmodel import StorageMaxConfigModel


testdata = [
    (
        '500 MB',  # policy_value
        [
            {
                'size': 400000000,  # 400 MB
                'policy_result': PolicyResult.IGNORE
            },
        ]
    ),
    (
        '500 MB',  # policy_value
        [
            {
                'size': 400000000,  # 400 MB
                'policy_result': PolicyResult.DELETE
            },
            {
                'size': 400000000,  # 400 MB
                'policy_result': PolicyResult.IGNORE
            },
        ]
    ),
    (
        '400 MB',  # policy_value
        [
            {
                'size': 400000000,  # 400 MB
                'policy_result': PolicyResult.DELETE
            },
            {
                'size': 400000000,  # 400 MB
                'policy_result': PolicyResult.DELETE
            },
        ]
    ),
    (
        '1 GB',  # policy_value
        [
            {
                'size': 400000000,  # 400 MB
                'policy_result': PolicyResult.DELETE
            },
            {
                'size': 400000000,  # 400 MB
                'policy_result': PolicyResult.DELETE
            },
            {
                'size': 400000000,  # 400 MB
                'policy_result': PolicyResult.IGNORE
            },
            {
                'size': 400000000,  # 400 MB
                'policy_result': PolicyResult.IGNORE
            },
        ]
    ),
]


@pytest.mark.parametrize("policy_value,files", testdata)
def test(policy_value: int, files: dict):
    container = Container()

    def get_size(path: str):
        return files[int(path)]['size']
    io_mock = mock.Mock()
    io_mock.size = get_size
    container.io.override(io_mock)

    policy_config = StorageMaxConfigModel(**{
        'name': StorageMaxConfigModel._NAME,
        'size': policy_value,
    })

    cameras_data = [CameraData(CameraModel(name='cam01', input={'url': 'rtsp://'}))]
    cameras_data[0].record_segments_data = [RecordSegmentData(str(i)) for i in range(len(files))]
    for segment in cameras_data[0].record_segments_data:
        assert segment.policy_result == PolicyResult.IGNORE

    policy = container.policies(policy_config.name)
    policy.apply_policy(policy_config, cameras_data)

    assert [s.policy_result for s in cameras_data[0].record_segments_data] == [file['policy_result'] for file in files]
