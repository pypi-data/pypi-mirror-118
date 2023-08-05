from os import replace
from typing import Collection
from jennifer.api.proxy import Proxy
from jennifer.agent import jennifer_agent
import json

__hooking_module__ = 'pymongo'


def safe(l, idx, default=None):
    try:
        return l[idx]
    except IndexError:
        return default


class CollectionProxy(Proxy):
    def __init__(self, obj, host, port, name):
        Proxy.__init__(self, obj)
        self.set('collection', name)
        self.set('host', host)
        self.set('port', port)

    def with_options(self, *args, **kwargs):
        obj = self._origin.with_options(*args, **kwargs)
        return CollectionProxy(
            obj, self.host, self.port, self.collection,
        )

    def find(self, *args, **kwargs):
        transaction = jennifer_agent().current_transaction()
        parameter = None
        document = safe(args, 0)
        try:
            parameter = json.dumps(document)
        except:
            pass

        result = None
        if transaction is not None and parameter is not None:
            transaction.profiler.db_execute(
                self.host, self.port, self.collection + '.find(' + \
                    parameter + ')')
        try:
            result = self._origin.find(*args, **kwargs)
        except Exception as e:
            if transaction is not None and parameter is not None:
                transaction.profiler.sql_error(e)
                transaction.profiler.end()
            raise e

        if transaction is not None and parameter is not None:
            transaction.profiler.end()

        return result

    def find_one_and_replace(self, *args, **kwargs):
        transaction = jennifer_agent().current_transaction()
        parameter = None
        filter_ = safe(args, 0) or kwargs.get('filter')
        replacement = safe(args, 1) or kwargs.get('replacement')

        try:
            parameter = [json.dumps(filter_), json.dumps(replacement)]
        except:
            pass

        result = None
        if transaction is not None and parameter is not None:
            transaction.profiler.db_execute(
                self.host, self.port, self.collection + '.findOneAndReplace(' + \
                    parameter[0] + ', ' + parameter[1] + ')')
        try:
            result = self._origin.find(*args, **kwargs)
        except Exception as e:
            if transaction is not None and parameter is not None:
                transaction.profiler.sql_error(e)
                transaction.profiler.end()
            raise e

        if transaction is not None and parameter is not None:
            transaction.profiler.end()

        return result

    def insert_many(self, *args, **kwargs):
        transaction = jennifer_agent().current_transaction()
        parameter = None
        document = safe(args, 0) or kwargs.get('document')
        try:
            parameter = json.dumps(document)
        except:
            pass

        result = None
        if transaction is not None and parameter is not None:
            transaction.profiler.db_execute(
                self.host, self.port, self.collection + ".insert(" + \
                    parameter + ")")
        try:
            result = self._origin.insert_many(*args, **kwargs)
        except Exception as e:
            if transaction is not None and parameter is not None:
                transaction.profiler.sql_error(e)
                transaction.profiler.end()
            raise e

        if transaction is not None and parameter is not None:
            transaction.profiler.end()

        return result

    def update_many(self, *args, **kwargs):
        transaction = jennifer_agent().current_transaction()
        parameter = None
        document = safe(args, 0) or kwargs.get('document')
        try:
            parameter = json.dumps(document)
        except:
            pass

        result = None
        if transaction is not None and parameter is not None:
            transaction.profiler.db_execute(
                self.host, self.port, self.collection + ".update(" + \
                    parameter + ")")
        try:
            result = self._origin.update_many(*args, **kwargs)
        except Exception as e:
            if transaction is not None and parameter is not None:
                transaction.profiler.sql_error(e)
                transaction.profiler.end()
            raise e

        if transaction is not None and parameter is not None:
            transaction.profiler.end()

        return result

    def update_one(self, *args, **kwargs):
        transaction = jennifer_agent().current_transaction()
        parameter = None
        document = safe(args, 0) or kwargs.get('document')
        try:
            parameter = json.dumps(document)
        except:
            pass

        result = None
        if transaction is not None and parameter is not None:
            transaction.profiler.db_execute(
                self.host, self.port, self.collection + ".updateone(" + \
                    parameter + ")")
        try:
            result = self._origin.update_one(*args, **kwargs)
        except Exception as e:
            if transaction is not None and parameter is not None:
                transaction.profiler.sql_error(e)
                transaction.profiler.end()
            raise e

        if transaction is not None and parameter is not None:
            transaction.profiler.end()

        return result

    def insert_one(self, *args, **kwargs):
        transaction = jennifer_agent().current_transaction()
        parameter = None
        document = safe(args, 0) or kwargs.get('doc')
        try:
            parameter = json.dumps(document)
        except:
            pass

        result = None
        if transaction is not None and parameter is not None:
            transaction.profiler.db_execute(
                self.host, self.port, self.collection + ".insertOne(" + \
                    parameter + ")")
        try:
            result = self._origin.insert_one(*args, **kwargs)
        except Exception as e:
            if transaction is not None and parameter is not None:
                transaction.profiler.sql_error(e)
                transaction.profiler.end()
            raise e

        if transaction is not None and parameter is not None:
            transaction.profiler.end()

        return result


class DatabaseProxy(Proxy):
    def __init__(self, obj, host, port, name):
        Proxy.__init__(self, obj)
        self.set('db', name)
        origin_getitem = self._origin.__getitem__
        def getitem(name):
            collection = origin_getitem(name)
            return CollectionProxy(collection, host, port, self.db + '.' + name)

        self._origin.__getitem__ = getitem


def hook(pymongo):
    MongoClientOrigin = pymongo.MongoClient
    class MongoClientWrap(MongoClientOrigin):
        def __getitem__(self, name):
            database = MongoClientOrigin.__getitem__(self, name)
            host, port = self.address
            proxy = DatabaseProxy(database, host, port, name)
            return proxy
    pymongo.MongoClient = MongoClientWrap
