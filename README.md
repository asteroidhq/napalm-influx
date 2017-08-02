# napalm-influx

Collects network device stats via NAPALM and stores them in Influxdb.
Because of NAPLAM this is a vendor neutral solution, able to poll data
from various devices. Influxdb data can be viewed with tools such as
Grafana, provisind and easy interface for network data.

Install
=========

* set up influx
* set up grafana
* install napalm-influx
* configure napalm-influx

Usage
======

napalm_influx -c [configfile]

Influx hints
============

You likely want this to be a gauge in your reporting and you can make one with somewhat ease using continuous queries.

```
CREATE CONTINUOUS QUERY cq_interface_gauge_5m ON asteroid BEGIN SELECT difference(first(value)) AS value INTO asteroid.autogen.rx_octets_5m FROM asteroid.autogen.rx_octets WHERE time > now() - 1w GROUP BY time(5m), device, interface, organisation, service_id, vlan END
CREATE CONTINUOUS QUERY cq_interface_gauge_5m_tx ON asteroid BEGIN SELECT difference(first(value)) AS value INTO asteroid.autogen.tx_octets_5m FROM asteroid.autogen.tx_octets WHERE time > now() - 1w GROUP BY time(5m), device, interface, organisation, service_id, vlan END
```
