from pysmarthome.db import s3db
from pysmarthome.managers.devices import DevicesManager
import time

db = s3db(bucket_name='pysmarthome', enc='json')
manager = DevicesManager(db)

tv = manager.load_device('67b0cbe0-9ac3-4265-8a79-90c696f5de5e', 'tv')
manager.load_devices()


t = 4
print(f'wait for {t} seconds...')
time.sleep(t)

print('start triggering...')
manager.get_device(name='pc_lamp').trigger_action('off')
manager.get_device(name='lava_lamp').trigger_action('off')
manager.get_device(name='floor_lamp').trigger_action('off')
manager.get_device(name='led_table_a').trigger_action('off')
manager.get_device(name='led_table_b').trigger_action('off')
manager.get_device(name='led_tv').trigger_action('off')
manager.get_device(name='led_monitors').trigger_action('off')
manager.get_device(name='q6fn').trigger_action('off')
manager.get_device(name='vesla00').trigger_action('pause')
docs = db.collections['devices']._documents
states = db.collections['devices_states']._documents
print(docs, states)
for d in docs:
    if d in states:
        print(docs[d]['name'], states[d]['state'])

t = 10
print(f'shutting down in {t} seconds...')
manager.get_device(name='vesla00').trigger_action('off')

