import sqlalchemy
import sqlalchemy.orm as orm


engine = sqlalchemy.create_engine('sqlite+pysqlite:///pupil_db.sqlite', echo=True)


class Base(orm.DeclarativeBase, orm.MappedAsDataclass):
    pass
