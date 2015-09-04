# -*- coding: utf-8 -*-
import os
import apsw

from sqlobject import *



class KeyDatabase (object):
    """
    Keeps track of the registered keys inside a PwdHash vault.-
    """
    #
    # the maximum number of entries this database will hold
    #
    MAX_ENTRIES_NUM = 128

    def __init__ (self, directory, db_name='pwdvault.db'):
        """
        Initializes the database, using 'cur_dir' as the base directory

        :param directory:  the full path to the containing directory;
        :param db_name:    the file name of the key database;
        """
        self.db_path = os.path.abspath ('%s/%s' % (directory,
                                                   db_name))


    def create (self):
        """
        Creates a new database with no entries, filled with random data not to
        leak any information when encrypted.-
        """
        import random
        import string
        import sqlite3

        #
        # create a new database
        #
        new_db = sqlite3.connect (self.db_path)
        new_db.close ( )

        #
        # create all the entries with random data
        #
        sys_rnd = random.SystemRandom ( )
        rnd_set = string.ascii_uppercase + string.digits
        self.connect (create=True)

        for i in range (KeyDatabase.MAX_ENTRIES_NUM):
            field_data = dict ( )
            for field in Key.sqlmeta.columns.values ( ):
                #
                # string fields contain random strings
                #
                if type (field) == col.SOStringCol:
                    field_data[field.name] = ''.join (sys_rnd.choice (rnd_set) for _ in range (field.length))
            #
            # create a new entry
            #
            key = Key (**field_data)


    def connect (self, create=False):
        """
        Connects to the key database, optionally creating all needed tables

        :param create: whether to create the database tables.-
        """
        conn_string              = 'sqlite:%s' % self.db_path
        connection               = connectionForURI (conn_string)
        sqlhub.processConnection = connection
        #
        # the table containing all keys
        #
        Key.createTable (ifNotExists=create)
        Key._connection.debug = False



class Key (SQLObject):
    """
    A key inside the PwdHash vault.-
    """
    #
    # using alternateID will automatically create a byName() method
    #
    name      = StringCol (length      = 256,
                           varchar     = False,
                           alternateID = True,
                           unique      = True)
    domain    = StringCol (length  = 512,
                           varchar = False)
    usr       = StringCol (length  = 128,
                           varchar = False)
    usr_field = StringCol (length  = 128,
                           varchar = False)
    pwd_field = StringCol (length  = 128,
                           varchar = False)
    image     = StringCol (length  = 512,
                           varchar = False)
    avail     = BoolCol   (default = True,
                           notNone = True)


    def _init (self, id, connection=None, selectResults=None):
        """
        Makes sure no more than KeyDatabase.MAX_ENTRIES_NUM keys are created.
        """
        SQLObject._init (self, id, connection, selectResults)
        rows = Key.select ( )
        if rows.count ( ) > KeyDatabase.MAX_ENTRIES_NUM:
            key = Key.get   (id)
            key.destroySelf ( )
            raise ValueError ("Cannot insert: maximum number of Keys reached")


    @classmethod
    def delete (cls, id, connection=None):
        """
        Deletes key with the given id.

        :param id: the id of the key to be deleted.-
        """
        key = cls.get (id, connection=connection)
        if not key.avail:
            key.avail = True
            key.sync ( )


    @classmethod
    def deleteBy (cls, connection=None, **kw):
        raise NotImplementedError ("This method is not available")


    @classmethod
    def deleteMany (cls, where=sqlbuilder.NoDefault, connection=None):
        raise NotImplementedError ("This method is not available")

