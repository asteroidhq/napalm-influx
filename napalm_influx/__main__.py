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

    print("starting poller")

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
        print("init napalm-influx")
        napalm_influx = NapalmInflux(host=config['influx'].get("host"),
                                     port=config['influx'].get("port"),
                                     user=config['influx'].get("user"),
                                     passwd=config['influx'].get("passwd"),
                                     db=config['influx'].get("db"))
        print("init napalm-influx done")

        print("poll routers")
        for router in config["routers"].keys():
            print("processing: " + router)
            napalm_influx.run(device_host=router,
                              user=config['routers'][router].get("user"),
                              passwd=config['routers'][router].get("passwd"),
                              device_os=config['routers'][router].get("router_os"),
                              tags=config['routers'][router].get("tags"))
            print("done processing: " + router)
    except Exception as err:
        print "Cannot poll router: {0}".format(err)
        sys.exit(1)

    print("poller finished")


if __name__ == "__main__":
    main()
