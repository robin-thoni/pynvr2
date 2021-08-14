import datetime

from pynvr2.janitor.mopdata import RecordSegmentData
from pynvr2.janitor.policies.abstractpolicy import AbstractPolicy, PolicyResult, register_policy
from pynvr2.models.config.janitorpolicies.durationmax import DurationMaxConfigModel


@register_policy("duration_min")
class DurationMinPolicy(AbstractPolicy):

    def apply_policy(self, record_segment_data: RecordSegmentData, policy: DurationMaxConfigModel, **kwargs) -> PolicyResult:
        if self._current_time - record_segment_data.record_segment.start_date <= datetime.timedelta(minutes=policy.value):
            return PolicyResult.PRESERVE
        return PolicyResult.IGNORE
