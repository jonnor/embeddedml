

import time
import requests

class BlynkClient():
    """
    Ref:
    https://docs.blynk.io/en/blynk.cloud/device-https-api/upload-set-of-data-with-timestamps-api

    """
    
    def __init__(self,
            token,
            hostname='blynk.cloud',
            protocol='https',
        ):

        self._telemetry_url = protocol + '://' + hostname + '/external/api/batch/update?token=' + token
  

    def post_telemetry(self, values : list[dict[str, float]]):
        """
        Send multiple telemetry values.
        The 'time' key should be in Unix milliseconds.
        """
        stream_values = {}

        # Blynk HTTP API currently cannot send multiple timestamped values on multiple streams
        # so we shuffle the data into being organized per-stream
        for datapoint in values:
            if 'time' in datapoint.keys():
                t = datapoint['time']
                for key, value in datapoint.items():
                    if key == 'time':
                        continue
                    if key not in stream_values.keys():
                        stream_values[key] = []
                    stream_values[key].append((t, value))
            else:
                print('WARNING: ignored datapoint without time')

        # NOTE: if no timestamps are provided (and there are multiple values)
        # then regular batch update would be better, since it could be done in 1 request
        # https://docs.blynk.io/en/blynk.cloud/device-https-api/update-multiple-datastreams-api
    
        for key, datapoints in stream_values.items():
            self.post_timestamped_values(key, datapoints)

    def post_timestamped_values(self, pin : str, values : list[tuple[int, float]]):
        """
        Post multiple values from different times, for 1 stream
        Each entry in values must be a tuple with (timestamp, value)
        """

        payload = values
        url = self._telemetry_url+f'&pin={pin}'
        r = requests.post(url, json=payload)
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

def main():
    # bc3ab311-4e92-11ef-b45a-8f71ad378839
    BLYNK_AUTH_TOKEN = 'Cxvp01Mvo2-A8er9mGRWLfHnPcTNvaTP'
    api = BlynkClient(token=BLYNK_AUTH_TOKEN)

    t = int(unix_time_seconds() * 1000)

    values = []
    for s in range(0, 60, 10):
        v = {'time': t-(s*1000), 'V1': 78.0+s}
        values.append(v)

    api.post_telemetry(values)
    print(values)
    print('Posted telemetry')

if __name__ == '__main__':
    main()


