

import os

import pandas
import numpy

def load_recordings(path,
        samplerate=52,
        sensitivity=4.0,
        maxvalue=32767,
        ):

    suffix = '.npy'

    files = []

    for f in os.listdir(path):
        if f.endswith(suffix):
            p = os.path.join(path, f)
            try:
                data = numpy.load(p, allow_pickle=True)
            except Exception as e:
                print(e)
                continue

            df = pandas.DataFrame(data, columns=['x', 'y', 'z'])

            # Scale values into physical units (g)
            df = df.astype(float) / maxvalue * sensitivity

            # Add a time column, use as index
            t = numpy.arange(0, len(df)) * (1.0/samplerate)
            df['time'] = t
            df = df.set_index('time')

            classname = os.path.splitext(f)[0].split('_')[1]
            
            # Remove :, special character on Windows
            filename = f.replace(':', '')

            files.append(dict(data=df, filename=filename, classname=classname))

            #print(f, data.shape)

    out = pandas.DataFrame.from_records(files)
    out = out.set_index('filename')
    return out

