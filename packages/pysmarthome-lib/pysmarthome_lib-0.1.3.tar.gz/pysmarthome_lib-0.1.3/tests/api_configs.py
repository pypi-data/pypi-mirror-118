from pysmarthome.db import s3db
from pysmarthome.managers.devices import DevicesManager
import time

db = s3db(bucket_name='pysmarthome', encoder='json')

manager = DevicesManager(db)
manager.load_controllers()

tv = manager.load_device('67b0cbe0-9ac3-4265-8a79-90c696f5de5e', 'tv')
# floor_lamp = manager.load_device('9ade5102-5232-4a54-8cf3-9c77d12eb8a8', 'broadlink_rgb_lamp')
#ac = manager.load_device('1de3ed56-c6f2-4c08-a34e-9fe1bfe416cf', 'ac')
# y = manager.load_device('f25eb2e4-fec9-48a7-820f-620a36c894ce', 'yeelight')
# s = manager.load_device('052905c5-3b67-4961-9f3b-c2fbc7cc3c3b', 'sonoff')
# salt = manager.load_device('407e6a41-5ad2-4a8f-bc5e-c10a98f0b387', 'sonoff')
# table_a = manager.load_device('66a6144c-99f6-4d38-a398-a82c11ea7fb3', 'govee')
# table_b = manager.load_device('5ad63d22-e22c-4ccb-ab45-83a0eef8d5ad', 'govee')
# led_tv = manager.load_device('54704389-dcfe-4c73-82cc-4b707c21bf79', 'govee')
# monitors = manager.load_device('2e08bfa0-e9be-4da1-ac1e-33d5d3418d10', 'govee')

#print('start triggering...')
#q = 'off'
#
#t = 4
#print(f'wait for {t} seconds...')
#time.sleep(t)

# led_tv.trigger_action(q)
# table_a.trigger_action(q)
# table_b.trigger_action(q)
# monitors.trigger_action(q)
# y.trigger_action(q)
# salt.trigger_action(q)
# s.trigger_action(q)
# floor_lamp.trigger_action(q)
# tv.trigger_action(q)
#tv.model.state.update(state={'volume': 24})
tv.vol(13)
print(tv.state.to_dict())


#docs = db.collections['devices']._documents
#states = db.collections['devices_states']._documents
#print(docs, states)
#for d in docs:
#    if d in states:
#        print(docs[d]['name'], states[d]['state']['power'])
