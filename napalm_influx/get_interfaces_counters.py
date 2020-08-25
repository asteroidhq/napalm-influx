#!/usr/bin/env python
""" fetch and parse interface counter data """

import datetime


def get_interfaces_counters(device_name, device, tags):
    """
    fetch and parse interface counters data

    :param config: (obj) confobj
    :param device_name: (str) device name string
    :param device: (obj) napalm device object
    :param tags: (dict) dict of tags as specified in config file
    :returns: list of dicts prepared for influx insert
    """

    # current timestamp
    time = str(datetime.datetime.now())

    # fetch interface data
    data = device.get_interfaces_counters()

    # {
    #     'Ethernet2': {
    #         'tx_multicast_packets': 699,
    #         'tx_discards': 0,
    #         'tx_octets': 88577,
    #         'tx_errors': 0,
    #         'rx_octets': 0,
    #         'tx_unicast_packets': 0,
    #         'rx_errors': 0,
    #         'tx_broadcast_packets': 0,
    #         'rx_multicast_packets': 0,
    #         'rx_broadcast_packets': 0,
    #         'rx_discards': 0,
    #         'rx_unicast_packets': 0
    #     }
    # }

    # influx result
    result = []

    # parse data
    for interface_name, interface_data in data.items():

        # create tags
        insert_tags = {
            "device": device_name,
            "interface": interface_name,
        }

        # add tags from config file if exist
        if interface_name in tags:
            insert_tags.update(tags[interface_name])

        # iterate though interface keys and values
        for key, value in interface_data.items():
            result.append(
                {
                    "measurement": key,
                    "tags": insert_tags,
                    "time": time,
                    "fields": {
                        "value": value
                    }
                }
            )

    return result
