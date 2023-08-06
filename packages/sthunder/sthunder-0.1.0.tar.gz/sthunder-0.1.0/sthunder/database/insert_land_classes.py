import os
from sqlalchemy import create_engine, select, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker
from geoalchemy2 import Geometry
from shapely import wkt as swkt
from shapely import geometry as sgeom
import geopandas as gpd


Base = declarative_base()


class FlashDatetime(Base):
    __tablename__ = 'flash_datetime'
    id = Column(Integer, primary_key=True)
    datetime = Column(DateTime)
    flash = relationship("FlashSpatioTemporal")


class FlashCoordinate(Base):
    __tablename__ = 'flash_coordinate'
    id = Column(Integer, primary_key=True)
    geom = Column(Geometry('POINT'), unique=True)
    flash = relationship("FlashSpatioTemporal")
    land_class = relationship("LandClass")


class FlashSpatioTemporal(Base):
    __tablename__ = 'flash_spatio_temporal'
    id = Column(Integer, primary_key=True)
    total = Column(Integer)
    time = Column(Integer, ForeignKey('flash_datetime.id'))
    coords = Column(Integer, ForeignKey('flash_coordinate.id'))


class Country(Base):
    __tablename__ = 'country'
    id = Column(Integer, primary_key=True)
    name = Column(String(150))
    geom = Column(Geometry('GEOMETRY'))
    country_state = relationship("State")
    country_biome = relationship("Biome")
    country_watershed = relationship("Watershed")
    country_region = relationship("Region")



class State(Base):
    __tablename__ = 'state'
    id = Column(Integer, primary_key=True)
    name = Column(String(150))
    country = Column(Integer, ForeignKey('country.id'))
    uf = Column(String(5))
    geom = Column(Geometry('GEOMETRY'))
    state_city = relationship("City")


class City(Base):
    __tablename__ = 'city'
    id = Column(Integer, primary_key=True)
    name = Column(String(150))
    state = Column(Integer, ForeignKey('state.id'))
    uf = Column(String(5))
    population = Column(Integer)
    gpd = Column(Float)
    geom = Column(Geometry('GEOMETRY'))


class Biome(Base):
    __tablename__ = 'biome'
    id = Column(Integer, primary_key=True)
    name = Column(String(150))
    country = Column(Integer, ForeignKey('country.id'))
    geom = Column(Geometry('GEOMETRY'))


class Watershed(Base):
    __tablename__ = 'watershed'
    id = Column(Integer, primary_key=True)
    name = Column(String(150))
    country = Column(Integer, ForeignKey('country.id'))
    geom = Column(Geometry('GEOMETRY'))


class Region(Base):
    __tablename__ = 'region'
    id = Column(Integer, primary_key=True)
    name = Column(String(150))
    country = Column(Integer, ForeignKey('country.id'))
    geom = Column(Geometry('GEOMETRY'))


class LandClass(Base):
    __tablename__ = 'land_class'
    id = Column(Integer, primary_key=True)
    class_name = Column(String(150))
    collection = Column(String(50))
    date = Column(Integer())
    coords = Column(Integer, ForeignKey('flash_coordinate.id'))


if __name__ == "__main__":
    import os
    from wlts import WLTS

    SERVICE_URL = "https://brazildatacube.dpi.inpe.br/wlts/"
    SERVICE_TOKEN = os.environ.get('BDC_TOKEN')
    UNDEF = 'No-Data'
    service = WLTS(url=SERVICE_URL, access_token=SERVICE_TOKEN)

    DB_USER = os.environ['USER_POSTGRES']
    DB_PASS = os.environ['PASS_POSTGRES']
    DB_PORT = '5432'
    DB_HOST = '127.0.0.1'
    DB_NAME = 'sthunder'
    DB_URI = f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}'

    engine = create_engine(DB_URI, echo=True)

    Base.metadata.create_all(engine)
    # print(Base.metadata)

    DB_SESSION = sessionmaker(bind=engine)
    session = DB_SESSION()

    geom_country = session.query(Country.name, FlashCoordinate.geom.ST_AsText()).filter(Country.name == 'Brazil', func.ST_Contains(Country.geom, FlashCoordinate.geom)).all()


    # print(len(geom_country))
    start = 3000
    end = start + 500
    for i, row in enumerate(geom_country[start:end]):
        print("Exexc: ", i+1)

        coord = swkt.loads(row[1])
        coord_id = session.query(
            FlashCoordinate.id
        ).filter(FlashCoordinate.geom == row[1]).first()[0]

        tjs = service.tj(latitude=coord.y, longitude=coord.x,
                         collections='mapbiomas5_amazonia,mapbiomas5_cerrado,'
                                     'mapbiomas5_caatinga,'
                                     'mapbiomas5_mata_atlantica,'
                                     'mapbiomas5_pampa,mapbiomas5_pantanal')
        print(i+1, coord.x, coord.y, coord_id)
        for tj in tjs['result']['trajectory']:
            # print('\t', tj)
            temp = session.query(LandClass.class_name, LandClass.collection,
                                 LandClass.date, LandClass.date,
                                 LandClass.coords).filter(
                LandClass.class_name==tj['class'],
                LandClass.collection==tj['collection'],
                LandClass.date==int(tj['date']),
                LandClass.coords==coord_id).all()

            if len(temp) == 0:
                print("is empty, inserting...")
                cclass = LandClass(class_name=tj['class'],
                                   collection=tj['collection'],
                                   date=int(tj['date']), coords=coord_id)
                session.add(cclass)
                session.commit()
            else:
                print("not is empty, skipping...")
    session.close()
