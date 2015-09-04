# -*- coding: utf-8 -*-

PWDVAULT_VERSION = "0.1.0"

#
# the configuration of this password vault
#
PWDVAULT_CONFIG = {
    "domain": "www.example.com",

    "cherrypy": {
        "global" {
            "server" {
                "socker_host" : '0.0.0.0',
                "socket_port" : 8080,
                "thread_pool" : 2
            }
        },
        "site" {
            "tools" {
                "encode.encoding" : "utf-8",
                "secureheaders.on" : "True",
                "staticdir.on"     : "True",
            }
        }
    }
}



def load_configuration (fname):
    """
    Loads the configuration of this password vault into PWDVAULT_CONFIG.

    :param fname:   full path to the JSON configuration file;
    :raise IOError: if there is an error reading the file in.-
    """
    with open (fname, 'r') as conf:
        PWDVAULT_CONFIG = json.load (conf)
