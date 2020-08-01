#!/usr/bin/env python3
"""Classe to manage SNMP agent configurations."""

# Import project libraries
from pattoo_agent_bacnet.ip import PATTOO_AGENT_BACNETIPD
from pattoo_shared import configuration, files, log
from pattoo_shared.configuration import Config
from pattoo_shared.variables import IPTargetPollingPoints


class ConfigBACnetIP(Config):
    """Class gathers all configuration information."""

    def __init__(self):
        """Initialize the class.

        Args:
            None

        Returns:
            None

        """
        # Instantiate inheritance
        Config.__init__(self)

        # Get the configuration directory
        config_file = configuration.agent_config_filename(
            PATTOO_AGENT_BACNETIPD)
        self._agent_config = files.read_yaml_file(config_file)

    def agent_ip_address(self):
        """Get list polling target information in configuration file.

        Args:
            None

        Returns:
            result: IP address

        """
        # Initialize key variables
        result = []

        # Get configuration snippet
        key = 'agent_ip_address'
        result = self._agent_config.get(key)
        if result is None:
            log_message = '"{}" not found in configuration file'.format(key)
            log.log2die(60002, log_message)
        return result

    def target_polling_points(self):
        """Get list polling target information in configuration file.

        Args:
            group: Group name to filter results by

        Returns:
            result: List of IPTargetPollingPoints objects

        """
        # Initialize key variables
        result = []
        datapoint_key = 'points'

        # Get configuration snippet
        key = 'polling_groups'
        groups = self._agent_config.get(key)

        if groups is None:
            log_message = '''\
    "{}" parameter not found in configuration file. Will not poll.'''
            log.log2info(60003, log_message)
            return result

        # Create snmp objects
        for group in groups:
            # Ignore bad values
            if isinstance(group, dict) is False:
                continue

            # Process data
            if 'ip_targets' and datapoint_key in group:
                for ip_target in group['ip_targets']:
                    poll_targets = configuration.get_polling_points(
                        group[datapoint_key])
                    dpt = IPTargetPollingPoints(ip_target)
                    dpt.add(poll_targets)
                    if dpt.valid is True:
                        result.append(dpt)
        return result

    def polling_interval(self):
        """Get targets.

        Args:
            None

        Returns:
            result: result

        """
        # Get result
        key = 'polling_interval'
        result = self._agent_config.get(key, 300)
        result = abs(int(result))
        return result
