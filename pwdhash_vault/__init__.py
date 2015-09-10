# -*- coding: utf-8 -*-
import os
import json
import logging



#
# default constant values
#
PWDVAULT_VERSION     = "0.1.0"
PWDVAULT_DB          = 'vault.db'
PWDVAULT_DIR         = '%s/%s' % (os.environ['HOME'],
                                  '.pwdvault')
PWDVAULT_CONFIG_FILE = "config.json"

#
# a default configuration dictionary
#
PWDVAULT_CONFIG = {
    "domain"   : "www.example.com",
    "cherrypy" : {
        "global" : {
            "server" : {
                "socket_host" : '0.0.0.0',
                "socket_port" : 8080,
                "thread_pool" : 2
            }
        },
        "site"   : {
            "tools" : {
                "encode.encoding"  : "utf-8",
                "secureheaders.on" : "True",
                "staticdir.on"     : "True",
            }
        }
    }
}


def load_configuration ( ):
    """
    Loads the configuration from PWDVAULT_CONFIG_FILE into PWDVAULT_CONFIG.-
    """
    try:
        with open ('%s/%s' % (PWDVAULT_DIR, PWDVAULT_CONFIG_FILE), 'r') as conf:
            PWDVAULT_CONFIG = json.load (conf)
    except IOError:
        logging.error ("Cannot read configuration from '%s'" % PWDVAULT_CONFIG_FILE)


def save_configuration ( ):
    """
    Saves PWDVAULT_CONFIG into PWDVAULT_CONFIG_FILE.

    :raise IOError: if the configuration could not be saved.-
    """
    with open ('%s/%s' % (PWDVAULT_DIR, PWDVAULT_CONFIG_FILE), 'w') as conf:
        json.dump (PWDVAULT_CONFIG,
                   conf,
                   indent=4)


def init_vault (directory):
    """
    Initializes an empty password vault into the given dir.

    :param directory: the directory into which the vault will be created;
    :raise IOError:   in case the vault could not be created.-
    """
    from os               import mkdir
    from pwdhash_vault.db import KeyDatabase

    logging.info ("Initializing empty vault into '%s' ..." % directory)

    mkdir (directory)
    db = KeyDatabase   (directory,
                        PWDVAULT_DB)
    db.create          ( )
    save_configuration ('%s/%s' % (directory,
                                   PWDVAULT_CONFIG_FILE))
    PWDVAULT_DIR = directory

