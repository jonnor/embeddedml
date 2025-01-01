
"""
Combine sensor data and labels into a dataset
"""

import subprocess
import os
import json

import plotly.express
import pandas
import numpy

from software.utils.labelstudio import read_timeseries_labels


def parse_har_record_filename(f):

    tok = f.replace('.npy', '').split('_')
    datestr, label = tok

    s = pandas.Series({
        'time': pandas.Timestamp(datestr),
        'label': label,
    })
    return s

def load_har_record(path,
        samplerate,
        sensitivity,
        maxvalue=32767,
        suffix = '.npy'
        ):
    """Load dataset from har_record.py, from emlearn-micropython har_trees example"""

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

            classname = f.split('_')[1].rstrip(suffix)
            
            # Remove :, special character on Windows
            filename = f.replace(':', '')

            files.append(dict(data=df, filename=filename, classname=classname))

            #print(f, data.shape)

    out = pandas.DataFrame.from_records(files)
    out = out.set_index('filename')
    return out


def parse_video_filename(path):
    # Expects filename on form VID_20241231_155240
    basename = os.path.basename(path)
    filename, ext = os.path.splitext(basename)

    tok = filename.split('_')
    vid, date, time = tok

    dt = pandas.to_datetime(filename, format='VID_%Y%m%d_%H%M%S')
    #dt = pandas.to_datetime(date, format='%Y%m%d')
    #print(filename)
    return dt

def find_label_gaps(df):
    df = df.sort_values('start')
    gaps = df.shift(-1)['start'] - df['end']
    return gaps

def read_labels(path):

    labels = read_timeseries_labels(path, label_column='activity', label_key='labels')
    # XXX: this is toothbrushing specific
    labels['filename'] = labels['file'].str.replace('label_', '')

    # Enrich
    labels['duration'] = labels['end'] - labels['start']
    gg = labels.groupby('filename', as_index=False).apply(find_label_gaps, include_groups=False).droplevel(0)
    labels['gap'] = gg

    return labels


def apply_labels(data, labels,
                 label_column='class',
                 time='time',
                 groupby='filename'):

    labels = labels.set_index(groupby)
    labels['start'] = pandas.to_timedelta(labels['start'], unit='s')
    labels['end'] = pandas.to_timedelta(labels['end'], unit='s')

    def apply_labels_one(df):
        group = df.name
        df = df.set_index(time)
        
        # Find relevant labels
        try:
            ll = labels.loc[group]
        except KeyError as e:
            print('No labels found for', group, df.index.max())

            df = df[df.index == 'SHOULD BE FALSE']
            assert len(df) == 0
            return df

        # Apply the labels
        dup = df[df.index.duplicated()]
        assert len(dup) == 0, dup
        
        df[label_column] = None
        
        #print(df.head())
        for idx, l in ll.iterrows():
            s = l['start']
            e = l['end']
            #print(s, e)
            df.loc[s:e, label_column] = l['class']

        #print(ll)
        #df = df.reset_index()

        return df
    
    out = data.groupby(groupby).apply(apply_labels_one)
    return out


def load_data(path):
    samplerate = 50
    sensitivity = 2.0

    files = load_har_record(path, samplerate=samplerate, sensitivity=sensitivity)
    files = files.reset_index()
    stats = files.filename.apply(parse_har_record_filename).add_prefix('file_')
    files = pandas.merge(files, stats, right_index=True, left_index=True)

    dfs = []
    for idx, f in files.iterrows():
        df = f.data.reset_index()
        df['filename'] = f.filename
        df['time'] = f.file_time + pandas.to_timedelta(df['time'], unit='s')
        dfs.append(df)

    data = pandas.concat(dfs)

    return data

def main():


    sensor_data_path = 'data/jonnor-brushing-1/har_record/'
    labels_path  = 'data/jonnor-brushing-1/labels/project-7-at-2024-12-31-23-50-84589958.csv'
    out_path = 'data/jonnor-brushing-1/combined.parquet'

    # Load sensor data
    data = load_data(sensor_data_path)
    print(data)
    
    # Load labels
    labels = read_labels(labels_path)

    print(labels)

    # Combine labels and data
    merged = apply_labels(data, labels)
    #merged['is_motion'] = ~lb['class'].isin(['docked'])
    merged['is_brushing'] = lb['class'].isin(['brushing'])
    merged

    print(merged.is_brushing.value_counts())

    merged.to_parquet(out_path)

if __name__ == '__main__':
    main()


