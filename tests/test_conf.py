# -*- coding: utf-8 -*-
import unittest

import pwdhash_vault



class ConfigurationTest (unittest.TestCase):
    def test_default_should_be_kept_if_file_not_found (self):
        from copy import deepcopy

        default_conf                       = deepcopy (pwdhash_vault.PWDVAULT_CONFIG)
        pwdhash_vault.PWDVAULT_CONFIG_FILE = "no_configuration.conf"

        pwdhash_vault.load_configuration ( )

        for k in pwdhash_vault.PWDVAULT_CONFIG.keys ( ):
            self.assertEqual (default_conf[k],
                              pwdhash_vault.PWDVAULT_CONFIG[k])

