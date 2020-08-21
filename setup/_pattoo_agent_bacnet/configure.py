"""Configure the bacnet agent."""
import os
from _pattoo_agent_bacnet import shared as _shared
from pattoo_shared.installation import configure, shared
from pattoo_shared import files


def install(pattoo_home):
    """Start configuration process.

    Args:
        None

    Returns:
        None

    """
    # Initialize key variables
    if os.environ.get('PATTOO_CONFIGDIR') is None:
        os.environ['PATTOO_CONFIGDIR'] = '{0}etc{0}pattoo'.format(os.sep)
    config_dir = os.environ.get('PATTOO_CONFIGDIR')

    bacnet_agent_dict = {
            'polling_interval': 300,
    }

    # Attempt to create configuration directory
    files.mkdir(config_dir)

    # Create the pattoo user and group
    if _shared.root_check() is True:
        # Create the pattoo user and group
        configure.create_user('pattoo', pattoo_home, '/bin/false', True)

        # Attempt to change the ownership of the config and home directories
        shared.chown(config_dir)
        shared.chown(pattoo_home)

    config_file = configure.pattoo_config(
                                        'pattoo_agent_bacnetipd',
                                        config_dir,
                                        bacnet_agent_dict)

    configure.check_config(config_file, bacnet_agent_dict)
