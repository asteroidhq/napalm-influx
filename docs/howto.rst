Napalm-Influx Howto
======================

Install Napalm-Influx
-----------------------------------

sudo python setup.py install


Create Config File
-----------------------------------

Place a config file like below into /etc/napalm-influx/napalm-influx.conf::

    # provide details of your influx db setup
    [influx]

    host = localhost
    port = 8086
    user = root
    passwd = root
    db = asteroid

    # provide details to your routers
    [routers]

        [[lunix]]
        user = admin
        passwd = passwd
        router_os = eos
        # provide additional tags you want to add to each
        # influx metric on a per-interface basis
        tags = '''{'Ethernet1': {'customer': 'Cust Name',
                                 'cust_id': 23},
                   'Ethernet2': {'customer': 'Other Cust Name',
                                 'cust_id': 42}}'''

        [[stellix]]
        user = admin
        passwd = passwd
        router_os = eos
        # provide additional tags you want to add to each
        # influx metric on a per-interface basis
        tags = "{'Ethernet1': {'customer': 'Cust Name',
                               'cust_id': 23},
                 'Ethernet2': {'customer': 'Other Cust Name',
                               'cust_id': 42}}"

Create Cron Job
------------------------------------

Add a cron job similar to this, to poll your devices::

    * * * * *   root    /usr/local/bin/napalm-influx
