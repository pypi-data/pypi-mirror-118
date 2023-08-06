from paretos.database.sqlite_database import SQLiteDatabase


class DatabaseFactory:
    """
    This class creates a new instance of the SQLite database connection.

    Within this dashboard API it is necessary to do this for every request.
    Each request might be handled in a separate thread.
    SQLite objects produce errors if they are shared between threads.
    """

    def __init__(self, data_source_name: str):
        self.__dsn = data_source_name

    def get_connection(self) -> SQLiteDatabase:
        return SQLiteDatabase(data_source_name=self.__dsn)
