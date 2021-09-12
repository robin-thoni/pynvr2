import datetime
from unittest import mock

from pynvr2.janitor.container import Container


def test_basic():
    container = Container()

    record_segment_details_mock = mock.Mock()
    record_segment_details_mock.get_start_time = lambda path, camera: datetime.datetime.strptime(path, camera.output.pattern)
    record_segment_details_mock.get_duration.return_value = datetime.timedelta(minutes=10)
    record_segment_details_mock.get_end_time = lambda path, camera: record_segment_details_mock.get_start_time(path, camera) + record_segment_details_mock.get_duration(path, camera)
    container.record_segment_details.override(record_segment_details_mock)

    container._io_selector.from_dict({
        'io_selector': 'io_ro'
    })

    io_mock = mock.Mock()
    io_mock.glob.return_value = [
        '/tmp/pynvr-cam01-2021-08-08_22-01-02.mp4'
    ]
    container.io.override(io_mock)

    datetime_mock = mock.Mock()
    datetime_mock.current.return_value = datetime.datetime(2021, 9, 10, 22, 1, 2)
    container.datetime.override(datetime_mock)

    container.config(**{
        'cameras': [
            {
                'name': 'cam01',
                'input': {
                    'url': 'rtsp://...',
                },
                'output': {
                    'pattern': '/tmp/pynvr-cam01-%Y-%m-%d_%H-%M-%S.mp4',
                },
            },
        ],
        'janitor': {
            'policies': [
                {
                    'name': 'camera_duration_max',
                    'value': '30 days',
                    'cameras': ['*'],
                },
            ],
        },
    })

    container.mop().sweep()

    io_mock.glob.assert_called_with('/tmp/pynvr-cam01-*-*-*_*-*-*.mp4')
    io_mock.remove.assert_called_with('/tmp/pynvr-cam01-2021-08-08_22-01-02.mp4')
