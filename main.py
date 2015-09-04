# -*- coding: utf-8 -*-
import sys



def create_generator ( ):
    """
    Returns an instantiated PwdHashGenerator object with the
    user's master password.-
    """
    import getpass
    from pwdhash_vault.generator import PwdHashGenerator

    #
    # ask the user's master password in order to create a generator
    #
    password = unicode (getpass.getpass (">>> Please enter your password <<<\n"),
                        'utf8')
    generator = PwdHashGenerator (password)
    del password
    return generator


def get_usage_message ( ):
    return """
Implements Stanford's PwdHash with console and web interfaces

Usage:
    %s [--config=<FILE>] [--no-web]
    %s (-h | --help | --version)

Options:
    -c, --config=<FILE> reads configuration from FILE [default: $HOME/.pwdvault/config.json]
    -h, --help          show this screen and exit
    -n, --no-web        starts in interactive mode
        --version       display version information and exit
    """ % (sys.argv[0], sys.argv[0])



def main ( ):
    """
    PwdHash entry point.-
    """
    import pwdhash_vault
    from   docopt        import docopt

    #
    # check command-line parameters
    #
    args = docopt (get_usage_message ( ),
                   version = pwdhash_vault.PWDVAULT_VERSION)
    #
    # read the configuration file in
    #
    try:
        pwdhash_vault.load_configuration (args['--config'])

    exception IOError:
        sys.stderr.write ("Configuration file '%s' is not accessible" %
                          args['--config'])
        sys.exit (1)
    #
    # interactive mode?
    #
    if args['--no-web']:
        from pwdhash_vault import console

        generator = create_generator ( )
        console.go (generator)
    else:
        #
        # start the web interface in a separate process
        #
        from multiprocessing import Process
        from pwdhash_vault   import web
        from pwdhash_vault   import platform

        generator = create_generator ( )
        p = Process (target=web.go, args=(generator,))
        p.start ( )
        #
        # display the Vault's home page in a browser
        #
        vault_home = 'http://%s:%s' % (web.PwdHashServer._global_config['server.socket_host'],
                                       web.PwdHashServer._global_config['server.socket_port'])
        platform.open_target (vault_home)
        #
        # the Vault's process
        #
        p.join ( )



if __name__ == '__main__':
    main ( )
