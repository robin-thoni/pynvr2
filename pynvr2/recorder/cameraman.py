import os

from pynvr2.models.args.recorderargsmodel import RecorderArgsModel
from pynvr2.models.config.configmodel import ConfigModel, CameraModel


class CameraMan:
    def __init__(self, options: RecorderArgsModel, config: ConfigModel):
        self.options = options
        self.config = config

    def get_camera(self) -> CameraModel:
        for c in self.config.cameras:
            if c.name == self.options.camera:
                return c
        raise ValueError("Could not find camera '{}'".format(self.options.camera))

    def get_ffmpeg_command_line(self) -> str:
        camera = self.get_camera()

        cmd_line = "ffmpeg"
        cmd_line += " -nostdin"  # Disable interactive mode
        cmd_line += " -n"  # Do not overwrite files; Should not happen
        if camera.ffmpeg.input.options:
            cmd_line += " {}".format(camera.ffmpeg.input.options)  # Input options (rtsp options, etc)
        cmd_line += " -i {}".format(camera.input.url)  # Input URL
        cmd_line += " -f segment"  # Segment output in multiple files
        cmd_line += " -segment_time {}".format(camera.output.segment_time)  # Length of each segment file
        cmd_line += " -c copy"  # Copy w/o transcoding
        cmd_line += " -reset_timestamps 1"  # Helps keeping the seekbar working for second file and afterwards. https://superuser.com/questions/1065683/ffmpeg-increases-video-segments-length-when-used-with-segment-time-how-to-fix
        cmd_line += " -strftime 1"  # Use local time to name output segments
        # cmd_line += " -strftime_mkdir 1"  # Automatically create directory structure. Useful when using %variables outside of the file name (e.g. one directory per day)
        # cmd_line += " -hls_segment_filename {}.ts".format(camera.output.pattern)  # See above
        # cmd_line += " -movflags +frag_keyframe+separate_moof+omit_tfhd_offset+empty_moov"  # https://superuser.com/questions/1507460/can-i-transcode-a-file-with-ffmpeg-and-read-the-output-file-on-the-fly
        cmd_line += " {}".format(camera.output.pattern)  # Output segments path template
        return cmd_line

    def live(self):
        cmd_line = self.get_ffmpeg_command_line()
        os.execv('/bin/sh', ['sh', '-c', 'exec {}'.format(cmd_line)])
