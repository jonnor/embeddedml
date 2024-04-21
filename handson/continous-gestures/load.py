
import glob
import os.path

import pandas
import numpy
import cbor2

def load_cbor_file(path):
    """
    Load .cbor file for EdgeImpulse datasets
    """
    
    with open(path, 'rb') as f:
        obj = cbor2.load(f)

        interval = pandas.Timedelta(obj['payload']['interval_ms'], unit='millisecond')
        sensors = obj['payload']['sensors']
        columns = [ s['name'] for s in sensors ]

        values = obj['payload']['values']
        df = pandas.DataFrame.from_records(values, columns=columns)
        df['time'] = interval * numpy.arange(0, len(df))
        df = df.set_index('time')

        return df

def load_dataset(path):

    dfs = []
    for filename in glob.glob('*.cbor', root_dir=path):
    
        # expecting format
        # "snake.3.cbor"
        df = load_cbor_file(os.path.join(path, filename))
        tok = os.path.basename(filename).split('.')
        classname, sample, ext = tok
        df['class'] = classname
        df['sample'] = int(sample)
        dfs.append(df)

    out = pandas.concat(dfs)
    out = out.reset_index().set_index(['class', 'sample', 'time'])

    return out    



path = 'data/original/training'
df = load_dataset(path)
print(df)


    #print(obj)
