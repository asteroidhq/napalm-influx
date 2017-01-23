#!/usr/bin/env python
""" fetch and parse interface counter data """

import datetime


def get_interface_counters(device_name, device):
    """
    fetch and parse interface counters data

    :param device_name: (str) device name string
    :param device: (obj) napalm device object
    :returns: list of dicts prepared for influx insert
    """

    # current timestamp
    time = str(datetime.datetime.now())

    # fetch interface data
    data = device.get_interfaces_counters()

    # {
    #     u'Ethernet2': {
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
        tags = {
            "device": device_name,
            "interface": interface_name,
        }

        # iterate though interface keys and values
        for key, value in interface_data.items():
            result.append(
                {
                    "measurement": key,
                    "tags": tags,
                    "time": time,
                    "fields": {
                        "value": value
                    }
                }
            )

    return result
