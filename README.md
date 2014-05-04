![](http://openbazaar.org/logo_small.png)

OpenBazaar is a decentralized marketplace proof of concept. It is based off of the POC code by the darkmarket team and protected by the GPL.


This project is alpha and all feedback is welcome at: http://www.reddit.com/r/Bitcoin/comments/23y80c
 
Official site: http://openbazaar.org (currently a placeholder)

## Features (Notional)
- Full market editor for management of items catalog
- Order management system
- Escrow-based transactions
- Arbiter management
- Private messaging
- Identity/Reputation system

##Quick Start

These instructions download a VirtualBox image (Ubuntu Trusty) and use Vagrant to configure an OpenBazaar node inside the virtual environment. When the node is running, you can navigate to http://localhost:8888 on your local machine to access the client. This setup should take less than 10GB and about an hour. These instructions should include all necessary code for starting OpenBazaar.

1. This example is built on an Ubuntu Trusty host. Doesn't work from inside a virtual machine. 

    `sudo apt-get update`

    `sudo apt-get install virtualbox git vagrant`

2. clone openbazaar:

    `git clone https://github.com/OpenBazaar/OpenBazaar.git`

    `cd OpenBazaar`
    
3. Set up vagrant: (this will take a while!)

    `vagrant up`

4. Log into the vagrant instance:

    `vagrant ssh`

5. Start the OpenBazaar node:

    `cd /vagrant && ./run_dev.sh`

6. Now return to your host and open firefox to:

    `http://127.0.0.1:8888`


## Dependencies

**NOTE:** These dependencies are for reference, they do not need to be manually installed if the Quick Start guide is used.

- https://github.com/warner/python-ecdsa
- https://github.com/darkwallet/python-obelisk
- MongoDB

`pip install pyzmq`
`pip install tornado`
`pip install pyelliptic`
`pip install pymongo`

1. Install python-obelisk
2. git clone https://github.com/darkwallet/python-obelisk
3. python setup.py install


### MongoDB

OpenBazaar now uses MongoDB as the backend for storing persistent data. At the moment only orders are being tracked there, but this will be fleshed out ongoing. You will need to set up a MongoDB instance on your machine outside of this software and create a database called 'openbazaar'. There is no authentication or encryption configured, but I will be adding in support for this soon.

- Install MongoDB with OpenSSL
- Start MongoDB 
- Create database named openbazaar

From command line:
`mongo`
`use openbazaar`


### OSX Users

For OSX there is a CLANG error when installing pyzmq but you can use the following command to ignore warnings:

`sudo ARCHFLAGS=-Wno-error=unused-command-line-argument-hard-error-in-future easy_install pyzmq`

### Issues with ./run_dev.sh
If you're getting errors saying `ZMQError: Can't assign requested address` then you probably need to bring up some loopback adapters for those 
IPs higher than 127.0.0.1.

sudo ifconfig lo0 alias 127.0.0.2 up
sudo ifconfig lo0 alias 127.0.0.3 up
sudo ifconfig lo0 alias 127.0.0.4 up

## Identity Server

To get the identity server running for querying nicknames in the UI you need to start the identity server. From the base directory of the software run the following:

`python identy/identity.py`


## Screenshot

This screen shot looks horrible and is just a placeholder ATM. Designers wanted. Apply to brian@openbazaar.org if you're interested in helping out.

![Screen 1](http://i.imgur.com/zUKFXyt.png)
![Screen 2](http://i.imgur.com/6SUrsw7.png)
=======


