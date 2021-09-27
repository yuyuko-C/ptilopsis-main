from peewee import MySQLDatabase,Model

class Model_Fuc:

    @classmethod
    def get_database(cls) -> MySQLDatabase:
        return cls._meta.database

    @classmethod
    def instance(cls):
        db = cls.get_database()
        with db.atomic():
            db.create_tables([cls])

    @classmethod
    def drop(cls):
        db = cls.get_database()
        with db.atomic():
            db.drop_tables([cls])

    @classmethod
    def reinstance(cls):
        if cls.is_exist():
            cls.drop()
        cls.instance()

    @classmethod
    def is_exist(cls):
        db = cls.get_database()
        return db.table_exists(cls.__name__.lower())

    @classmethod
    def reset_auto_increment(cls):
        db = cls.get_database()
        table_name=cls.__name__.lower()
        db.execute_sql("alter table `{}` auto_increment=1;".format(table_name))

    @classmethod
    def reconnect(cls, method):
        db = cls.get_database()
        if db.is_closed():
            db.connect()

        def inner(cls, *args, **kargs):
            return method(cls, *args, **kargs)

        return inner


db = MySQLDatabase('ptilopsis', host='127.0.0.1', port=3306, user='root', password='Star')

class Base_Model(Model, Model_Fuc):
    class Meta:
        database = db



class Base_Model(Base_Model):

    @classmethod
    @Base_Model.reconnect
    def update(cls, __data=None, **update):
        return super().update(__data, **update)

    @classmethod
    @Base_Model.reconnect
    def select(cls, *fields):
        return super().select(*fields)

    @classmethod
    @Base_Model.reconnect
    def replace(cls, __data=None, **insert):
        return super().replace(__data, **insert)

    @classmethod
    @Base_Model.reconnect
    def create(cls, **query):
        return super().create(**query)
