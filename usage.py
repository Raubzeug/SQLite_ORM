import sqlite3

from base import Base
from model import Model
from column import Column

"""usage example"""

class Person(Model):
    id = Column('INTEGER', pk=True)
    name = Column('TEXT')
    age = Column('INTEGER')


class Pets(Model):
    id = Column('INTEGER')
    name = Column('TEXT', req=True)
    breed = Column('TEXT')
    owner = Column('INTEGER', req=True)
    owner.foreignkey = Person.id


with Base('test.db') as con:
    Person.create_table(con)
    Pets.create_table(con)
    Person(con, id=1, name='Bob')
    Person(con, name='Joe', id=5, age=42)
    Person(con, name='Bill', id=2)
    Pets(con, name='Tusik', id=1, owner=1)
    Pets(con, name='Bruce', id=2, owner=5)
    Pets(con, name='Bruce', id=3, owner=4) #foreign key constraint error
    Person.delete(con, condition='id=4') #deleting failed because of foreign key constraint
    Person.update(con, 'age=56', 'id=2')
    print(Person.join(con, Pets))
    print(Pets.join(con, Person))
    print(Person.select_all(con))
    print(Pets.select_all(con))
    print(Person.select(con, columns=['id', 'name'], condition='id=5 and name=Joe'))
    Pets.drop_table(con) #Pets table should be deleted first because of foreign key constraint
    Person.drop_table(con)
