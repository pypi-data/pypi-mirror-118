from pysmarthome.db import s3db
from pysmarthome import config
from pysmarthome.managers.devices import DevicesManager
import time
db = s3db(**config['s3db'], enc='json')
manager = DevicesManager(db)

time.sleep(3)
print('start triggering...')

y = manager.load_device('f25eb2e4-fec9-48a7-820f-620a36c894ce', 'yeelight')
y.trigger_action('off')

s = manager.load_device('052905c5-3b67-4961-9f3b-c2fbc7cc3c3b', 'sonoff')
s.trigger_action('off')

salt = manager.load_device('407e6a41-5ad2-4a8f-bc5e-c10a98f0b387', 'sonoff')
salt.trigger_action('off')

print(y.to_dict())
print(s.to_dict())
print(salt.to_dict())
