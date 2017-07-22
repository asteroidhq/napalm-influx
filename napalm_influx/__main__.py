#!/usr/bin/env python
""" napalm-influx entry point """

import sys
import logging
import argparse
import os
from configobj import ConfigObj

from .napalm_influx import NapalmInflux


def main():
    """
    main entry point
    """

    print("starting poller")

    # load config file
    parser = argparse.ArgumentParser(description="Poll router data and import it into InfluxDB")
    parser.add_argument('-c', nargs=1, dest="configfile_location", help="Configuration file, default: ./napalm-influx.conf, then /etc/napalm-influx/napalm-influx.conf")
    parser.add_argument('-d', dest='debug_mode', action='store_true', help="Print additional debug info and full stack traces")
    args = vars(parser.parse_args())

    try:
        configfile_location = args['configfile_location'][0]
    except TypeError:
        if os.path.isfile("./napalm-influx.conf"):
            configfile_location = "./napalm-influx.conf"
        elif os.path.isfile("/etc/napalm-influx/napalm-influx.conf"):
            configfile_location = "/etc/napalm-influx/napalm-influx.conf"
        elif os.path.isfile("/etc/napalm-influx.conf"):
            configfile_location = "/etc/napalm-influx.conf"
        else:
            print "Configuration file not found, specify with -c"
            sys.exit(1)
    print "Configuration file: " + str(configfile_location)

    try:
        config = ConfigObj(configfile_location)
    except IOError as err:
        print "Cannot open config file at: {0}".format(err)
        sys.exit(1)
    except Exception as err:
        print "Cannot load config file: {0}".format(err)
        sys.exit(1)

    if args['debug_mode']:
        print "Debug mode engaged"

    # set up logging
    try:
        logging.basicConfig(filename='/var/log/napalm-influx.log',
                            level=logging.DEBUG)
    except Exception as err:
        print "Cannot init logging: {0}".format(err)
        sys.exit(1)

    # establish link to Influx.
    try:
        print("init napalm-influx")
        napalm_influx = NapalmInflux(host=config['influx'].get("host"),
                                     port=config['influx'].get("port"),
                                     user=config['influx'].get("user"),
                                     passwd=config['influx'].get("passwd"),
                                     db=config['influx'].get("db"))
        print("init napalm-influx done")
    except Exception as err:
        print "Cannot link to InfluxDB.".format(err)
        sys.exit(1)

    # poll routers
    try:
        print("poll routers")
        if args['debug_mode']:
            print "Routers to poll: " + str(config["routers"].keys())
        for router in config["routers"].keys():
            print("processing: " + router)
            napalm_influx.run(device_host=router,
                              user=config['routers'][router].get("user"),
                              passwd=config['routers'][router].get("passwd"),
                              device_os=config['routers'][router].get("router_os"),
                              tags=config['routers'][router].get("tags"))
            print("done processing: " + router)
    except Exception as err:
        print "Error polling or storing " + str(router) +  ": {0}".format(err)
        if args['debug_mode']:
            raise
        sys.exit(1)

    print("poller finished")


if __name__ == "__main__":
    main()
