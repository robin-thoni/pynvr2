import argparse
import sys

import yaml

from pynvr2.models.args.recorderargsmodel import RecorderArgsModel
from pynvr2.models.config.configmodel import ConfigModel
from pynvr2.recorder.cameraman import CameraMan


def main():

    default_options = {
        'config_path': '/etc/pynvr2.yml',
    }

    parser = argparse.ArgumentParser(description='Py NVR - Recorder')
    parser.add_argument('-c', '--config', type=str, default=default_options['config_path'], help='Path to config file')
    parser.add_argument('camera', type=str, help='Camera to record')
    args = parser.parse_args(sys.argv[1:])

    options = RecorderArgsModel(**vars(args))

    with open(options.config_path, 'r') as f:
        config_dict = yaml.load(f, Loader=yaml.FullLoader)
    config = ConfigModel(**config_dict)

    camera_mam = CameraMan(options, config)
    camera_mam.live()

    return 0


if __name__ == '__main__':
    sys.exit(main())
