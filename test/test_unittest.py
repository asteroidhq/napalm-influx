#!/usr/bin/env python
""" napalm-influx unit tests """

import mock
import unittest

from napalm_influx.napalm_influx import NapalmInflux
from napalm_influx.get_interface_counters import get_interface_counters


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
        self.assertIsNone(test.run('router', 'user', 'passwd', 'eos'))


class TestGetInterfaceCounters(unittest.TestCase):
    """
    testing napalm_influx.napalm_influx.get_interface_counters()
    """

    def test_get_interface_counters(self):

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

        # fake device
        class Device():
            def get_interfaces_counters(device):
                return napalm_data
        device = Device()
        # expected parsed result
        expected_interface_data = _remove_time(eval(open('test/data_influx_result.json').read()))
        # call get_interface_data
        actual_interface_data = _remove_time(get_interface_counters('router_name', device))
        self.assertEqual(_ordered(actual_interface_data), _ordered(expected_interface_data))
