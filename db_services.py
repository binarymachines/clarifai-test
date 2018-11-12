#!/usr/bin/env python


import os
from contextlib import contextmanager
import sqldbx 

from snap import snap
from snap import common

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy_utils import UUIDType
import uuid


class PostgreSQLServiceObject(object):
    def __init__(self, **kwargs):
        port = int(kwargs['port'])
        self.db = sqldbx.PostgreSQLDatabase(kwargs['host'],
                                            kwargs['database'],
                                            port)
        self.username = kwargs['username']
        self.password = kwargs['password']        
        self.schema = kwargs['schema']
        self.data_manager = None
        self.db.login(self.username, self.password)        
        self.data_manager = sqldbx.PersistenceManager(self.db)
        self.Base = automap_base()
        self.Base.prepare(self.db.engine, reflect=True)
        


    def get_connection(self):
        return self.db.engine.connect()


    @contextmanager
    def txn_scope(self):
        session = self.db.get_session()
        try:
            yield session
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()


class MySQLService(object):
    def __init__(self, **kwargs):
        self.host = kwargs['host']
        self.port = int(kwargs.get('port', 3306))
        self.username = kwargs['username']
        self.db_name = kwargs['database']
        self.db = sqldbx.MySQLDatabase(self.host, self.db_name, self.port)
        self.db.login(self.username, kwargs['password'])
        self._data_manager = sqldbx.PersistenceManager(self.db)
        self.Base = automap_base()
        self.Base.prepare(self.db.engine, reflect=True)


    def get_connection(self):
        return self.db.engine.connect()

    @contextmanager
    def txn_scope(self):
        session = self.db.get_session()
        try:
            yield session
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()
        
    @property
    def data_manager(self):
        return self._data_manager

    @property
    def database(self):
        return self.db


class MSSQLServiceObject(object):
    def __init__(self, **kwargs):
        kwreader = common.KeywordArgReader('host', 'username', 'database', 'password')
        kwreader.read(**kwargs)

        self.host = kwreader.get_value('host')
        self.port = int(kwreader.get_value('port') or 1433)
        self.username = kwreader.get_value('username')
        self.db_name = kwreader.get_value('database')
        self.password = kwreader.get_value('password')
        self.db = sqldbx.SQLServerDatabase(self.host, self.db_name, self.port)
        self.db.login(self.username, self.password)
        self._data_manager = sqldbx.PersistenceManager(self.db)


    @property
    def data_manager(self):
        return self._data_manager

    @property
    def database(self):
        return self.db


class RedshiftServiceObject():
    def __init__(self, **kwargs):
        self.host = kwargs['host']
        self.db_name = kwargs['db_name']
        self.port = kwargs['port']
        self.username = kwargs['username']
        self.schema = kwargs['schema']
        self.data_manager = None
        self.db = sqldbx.PostgreSQLDatabase(self.host, self.db_name, self.port)


    def login(self, password):
        self.db.login(self.username, password, self.schema)
        self.data_manager = sqldbx.PersistenceManager(self.db)


    def get_connection(self):
        return self.db.engine.connect()



