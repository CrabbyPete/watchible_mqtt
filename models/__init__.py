
from config import MONGODB
from pymongo     import ReadPreference
from mongoengine import connect

ok = connect(MONGODB['db'],
             host=MONGODB['uri'],
             read_preference=ReadPreference.PRIMARY)
pass