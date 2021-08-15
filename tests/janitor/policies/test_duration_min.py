import datetime

from datetime import timedelta

import pytest

from pynvr2.janitor.mopdata import RecordSegmentData
from pynvr2.janitor.policies.policies import DurationMinPolicy
from pynvr2.janitor.policies.policyresult import PolicyResult
from pynvr2.models.config.janitorpolicies.durationmin import DurationMinConfigModel
from pynvr2.models.recordsegmentmodel import RecordSegmentModel


def strptime(date: str):
    return datetime.datetime.strptime(date, '%Y-%m-%d_%H-%M-%S')


testdata = [
    (
        60,  # policy_value, minutes
        '2021-08-15_11-15-00',  # current_date
        '2021-08-15_10-15-00',  # record_segment_date
        PolicyResult.PRESERVE,  # policy_result
    ),
    (
        60,  # policy_value, minutes
        '2021-08-15_11-15-00',  # current_date
        '2021-08-15_10-14-59',  # record_segment_date
        PolicyResult.IGNORE,  # policy_result
    ),
    (
        60,  # policy_value, minutes
        '2021-08-15_11-15-00',  # current_date
        '2021-08-15_10-14-00',  # record_segment_date
        PolicyResult.IGNORE,  # policy_result
    ),
    (
        60,  # policy_value, minutes
        '2021-08-15_11-15-00',  # current_date
        '2021-08-15_10-16-00',  # record_segment_date
        PolicyResult.PRESERVE,  # policy_result
    ),
    (
        60,  # policy_value, minutes
        '2021-08-15_11-15-00',  # current_date
        '2021-08-15_10-15-01',  # record_segment_date
        PolicyResult.PRESERVE,  # policy_result
    ),
]


@pytest.mark.parametrize("policy_value,current_date,record_segment_date,expected_policy_result", testdata)
def test(policy_value: int, current_date: str, record_segment_date: str, expected_policy_result: PolicyResult):

    policy_config = DurationMinConfigModel(**{
        'name': 'duration_min',
        'value': policy_value,
    })

    policy = DurationMinPolicy(
        current_time=strptime(current_date),
    )

    record_segment_data = RecordSegmentData(RecordSegmentModel(strptime(record_segment_date), timedelta(minutes=10)), '')

    policy_result = policy.apply_policy(record_segment_data, policy_config)

    assert policy_result == expected_policy_result
