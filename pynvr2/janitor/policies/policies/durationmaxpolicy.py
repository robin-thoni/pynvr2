import datetime

from pynvr2.janitor.mopdata import RecordSegmentData
from pynvr2.janitor.policies.abstractpolicy import AbstractPolicy, PolicyResult, register_policy
from pynvr2.models.config.janitorpolicies.durationmax import DurationMaxConfigModel


@register_policy("duration_max")
class DurationMaxPolicy(AbstractPolicy):

    def apply_policy(self, record_segment_data: RecordSegmentData, policy: DurationMaxConfigModel, **kwargs) -> PolicyResult:

        diff = self._current_time - record_segment_data.record_segment.start_date
        if diff >= datetime.timedelta(minutes=policy.value):
            return PolicyResult.DELETE
        return PolicyResult.IGNORE
