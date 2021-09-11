import argparse
import datetime
import sys

import yaml

from pynvr2.janitor.container import Container


def main():

    container = Container()
    # Force datetime to now() for the rest of the execution, for consistency across all policies
    container.datetime(value=datetime.datetime.now())  # TODO really? e.g. Can't be used to log reel time

    default_options = {
        'config_path': '/etc/pynvr2.yml',
    }

    parser = argparse.ArgumentParser(description='Py NVR - Janitor')
    parser.add_argument('-c', '--config', type=str, default=default_options['config_path'], help='Path to config file')
    parser.add_argument('-n', '--dry', action='store_true', help='Do not rotate files. Just log.')
    args = parser.parse_args(sys.argv[1:])

    container.options(**vars(args))
    container._io_selector.from_dict({
        'io_selector': 'io_ro' if container.options().dry else 'io_rw'
    })

    with open(container.options().config_path, 'r') as f:
        config_dict = yaml.load(f, Loader=yaml.FullLoader)
    container.config(**config_dict)

    container.mop().sweep()

    return 0


if __name__ == '__main__':
    sys.exit(main())
