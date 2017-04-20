from sqlalchemy import create_engine,func
from sqlalchemy.orm import sessionmaker,aliased
from setup_db import Base, Shelter, Puppy
#from flask.ext.sqlalchemy import SQLAlchemy
from random import randint
import datetime
import random
from dateutil.relativedelta import relativedelta


engine = create_engine('sqlite:///shelter.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

question_1 = session.query(Puppy)\
                    .order_by(Puppy.name)\
                    .all()

print('Question 1')
for row in question_1:
    print(row.name)
print('='*100)
date_6month = datetime.datetime.now().date() - relativedelta(months = 6)
question_2 = session.query(Puppy)\
                    .filter(Puppy.date_of_birth > date_6month)\
                    .all()
print('Question 2')
for row in question_2:
    print(row.name,row.date_of_birth)
print('='*100)

print("Question 3")
question_3 =  session.query(Puppy)\
                     .order_by(-Puppy.weight)\
                     .all()
for row in question_3:
    print(row.name,row.weight)
print('='*100)
print("Question 4")
a_alias = aliased(Shelter)

try:
    question_4  = session.query(Shelter, func.count(Puppy.id)).join(Puppy).group_by(Shelter.id).all()
    for item in question_4:
        print item[0].id, item[0].name, item[1]
except Exception as e:
    print(e)
    session.close()

session.close()
