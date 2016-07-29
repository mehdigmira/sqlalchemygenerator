# sqlalchemygenerator

A small script that helps me build up quickly small SQlAlchemy test cases.
For example: 
python table_builder.py student->school->city->country student->sport will generate:
```python
from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, func, Table, create_engine
from sqlalchemy.orm import relationship, backref, sessionmaker, joinedload, contains_eager
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
engine = create_engine('sqlite://', echo=True)
    
class City(Base):
    __tablename__ = 'city'
    id = Column(Integer, primary_key=True)
    name = Column(String)

    country_id = Column(Integer, ForeignKey('country.id'))
    country = relationship('Country', backref='citys')
            

        
class School(Base):
    __tablename__ = 'school'
    id = Column(Integer, primary_key=True)
    name = Column(String)

    city_id = Column(Integer, ForeignKey('city.id'))
    city = relationship('City', backref='schools')
            

        
class Sport(Base):
    __tablename__ = 'sport'
    id = Column(Integer, primary_key=True)
    name = Column(String)


        
class Student(Base):
    __tablename__ = 'student'
    id = Column(Integer, primary_key=True)
    name = Column(String)

    school_id = Column(Integer, ForeignKey('school.id'))
    school = relationship('School', backref='students')
            
    sport_id = Column(Integer, ForeignKey('sport.id'))
    sport = relationship('Sport', backref='students')
            

        
class Country(Base):
    __tablename__ = 'country'
    id = Column(Integer, primary_key=True)
    name = Column(String)


        
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)
Session = sessionmaker(engine)
session = Session()
```
