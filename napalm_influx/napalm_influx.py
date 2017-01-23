#!/usr/bin/env python
""" collect network device data via napalm and write it to influxdb """

import logging

from influxdb import InfluxDBClient
from napalm import get_network_driver

from .get_interface_counters import get_interface_counters


class NapalmInflux(object):
    """
    the NapalmInflux class implements the influx as well as device
    connection, it polls the device and writes the resulting data
    to the db
    """

    def __init__(self, host, port, user, passwd, db):
        """
        set up logger and influx connection

        :param host: influx hostname
        :param port: influx port
        :param user: influx user
        :param passwd: influx passwd
        :param db: influx db
        """

        self.log = logging.getLogger('NapalmInflux')
        # connect to influx
        self.client = InfluxDBClient(host, port, user, passwd, db)

    def run(self, device_host, user, passwd, device_os):
        """
        connect to provided device, fetch data and write to influx

        :param device_host: (str) device hostname
        :param user: (str) device user
        :param passwd: (str) device passwd
        :param os: (str) a supported napam os
        """
	
	try:
            #self.log.info('polling device: %s', device_host)
            print('polling device')
            # open device connection
            driver = get_network_driver(device_os)
            device = driver(device_host, user, passwd)
            device.open()
            # get interface counter data
            result = get_interface_counters(device_host, device)
            print('done polling device')
            print result

            # write data to influx
            print('writing data to influx')
            self.client.write_points(result)
            #self.log.info('done polling device: %s', device_host)
            print('done writing data to influx')
        except Exception as err:
            print err
