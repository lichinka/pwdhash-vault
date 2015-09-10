import cherrypy
from cherrypy.test import helper

from pwdhash_vault.web import PwdHashServer
from pwdhash_vault.generator import PwdHashGenerator



class PwdHashServerTest (helper.CPWebCase):
    """
    Tests the web interface of the PwdHash generator.-
    """
    def _get_url (self, url, txt_list):
        """
        Tries to access 'url' and checks it contains all the elements of
        'txt_list'.-
        """
        self.getPage (url)
        self.assertStatus ('200 OK')
        self.assertHeader ('Content-Type', 'text/html;charset=utf-8')
        for t in txt_list:
            self.assertInBody (t)


    def setup_server ( ):
        #
        # instantiate the password generator used by the web app
        #
        passwd = "pepe"
        pwd_gen = PwdHashGenerator (passwd)
        #
        # start the web-app server
        #
        cherrypy.tree.mount (PwdHashServer (pwd_gen))
    #
    # this method creates the testing environment
    #
    setup_server = staticmethod (setup_server)


    def test_index (self):
        """
        Checks the index page is correctly served.-
        """
        self._get_url ('/',
                       ['PwdHash Vault', 'ABOUT'])


    def test_about (self):
        """
        Checks the 'About' page is correctly served.-
        """
        self._get_url ('/about',
                       ['theft-resistant', 'HOME'])


    def test_add (self):
        """
        Checks the 'Add' page is correctly served.-
        """
        self._get_url ('/add',
                       ['Site Address', 'Update'])


    def test_only_not_available_entries_are_displayed (self):
        from   tempfile import mkdtemp
        import pwdhash_vault

        tmp_vault = mkdtemp ( )
        pwdhash_vault.init_vault (tmp_vault)

        expected_entries = Key.select ( ).orderBy ('name')
        print (expected_entries)
        self._get_url ('/',
                       expected_entries)

    def test_pick_image (self):
        """
        Checks the 'Pick an image' page is correctly served.-
        """
        self._get_url ('/pick_image?query=some%20logo%20png',
                       ['Pick an image', '>>>>'])


