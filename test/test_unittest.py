#!/usr/bin/env python
""" napalm-influx unit tests """

import mock
import unittest

from napalm_influx.napalm_influx import NapalmInflux
from napalm_influx.get_interfaces_counters import get_interfaces_counters
from napalm_influx.get_optics import get_optics


class TestNapalmInflux(unittest.TestCase):
    """
    testing napalm_influx.napalm_influx.NapalmInflux()
    """

    def test_init(self):
        self.assertIsInstance(NapalmInflux('host', 1234, 'user', 'passwd', 'db'), NapalmInflux)

    @mock.patch('napalm_influx.napalm_influx.get_network_driver')
    @mock.patch('napalm_influx.napalm_influx.InfluxDBClient')
    def test_run(self, mock_influx, mock_napalm):
        test = NapalmInflux('host', 1234, 'user', 'passwd', 'db')
        self.assertIsNone(test.run('router', 'user', 'passwd', 'eos', {}))


class TestGetInterfacesCounters(unittest.TestCase):
    """
    testing napalm_influx.napalm_influx.get_interfaces_counters()
    """

    def test_get_interfaces_counters(self):

        def _ordered(obj):
            if isinstance(obj, dict):
                return sorted((k, _ordered(v)) for k, v in obj.items())
            if isinstance(obj, list):
                return sorted(_ordered(x) for x in obj)
            else:
                return obj

        def _remove_time(obj):
            for item in obj:
                del item['time']
            return obj

        # show diff
        self.maxDiff = None

        # fake napalm data
        napalm_data = eval(open('test/data_napalm_get_interfaces_counters.json').read())

        # fake tags from config
        tags = {'Ethernet1': {'organisation': 'Cust Name',
                              'service_id': 23,
                              'vlan': 456},
                'Ethernet2': {'organisation': 'Other Cust Name',
                              'service_id': 42,
                              'vlan': 456}}

        # fake device
        class Device():
            def get_interfaces_counters(device):
                return napalm_data

        device = Device()
        # expected parsed result
        expected_interface_data = _remove_time(eval(open('test/data_result_get_interfaces_counters.json').read()))
        # call get_interface_data
        actual_interface_data = _remove_time(get_interfaces_counters('router_name', device, tags))
        self.assertEqual(_ordered(expected_interface_data), _ordered(actual_interface_data))


class TestGetOptics(unittest.TestCase):
    """
    testing napalm_influx.napalm_influx.get_optics()
    """

    def test_get_optics(self):

        def _ordered(obj):
            if isinstance(obj, dict):
                return sorted((k, _ordered(v)) for k, v in obj.items())
            if isinstance(obj, list):
                return sorted(_ordered(x) for x in obj)
            else:
                return obj

        def _remove_time(obj):
            for item in obj:
                del item['time']
            return obj

        # show diff
        self.maxDiff = None

        # fake napalm data
        napalm_data = eval(open('test/data_napalm_get_optics.json').read())

        # fake tags from config
        tags = {'Ethernet1': {'organisation': 'Cust Name',
                              'service_id': 23,
                              'vlan': 456},
                'Ethernet2': {'organisation': 'Other Cust Name',
                              'service_id': 42,
                              'vlan': 456}}
        # fake device
        class Device():
            def get_optics(device):
                return napalm_data

        device = Device()
        # expected parsed result
        expected_interface_data = _remove_time(eval(open('test/data_result_get_optics.json').read()))
        # call get_optics
        actual_interface_data = _remove_time(get_optics('router_name', device, tags))
        self.assertEqual(_ordered(expected_interface_data), _ordered(actual_interface_data))
