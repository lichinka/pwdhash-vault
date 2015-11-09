# -*- coding: utf-8 -*-
import unittest

import pwdhash_vault



class ConfigurationTest (unittest.TestCase):
    def test_default_should_be_kept_if_file_not_found (self):
        import os
        import tempfile
        from   copy     import deepcopy

        default_conf                           = deepcopy (pwdhash_vault.PWDVAULT_CONFIG)
        default_conf_file                      = pwdhash_vault.PWDVAULT_CONFIG_FILE
        fd, pwdhash_vault.PWDVAULT_CONFIG_FILE = tempfile.mkstemp (text=True)
        os.close (fd)

        pwdhash_vault.load_configuration ( )

        for k in pwdhash_vault.PWDVAULT_CONFIG.keys ( ):
            self.assertEqual (default_conf[k],
                              pwdhash_vault.PWDVAULT_CONFIG[k])
        #
        # restore the original values
        #
        pwdhash_vault.PWDVAULT_CONFIG_FILE = default_conf_file


    def test_empty_vault_is_correctly_initialized (self):
        import tempfile
        import pwdhash_vault

        #
        # an empty vault to test the configuration
        #
        non_existent_vault = tempfile.mkdtemp ( )
        pwdhash_vault.init_vault (non_existent_vault)
        self.assertEqual (pwdhash_vault.PWDVAULT_DIR,
                          non_existent_vault)


    def test_configuration_correctly_loaded (self):
        import json
        import pwdhash_vault

        #
        # an empty vault to test the configuration
        #
        self.test_empty_vault_is_correctly_initialized ( )
        #
        # a random configuration dictionary
        #
        random_config = {
            "domain"   : "testing_only",
            "cherrypy" : {
                "global" : {
                    "server" : {
                        "socket_host" : '172.17.42.1',
                        "socket_port" : 6666,
                        "thread_pool" : 12
                    }
                },
                "site"   : {
                    "tools" : {
                        "encode.encoding"  : "utf-8",
                        "secureheaders.on" : "False",
                        "staticdir.on"     : "False"
                    }
                }
            }
        }
        with open ('%s/%s' % (pwdhash_vault.PWDVAULT_DIR,
                              pwdhash_vault.PWDVAULT_CONFIG_FILE), 'w') as conf:
            json.dump (random_config,
                       conf,
                       indent=4)
        pwdhash_vault.load_configuration ( )
        for k in pwdhash_vault.PWDVAULT_CONFIG.keys ( ):
            self.assertEqual (random_config[k],
                              pwdhash_vault.PWDVAULT_CONFIG[k])

