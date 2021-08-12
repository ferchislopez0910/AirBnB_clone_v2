#!/usr/bin/python3
"""database storage for hbnb clone"""
from models.base_model import BaseModel
from models.base_model import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
from os import getenv
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.review import Review
from models.amenity import Amenity



class DBStorage:
    """Class Storage"""
    __engine = None
    __session = None

    def __init__(self):
        """inicializacion"""
        HBNB_MYSQL_USER = getenv('HBNB_MYSQL_USER')
        HBNB_MYSQL_PWD = getenv('HBNB_MYSQL_PWD')
        HBNB_MYSQL_HOST = getenv('HBNB_MYSQL_HOST')
        HBNB_MYSQL_DB = getenv('HBNB_MYSQL_DB')
        HBNB_ENV = getenv('HBNB_ENV')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'
                                      .format(HBNB_MYSQL_USER,
                                              HBNB_MYSQL_PWD,
                                              HBNB_MYSQL_HOST,
                                              HBNB_MYSQL_DB),
                                      pool_pre_ping=True)
        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """auto"""
        if cls is None:
            O_query = self.__session.query(State).all()
            O_query.extend(self.__session.query(City).all())
            O_query.extend(self.__session.query(User).all())
            O_query.extend(self.__session.query(Place).all())
            O_query.extend(self.__session.query(Review).all())
            O_query.extend(self.__session.query(Amenity).all())
        else:
            if type(cls) == str:
                cls = eval(cls)
            O_query = self.__session.query(cls)

        mydict = {}
        for objt in O_query:
         key = "{}.{}".format(type(objt)._name, objt.id)
         mydict[key] = objt
         return mydict

    def new(self, obj):
        """Add the object datab session"""
        self.__session.add(obj)

    def save(self):
        """Commit the changes"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete from the current database session obj if not None"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """reloads data of the datab"""
        Base.metadata.create_all(self.__engine)
        Session = scoped_session(sessionmaker(bind=self.__engine,
                                              expire_on_commit=False))
        self.__session = Session()

    def close(self):
        """call remove() method on the private session attribute"""
        self.__session.close()
