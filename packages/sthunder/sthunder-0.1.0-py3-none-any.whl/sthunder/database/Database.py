import sys; sys.path.insert(0, "/home/adriano/sthunder")
from sqlalchemy import create_engine, select, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.
import os
from sthunder.database import db_schema as dbs


class Database:
    def __init__(self, **kwargs):
        self._base = declarative_base()
        self._user = kwargs.get('username', os.environ['USER_POSTGRES'])
        self._pass = kwargs.get('password', os.environ['PASS_POSTGRES'])
        self._port = kwargs.get('port', '5432')
        self._host = kwargs.get('host', '127.0.0.1')
        self._name = kwargs.get('database', 'sthunder')
        self._uri = f'postgresql://{self._user}:{self._pass}@{self._host}/' \
                    f'{self._name}'
        self.session = sessionmaker(bind=create_engine(self._uri, echo=True))()


if __name__ == "__main__":
    db = Database()

    # qs = db.session.query(
    #     dbs.State.name, dbs.FlashCoordinate.geom.st_astext(), dbs.LandClass
    # ).filter(
    #     func.st_contains(
    #         dbs.State.geom, dbs.FlashCoordinate.geom
    #     ),
    #     dbs.State.name == 'Paraná'
    # ).all()

    qs = db.session.query(
        dbs.LandClass.id, dbs.FlashCoordinate.geom.st_astext(),
        dbs.LandClass.class_name
    ).join(
        dbs.FlashCoordinate, dbs.FlashCoordinate.id == dbs.LandClass.coords
    ).filter(dbs.LandClass.class_name != 'No-Data').all()

    for q in qs:
        print(q)

    db.session.close()

