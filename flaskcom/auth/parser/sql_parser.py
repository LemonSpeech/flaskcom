# from flaskcom.auth import AbstractDatabaseType
from flaskcom.auth.parser.utils import convert_datatype, convert_value

class SQLParser(object):

    """This class is responsible to parse the SQL statements from a given class"""

    def __init__(self):
        """TODO: to be defined. """
        
    def __create_sql_table_statement_line(self, key, value, is_key=False):
        """This function is used to create a single line for creating
        the table. It converts the datatypes but also includes the generation
        of keys and foreign keys

        Args:
            key (TODO): TODO
            value (TODO): TODO

        Returns: TODO

        """
        if is_key:
            string = "{} {} not null primary key".format(key, convert_datatype(value))
        else:
            string = "{} {}".format(key, convert_datatype(value))
        return string

    def create_sql_table_statement(self, cls):
        """TODO: Docstring for create_sql_statement.

        Args:
            class (TODO): TODO

        Returns: TODO

        """

        from itertools import chain

        ids = cls.get_keys()
        args = { key: value for key, value in chain(cls.get_passwords().items(),
                                                    cls.get_positional_arguments().items())}

        sql_statement = """
        CREATE TABLE {} (
        {}
        )
        """
        stringify_ids = [self.__create_sql_table_statement_line(key, value, is_key=True) for key, value in ids.items()]
        stringify_args = [self.__create_sql_table_statement_line(key, value) for key, value in args.items()]

        stringified_content = stringify_ids + stringify_args
        stringified_content = ",\n".join(stringified_content)

        sql_statement = sql_statement.format(cls.__tablename__, stringified_content)
        print(sql_statement)
        return sql_statement
    
    def create_sql_insert_statement(self, obj):
        """TODO: Docstring for create_sql_create_object_statement.

        Args:
            cls (TODO): TODO

        Returns: TODO

        """

        cls = obj.__class__
        sql_statement = """ INSERT INTO {} ({})
        VALUES ({}) """
        args = cls.get_unified_dict()

        keys = args.keys()
        values = [convert_value(getattr(obj, key)) for key in keys]

        stringified_keys = ", ".join(keys)
        stringified_values = ", ".join(values)

        sql_statement = sql_statement.format(cls.__tablename__,
                                             stringified_keys,
                                             stringified_values)
        return sql_statement

    def create_select_statement(self, object):
        """TODO: Docstring for create_select_statement.

        Args:
            cls (TODO): TODO

        Returns: TODO

        """

        cls = object.__class__
        ids = cls.get_keys().keys()
        ids += cls.get_passwords().keys()
        id_value_dict = {id : getattr(object, id) for id in ids}

        get_value_statement = cls.get_unified_dict().keys()
        get_value_statement = ", ".join(get_value_statement)

        # We create a list and join it to a statement
        where_statement = ["{} = {}".format(key, convert_value(value)) for key, value in id_value_dict.items()]
        where_statement = " AND ".join(where_statement)

        sql_statement = """Select {1} from {0}
        WHERE {2}"""
        sql_statement = sql_statement.format(cls.__tablename__, get_value_statement, where_statement)
        return sql_statement

    def show_all_statement(self, cls):
        """TODO: Docstring for show_all_statement.
        Returns: TODO

        """
        get_value_statement = cls.get_unified_dict().keys()
        get_value_statement = ", ".join(get_value_statement)
        sql_statement = """Select {1} from {0}"""
        sql_statement = sql_statement.format(cls.__tablename__, get_value_statement)
        print(sql_statement)
        return sql_statement
