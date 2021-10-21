from abc import ABCMeta, abstractmethod
import sqlite3 as sqll
from flaskcom.auth.parser import SQLParser

class AbstractDatabaseType(object):

    """Docstring for AbstractDatabaseType. """

    __metaclass__ = ABCMeta

    """
    Returns: TODO

        """

    def __init__(self, database_path):
        """TODO: Docstring for __init__.
        Returns: TODO

        """
        self.relationships = []
        self._database_path = database_path

    @classmethod
    def check_setattr_type(cls, arg, value):
        """This function aims to control if value have the same type that are needed for the
        database. If the type is incorrect an Exception is thrown

        Args:
            arg (string): the name of the attribute
            value : The actual value

        Returns: TODO

        """
        if arg in cls.get_positional_arguments().keys():
            value = cls.get_positional_arguments()[arg](value)

        elif arg in cls.get_passwords().keys():
            value = cls.get_passwords()[arg](value)

        elif arg in cls.get_keys().keys():
            value = cls.get_keys()[arg](value)
        return value

    def __setattr__(self, arg, value):
        """TODO: Docstring for __setattr__.

        Args:
            arg (TODO): TODO

        Returns: TODO

        """
        try:
            value = self.__class__.check_setattr_type(arg, value)
            super(AbstractDatabaseType, self).__setattr__(arg, value)
        except Exception as ex:
            # print(arg, value, type(value))
            raise ex

    @classmethod
    def get_unified_dict(cls):
        """TODO: Docstring for get_unified_dict.
        Returns: TODO

        """
        from itertools import chain
        result_dict = { key: value for key, value in chain(cls.get_keys().items(),
                                                           cls.get_passwords().items(),
                                                           cls.get_positional_arguments().items())}
        return result_dict

    @abstractmethod
    def get_keys(cls):
        """TODO: Docstring for get_keys.
        Returns: TODO

        """
        pass

    @classmethod
    def get_passwords(cls):
        """TODO: Docstring for get_passwords.
        Returns: TODO

        """
        return {}

    @abstractmethod
    def get_positional_arguments(cls):
        """This function has to be defined in classes that inherit.
        It is necessary to implement this as a classmethod

        Returns: a dictionary that maps the positional arguments to
        types.

        """
        pass

    @classmethod
    def show_all_entries(cls, database_path):
        """TODO: Docstring for show_all_entries.
        Returns: TODO

        """

        parser = SQLParser()
        statement = parser.show_all_statement(cls)
        con = sqll.connect(database_path)
        cursor = con.execute(statement)
        for entry in cursor.fetchall():
            print(entry)

    def load(self):
        """TODO: Docstring for create_from_db.

        Args:
            **ids (TODO): TODO

        Returns: TODO

        """

        parser = SQLParser()
        sql_statement = parser.create_select_statement(self)
        con = sqll.connect(self._database_path)
        print(sql_statement)
        cursor = con.execute(sql_statement)
        object = cursor.fetchall()

        # We look if there is only one element
        print(object)
        assert len(object) == 1, "To many returned results"
        object = object[0]

        # we write the values in in our instance
        for i, (key, value) in enumerate(self.__class__.get_unified_dict().items()):
            print(key, value, object[i])
            setattr(self, key, object[i])
        con.close()

    def create_entry(self):
        """TODO: Docstring for save.
        Returns: TODO

        """
        con = sqll.connect(self._database_path)
        parser = SQLParser()
        sql_statement = parser.create_sql_insert_statement(self)
        con.execute(sql_statement)
        con.commit()
        con.close()
        
    @classmethod
    def get_relationship_classes(cls):
        """TODO: Docstring for get_relationship_object.
        Returns: TODO

        """
        return []
