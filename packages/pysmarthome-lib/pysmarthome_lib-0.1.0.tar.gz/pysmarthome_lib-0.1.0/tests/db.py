from pysmarthome.db import s3db
from pysmarthome import config
import json
import os

db = s3db(**config['s3db'], enc='json')
configs = db.collections['api_configs']
print(configs.documents)

# dirname = os.path.abspath(os.path.dirname(__file__))
# devices_states_file = os.path.join(dirname, '..', 'data', 'devices_states.json')
# 
# with open(devices_states_file) as f:
#     states = json.load(f)
# 
# devices_states.documents = states
# 
# devices_states.update('67b0cbe0-9ac3-4265-8a79-90c696f5de5e', state={'power': 'on'})
#devices_states.load_documents()
#print(devices_states.documents)
