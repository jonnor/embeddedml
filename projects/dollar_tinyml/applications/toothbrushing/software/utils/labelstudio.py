"""
Utilities for working with Label Studio data
"""


import re
import os
import json

import pandas


def extract_filename(url):

    base = os.path.basename(url)

    # label studio adds a ID- on import
    filename = re.sub(r'(\w+)-', '', base, count=1)

    return filename

def read_timeseries_labels(path):
    """
    Read .CSV export with TimeSeriesLabels tags
    Ref: https://labelstud.io/templates/time_series
    """
    import json
    
    df = pandas.read_csv(path)

    df = df.rename(columns={
        'timeseriesUrl': 'data_url',
    }, errors='ignore')

    # Extract data identifier, used for correlating with data
    df['file'] = df['data_url'].apply(extract_filename).drop(columns=['data_url'])

    labels = []
    for idx, row in df.iterrows():
        data = json.loads(row['label'])
        
        for label in data:
            #print(label)

            # Extract the actual label
            label_value = label['timeserieslabels']
            assert len(label_value) == 1, label_value
            del label['timeserieslabels']
            label['class'] = label_value[0]

            # Merge metadata from file level
            row_keys = set(row.keys()) - set(['label'])
            for k in row_keys:
                label[k] = row[k]
            
            labels.append(label)

    out = pandas.DataFrame.from_records(labels)
    
    return out
