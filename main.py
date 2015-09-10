# -*- coding: utf-8 -*-
import sys
import logging
import pwdhash_vault



def create_generator ( ):
    """
    Returns an instantiated PwdHashGenerator object with the
    user's master password.-
    """
    import getpass
    from   pwdhash_vault.generator import PwdHashGenerator

    #
    # ask the user's master password in order to create a generator
    #
    password  = unicode (getpass.getpass (">>> Please enter your password <<<\n"),
                         'utf8')
    generator = PwdHashGenerator (password)
    del password
    return generator


def get_usage_message ( ):
    return """
Implements Stanford's PwdHash with console and web interfaces

Usage:
    %s [--vault=<DIR>] [--no-web]
    %s (-h | --help | --version)

Options:
    -h, --help        show this screen and exit
    -n, --no-web      starts in interactive mode
    -v, --vault=<DIR> uses the password vault at DIR [default: %s]
        --version     display version information and exit
    """ % (sys.argv[0], sys.argv[0], pwdhash_vault.PWDVAULT_DIR)



def main ( ):
    """
    PwdHash entry point.-
    """
    from os.path import isdir
    from docopt  import docopt

    #
    # check command-line parameters
    #
    args = docopt (get_usage_message ( ),
                   version = pwdhash_vault.PWDVAULT_VERSION)
    #
    # check exitence of the vault directory
    #
    if args['--vault']:
        pwdhash_vault.PWDVAULT_DIR = args['--vault']
    if not isdir (pwdhash_vault.PWDVAULT_DIR):
        logging.warning ("No vault found at '%s'" % pwdhash_vault.PWDVAULT_DIR)
        create = raw_input ("Do you want to create an empty one? (y/N)")
        if create == 'y':
            pwdhash_vault.init_vault (pwdhash_vault.PWDVAULT_DIR)
        else:
            sys.exit (1)
    #
    # read the configuration file in
    #
    pwdhash_vault.load_configuration ( )
    #
    # create a password generator
    #
    generator = create_generator ( )
    #
    # interactive mode?
    #
    if args['--no-web']:
        from pwdhash_vault import console

        console.go (generator)
    else:
        #
        # start the web interface in a separate process
        #
        from multiprocessing import Process
        from pwdhash_vault   import web
        from pwdhash_vault   import platform

        p = Process (target=web.go, args=(generator,))
        p.start ( )
        #
        # display the Vault's home page in a browser
        #
        server_cfg = pwdhash_vault.PWDVAULT_CONFIG['cherrypy']['global']['server']
        vault_home = 'http://%s:%s' % (server_cfg['socket_host'],
                                       server_cfg['socket_port'])
        platform.open_target (vault_home)
        #
        # the Vault's process
        #
        p.join ( )



if __name__ == '__main__':
    main ( )
