#!/usr/bin/env python
""" collect network device data via napalm and write it to influxdb """

import logging

from influxdb import InfluxDBClient
from napalm import get_network_driver

from .get_interfaces_counters import get_interfaces_counters
from .get_optics import get_optics


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
        self.influx = InfluxDBClient(host, port, user, passwd, db)

    def run(self, device_host, user, passwd, device_os, tags):
        """
        connect to provided device, fetch data and write to influx

        :param device_host: (str) device hostname
        :param user: (str) device user
        :param passwd: (str) device passwd
        :param os: (str) a supported napalm os
        :param tags: (dict) dict of tags as specified in config file
        """
        if tags is None:
            tags = {}

        print tags

        try:
            print "polling device: " + device_host
            # open device connection with napalm
            driver = get_network_driver(device_os)
            device = driver(device_host, user, passwd)
            device.open()

            # get interface counter data
            iface_counters = get_interfaces_counters(device_host, device, tags)
            print 'done polling device'
            print iface_counters

            # get optics data
            optics = get_optics(device_host, device, tags)
            print 'done polling device'
            print optics

            # write data to influx
            print 'writing data to influx'
            self.influx.write_points(iface_counters)
            # self.log.info('done polling device: %s', device_host)
            print 'done writing data to influx'
        except Exception as err:
            print err
