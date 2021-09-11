import datetime

from unittest import mock

import pytest

from pynvr2.janitor.container import Container
from pynvr2.janitor.mopdata import RecordSegmentData, CameraData
from pynvr2.janitor.policies.policyresult import PolicyResult
from pynvr2.models.config.configmodel import CameraModel
from pynvr2.models.config.janitorpolicies.durationmin import DurationMinConfigModel


def strptime(date: str):
    return datetime.datetime.strptime(date, '%Y-%m-%d_%H-%M-%S')


testdata = [
    (
        '60 minutes',  # policy_value
        '2021-08-15_11-15-00',  # current_date
        '2021-08-15_10-15-00',  # record_segment_date
        PolicyResult.PRESERVE,  # policy_result
    ),
    (
        '60 minutes',  # policy_value
        '2021-08-15_11-15-00',  # current_date
        '2021-08-15_10-14-59',  # record_segment_date
        PolicyResult.IGNORE,  # policy_result
    ),
    (
        '60 minutes',  # policy_value
        '2021-08-15_11-15-00',  # current_date
        '2021-08-15_10-14-00',  # record_segment_date
        PolicyResult.IGNORE,  # policy_result
    ),
    (
        '60 minutes',  # policy_value
        '2021-08-15_11-15-00',  # current_date
        '2021-08-15_10-16-00',  # record_segment_date
        PolicyResult.PRESERVE,  # policy_result
    ),
    (
        '60 minutes',  # policy_value
        '2021-08-15_11-15-00',  # current_date
        '2021-08-15_10-15-01',  # record_segment_date
        PolicyResult.PRESERVE,  # policy_result
    ),
]


@pytest.mark.parametrize("policy_value,current_date,record_segment_date,expected_policy_result", testdata)
def test(policy_value: int, current_date: str, record_segment_date: str, expected_policy_result: PolicyResult):
    container = Container()

    record_segment_details_mock = mock.Mock()
    record_segment_details_mock.get_start_time.return_value = strptime(record_segment_date)
    container.record_segment_details.override(record_segment_details_mock)

    container.datetime(value=strptime(current_date))

    policy_config = DurationMinConfigModel(**{
        'name': DurationMinConfigModel._NAME,
        'value': policy_value,
    })

    cameras_data = [CameraData(CameraModel(name='cam01', input={'url': 'rtsp://'}))]
    cameras_data[0].record_segments_data = [RecordSegmentData('')]
    assert cameras_data[0].record_segments_data[0].policy_result == PolicyResult.IGNORE

    policy = container.policies(policy_config.name)
    policy.apply_policy(policy_config, cameras_data)

    assert cameras_data[0].record_segments_data[0].policy_result == expected_policy_result
