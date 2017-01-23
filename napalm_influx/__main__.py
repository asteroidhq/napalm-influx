#!/usr/bin/env python
""" napalm-influx entry point """

import sys
import logging
from configobj import ConfigObj

from .napalm_influx import NapalmInflux


def main():
    """
    main entry point
    """

    # load config file
    try:
        config = ConfigObj('/etc/napalm-influx/napalm-influx.conf')
    except IOError as err:
        print "Cannot open config file at: {0}".format(err)
        sys.exit(1)
    except Exception as err:
        print "Cannot load config file: {0}".format(err)
        sys.exit(1)

    # set up logging
    try:
        logging.basicConfig(filename='/var/log/napalm-influx.log',
                            level=logging.DEBUG)
    except Exception as err:
        print "Cannot init logging: {0}".format(err)
        sys.exit(1)

    # poll routers
    try:
        napalm_influx = NapalmInflux(host=config.get("influx", "host"),
                                     port=config.get("influx", "port"),
                                     user=config.get("influx", "user"),
                                     passwd=config.get("influx", "passwd"),
                                     db=config.get("influx", "db"))

        for router in config["routers"].keys():
            napalm_influx.run(device_host=router,
                              user=config.get("routers", router, "user"),
                              passwd=config.get("routers", router, "passwd"),
                              device_os=config.get("routers", router, "router_os"))
    except Exception as err:
        print "Cannot poll router: {0}".format(err)
        sys.exit(1)


if __name__ == "__main__":
    main()
