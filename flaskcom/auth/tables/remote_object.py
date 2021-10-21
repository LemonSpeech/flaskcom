from __future__ import print_function
from flaskcom.auth.tables import AbstractDatabaseType
import sqlite3 as sqll

class RemoteObject(AbstractDatabaseType):

    """Docstring for RemoteObject. """

    __tablename__ = "RemoteObject"

    def __init__(self, name):
        """TODO: to be defined. 
        """
        super(RemoteObject, self).__init__()
        self.name = name
        
    @classmethod
    def get_positional_arguments(cls):
        """TODO: Docstring for get_data.
        Returns: TODO

        """
        positional_arguments = {
            "name" : unicode,
        }
        return positional_arguments

    @classmethod
    def get_keys(cls):
        """TODO: Docstring for get_keys.
        Returns: TODO

        """
        return {"name" : unicode}
