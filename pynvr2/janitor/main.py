import argparse
import sys

import yaml

from pynvr2.janitor.mop import Mop
from pynvr2.models.args.janitorargsmodel import JanitorArgsModel
from pynvr2.models.config.configmodel import ConfigModel


def main():

    default_options = {
        'config_path': '/etc/pynvr2.yml',
    }

    parser = argparse.ArgumentParser(description='Py NVR - Janitor')
    parser.add_argument('-c', '--config', type=str, default=default_options['config_path'], help='Path to config file')
    parser.add_argument('-n', '--dry', action='store_true', help='Do not rotate files. Just log.')
    args = parser.parse_args(sys.argv[1:])

    options = JanitorArgsModel(**vars(args))

    with open(options.config_path, 'r') as f:
        config_dict = yaml.load(f, Loader=yaml.FullLoader)
    config = ConfigModel(**config_dict)

    mop = Mop(options, config)
    mop.sweep()

    return 0


if __name__ == '__main__':
    sys.exit(main())
