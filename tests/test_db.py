# -*- coding: utf-8 -*-
import unittest

from pwdhash_vault.db import Key, KeyDatabase



class KeyDatabaseTest (unittest.TestCase):
    def setUp (self):
        from os.path  import basename, dirname
        from tempfile import NamedTemporaryFile

        self.tmp_db = NamedTemporaryFile (suffix='.db')
        self.key_db = KeyDatabase (directory = dirname  (self.tmp_db.name),
                                   db_name   = basename (self.tmp_db.name))
        self.key_db.create ( )


    def test_initial_database_creation (self):
        with self.tmp_db.file:
            rows = Key.select ( )
            #
            # make sure all the entries are there
            #
            self.assertEqual (rows.count ( ),
                              KeyDatabase.MAX_ENTRIES_NUM)
            #
            # make sure the fields contain the right content
            #
            for r in rows:
                self.assertGreaterEqual (r.id, 0)
                self.assertEqual        (len (r.name.strip ( )),
                                         Key.sqlmeta.columns['name'].length)
                self.assertEqual        (len (r.domain.strip ( )),
                                         Key.sqlmeta.columns['domain'].length)
                self.assertEqual        (len (r.image.strip ( )),
                                         Key.sqlmeta.columns['image'].length)
                self.assertTrue         (r.avail)


    def test_delete_marks_entry_as_available (self):
        import random

        with self.tmp_db.file:
            for i in range (10):
                rnd_id = random.randint (1,
                                         KeyDatabase.MAX_ENTRIES_NUM)
                key    = Key.get (rnd_id)

                Key.delete (rnd_id)

                key = Key.get (rnd_id)
                self.assertTrue (key.avail)


    def test_deleteBy_should_not_be_accessible (self):
        with self.assertRaises (NotImplementedError):
            Key.deleteBy ( )


    def test_deleteMany_should_not_be_accessible (self):
        with self.assertRaises (NotImplementedError):
            Key.deleteMany ( )


    def test_cannot_insert_more_keys (self):
        with self.assertRaises (ValueError):
            key = Key (name   = "pepe",
                       domain = "pepe.me",
                       image  = None)
        rows = Key.select ( )
        self.assertEqual (rows.count ( ),
                          KeyDatabase.MAX_ENTRIES_NUM)

