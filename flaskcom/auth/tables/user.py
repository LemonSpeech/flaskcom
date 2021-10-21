from flaskcom.auth.tables import AbstractDatabaseType
from flaskcom.auth.parser import SQLParser
import sqlite3 as sqll

class User(AbstractDatabaseType):

    """The UserBase simply represents a class that contains a password and a name.
    This base class is connected with Admin and User classes that are also connected with
    a service."""
    __tablename__ = "User"

    def __init__(self, database_path, name, password):
        """TODO: to be defined. """
        AbstractDatabaseType.__init__(self, database_path)
        self.name = name
        self.password = password
        self.is_admin = False

    @classmethod
    def get_positional_arguments(cls):
        """TODO: Docstring for get_positional_arguments.

        Args:
            class (TODO): TODO

        Returns: TODO

        """
        argument_dict =  {
        }
        return argument_dict
        
    @classmethod
    def get_keys(cls):
        """TODO: Docstring for get_keys.
        Returns: TODO

        """
        return_dict = {
            "name": unicode
        }        
        return return_dict

    @classmethod
    def get_passwords(cls):
        """TODO: Docstring for get_password.
        Returns: TODO

        """
        return_dict = {
            "password" : unicode
        }
        return return_dict

    def create_entry(self):
        """TODO: Docstring for create_entry.
        Returns: TODO

        """
        pass
    
class Admin(AbstractDatabaseType):

    """A AbstractDatabaseType can be admin of a flaskcom remote object. From a database standpoint, it represents
    a relationship class"""

    __tablename__ = "Admin"

    def __init__(self, database_path, name, password):
        """TODO: to be defined.

        Args:
            name (TODO): TODO
            password (TODO): TODO
            remote_object (TODO): TODO


        """
        AbstractDatabaseType.__init__(self, database_path)
        self.name = name
        self.password = password
        
    @classmethod
    def get_positional_arguments(cls):
        """TODO: Docstring for get_positional_arguments.

        Args:
            class (TODO): TODO

        Returns: TODO

        """
        argument_dict =  {}
        return argument_dict
        
    @classmethod
    def get_keys(cls):
        """TODO: Docstring for get_keys.
        Returns: TODO

        """
        return_dict = {
            "name": unicode
        }        
        return return_dict

    @classmethod
    def get_passwords(cls):
        """TODO: Docstring for get_password.
        Returns: TODO

        """
        return_dict = {
            "password" : unicode
        }
        return return_dict

    def create_user(self, name, password):
        """TODO: Docstring for create_user.

        Args:
            name (TODO): TODO
            password (TODO): TODO

        Returns: TODO

        """
        self.load()

        parser = SQLParser()
        new_user = User(self._database_path, name, password)
        con = sqll.connect(self._database_path)
        con.execute(parser.create_sql_insert_statement(new_user))
        con.commit()
