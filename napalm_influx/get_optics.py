#!/usr/bin/env python
""" fetch and parse optics data """

import datetime


def get_optics(device_name, device, tags):
    """
    fetch and parse optics data

    :param config: (obj) confobj
    :param device_name: (str) device name string
    :param device: (obj) napalm device object
    :param tags: (dict) dict of tags as specified in config file
    :returns: list of dicts prepared for influx insert
    """

    # current timestamp
    time = str(datetime.datetime.now())

    # fetch interface data
    data = device.get_optics()

    # {
    #     'et1': {
    #         'physical_channels': {
    #             'channel': [
    #                 {
    #                     'index': 0,
    #                     'state': {
    #                         'input_power': {
    #                             'instant': 0.0, 'avg': 0.0, 'min': 0.0, 'max': 0.0,
    #                         },
    #                         'output_power': {
    #                             'instant': 0.0, 'avg': 0.0, 'min': 0.0, 'max': 0.0,
    #                         },
    #                         'laser_bias_current': {
    #                             'instant': 0.0, 'avg': 0.0, 'min': 0.0, 'max': 0.0,
    #                         },
    #                     }
    #                 }
    #             ]
    #         }
    #     }
    # }

    # influx result
    result = []

    # parse data
    for interface_name, optics_data in data.iteritems():
        # create tags
        insert_tags = {
            "device": device_name,
            "interface": interface_name,
        }

        # add tags from config file if exist
        if interface_name in tags:
            insert_tags.update(tags[interface_name])

        # iterate though interface keys and values
        for channel in optics_data['physical_channels']['channel']:
            tags['channel'] = channel['index']

            for state_name, state_value in channel['state'].iteritems():
                key = state_name
                value = state_value['instant']
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
