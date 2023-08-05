from pysmarthome.db import s3db
from pysmarthome.devices import Pc, Tv, GoveeLedStrip
from pysmarthome.devices import SonoffDevice

db = s3db(bucket_name='pysmarthome', enc='json')
# print(db.collections['devices'].documents)
# print('----------------')
# print(db.collections['devices_states'].documents)


#print(db.collections['devices_states'].documents)
#db.delete('cf18cd44-cba4-4a33-984d-7cd2122816ba', 'devices_states')
#pc = Pc.create(db, name='test-creation')

#Pc.load(db, id='62d4e379-8a96-4f89-b0d9-96d02f391a14')
# print('PC DICT: ', pc.to_dict())
# print('STATE DICT: ', pc.state.to_dict())
# 
# print('deleting.....')
# pc.delete()
# 
# db.collections['devices'].load_documents()
# db.collections['devices_states'].load_documents()
# 
# print(db.collections['devices'].documents)
# print('----------------')
# print(db.collections['devices_states'].documents)
