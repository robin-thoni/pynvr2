from pynvr2.janitor.mopdata import CameraData, RecordSegmentData
from pynvr2.janitor.policies.policies.cameraabstractpolicy import CameraAbstractPolicy
from pynvr2.janitor.policies.policiesstore import policies
from pynvr2.janitor.policies.policyresult import PolicyResult
from pynvr2.models.config.janitorpolicies.storageconfigmodel import StorageMaxConfigModel


@policies.register(StorageMaxConfigModel._NAME)
class StorageMaxPolicy(CameraAbstractPolicy):
    def get_record_segment_policy(self, config: StorageMaxConfigModel, camera_data: CameraData,
                                  record_segment_data: RecordSegmentData) -> PolicyResult:

        current_size = sum([self.container.io().size(r.file_path) for r in camera_data.record_segments_data if r.policy_result != PolicyResult.DELETE])
        config_value = self.container.unit_parser().parse_bytes(config.size)
        if current_size >= config_value:
            return PolicyResult.DELETE
        return PolicyResult.IGNORE
