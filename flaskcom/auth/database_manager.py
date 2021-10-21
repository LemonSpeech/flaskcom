from os.path import isfile
from flaskcom.auth.tables import User, Admin
from flaskcom.auth.parser import SQLParser
import sqlite3 as sqll

class DataBaseManager(object):

    """Docstring for DataBaseManager. """
    __instance = None

    def __new__(cls, file_path):
        if not cls.__instance:
            cls.__instance = super(DataBaseManager, cls).__new__(cls, file_path)
        return cls.__instance

    def __init__(self, file_path):
        """TODO: to be defined.

        Args:
            file_path (TODO): TODO
            password (TODO): TODO


        """
        self._file_path = file_path
        if not isfile(self._file_path):
            self.__init__db__()
        
    def __init__db__(self):
        """TODO: Docstring for __init__db__.
        Returns: TODO

        """

        # We create the tables
        parser = SQLParser()
        tables_to_create = [
            User,
            Admin
        ]

        con = sqll.connect(self._file_path)
        for table in tables_to_create:
            sql_statement = parser.create_sql_table_statement(table)
            con.execute(sql_statement)
            con.commit()

        # We create a dummy admin
        admin = Admin(self._file_path, "admin", "password")
        sql_statement = parser.create_sql_insert_statement(admin)
        con.execute(sql_statement)
        con.commit()

        con.close()

    def get_user(self, name,
                 password):
        """TODO: Docstring for get_user.

        Args:
            name (TODO): TODO
            password (TODO): TODO

        Returns: TODO

        """
        user = Admin(self._file_path, name, password)
        if user:
            return user

        user = User(self._file_path, name, password)
        if user:
            return user

        return None
