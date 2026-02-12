import datetime
import sqlalchemy
import sqlalchemy.orm as orm
from database import Base, engine


student_society = sqlalchemy.Table(
    'student_society',
    Base.metadata,
    sqlalchemy.Column('pupil_id', sqlalchemy.Integer, sqlalchemy.ForeignKey('pupil.pupil_id'), primary_key=True),
    sqlalchemy.Column('society_id', sqlalchemy.Integer, sqlalchemy.ForeignKey('society.society_id'), primary_key=True)
)


class House(Base):
    __tablename__ = 'house'
    house_id: orm.Mapped[int] = orm.mapped_column(primary_key=True, autoincrement=True, init=False)
    house_name: orm.Mapped[str] = orm.mapped_column()

    pupils: orm.Mapped[list['Pupil']] = orm.relationship(back_populates='house', init=False, default=[])

    def __repr__(self):
        return f"House(id={self.house_id}, name='{self.house_name}')"


class Pupil(Base):
    __tablename__ = 'pupil'
    pupil_id: orm.Mapped[int] = orm.mapped_column(primary_key=True, autoincrement=True, init=False)
    first_name: orm.Mapped[str] = orm.mapped_column()
    second_name: orm.Mapped[str] = orm.mapped_column()
    date_of_birth: orm.Mapped[datetime.date] = orm.mapped_column()
    house_id: orm.Mapped[int] = orm.mapped_column(sqlalchemy.ForeignKey('house.house_id'), init=False)

    house: orm.Mapped['House'] = orm.relationship(foreign_keys=[house_id], back_populates='pupils', init=False)
    societies: orm.Mapped[list['Society']] = orm.relationship(secondary=student_society, back_populates='pupils', default=[], init=False)

    def __repr__(self):
        return f"Pupil(id={self.pupil_id}, name='{self.first_name} {self.second_name}')"


class Society(Base):
    __tablename__ = 'society'
    society_id: orm.Mapped[int] = orm.mapped_column(primary_key=True, autoincrement=True, init=False)
    name: orm.Mapped[str] = orm.mapped_column()
    room: orm.Mapped[str] = orm.mapped_column()
    week: orm.Mapped[str] = orm.mapped_column()
    time: orm.Mapped[str] = orm.mapped_column()

    pupils: orm.Mapped[list['Pupil']] = orm.relationship(secondary=student_society, back_populates='societies', default=[], init=False)

    def __repr__(self):
        return f"Society(id={self.society_id}, name='{self.name}', room='{self.room}', week='{self.week}', time='{self.time}')"


def create_database():
    """Initialize the database by creating all tables."""
    Base.metadata.create_all(engine)
