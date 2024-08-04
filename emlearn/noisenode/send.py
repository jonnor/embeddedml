
import time
import requests

class ThingsBoard():
    """
    Ref:
    https://thingsboard.io/docs/reference/http-api/
    """
    
    def __init__(self,
            token,
            hostname='thingsboard.cloud',
            protocol='https',
        ):
        

        self._telemetry_url = protocol + '://' + hostname + '/api/v1/' + token + '/telemetry'
    
    def post_telemetry(self, values : list[dict]):
        """
        Send multiple telemetry values.
        The 'time' key should be in Unix milliseconds.
        """

        def encode_one(d):
            o = { 'values': {} }
            if 'time' in d:
                o['ts'] = d['time']
            for k, v in d.items():
                if k == 'time':
                    continue
                o['values'][k] = v
            return o

        payload = [ encode_one(v) for v in values ]


        r = requests.post(self._telemetry_url, json=payload)
        assert r.status_code == 200, (r.status_code, r.content)

def unix_time_seconds():
    timestamp = time.time()
    epoch_year = time.gmtime(0)[0]

    if epoch_year == 2020:
        # seconds between 2000 (MicroPython epoch) and 1970 (Unix epoch)
        epoch_difference = 946684800
        timestamp = timestamp + epoch_difference
    elif epoch_year == 1970:
        pass
    else:
        raise ValueError('Unknown epoch year')

    return float(timestamp)

# bc3ab311-4e92-11ef-b45a-8f71ad378839
ACCESS_TOKEN = '7AiV0dXRPWKrxrLcI4wO'
api = ThingsBoard(token=ACCESS_TOKEN)

t = int(unix_time_seconds() * 1000)

values = []
for s in range(0, 60, 10):
    v = {'time': t-(s*1000), 'db2': 78.0+s, 'hex': 'ABCEDFE123122312452231DFABCEDF'}
    values.append(v)

api.post_telemetry(values)
print(values)
print('Posted telemetry')

