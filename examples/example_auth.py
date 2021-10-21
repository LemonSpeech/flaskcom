from flaskcom.auth.tables import User, Admin
from flaskcom.auth.database_manager import DataBaseManager

if __name__ == "__main__":
    # remote_object = RemoteObject("acoustic model")
    # remote_object.load()

    # # User.initialize_table()
    # user = User("admin", "Hallo")
    # # user.create_entry()
    # print(user.show_all_entries())
    # Admin.initialize_table()
    database_manager = DataBaseManager("flaskcom")
    user = database_manager.get_user("admin", "password")
    print(user)
    user.create_user("test", "test")
