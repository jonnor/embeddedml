
import re
import os
import numpy
import pandas
import seaborn

# From https://github.com/pimoroni/as7343-micropython
CHANNEL_MAP = [
    "FZ", "FY", "FXL", "NIR", "VIS1_TL", "VIS1_BR",  # Cycle 1
    "F2", "F3", "F4", "F6", "VIS2_TL", "VIS2_BR",    # Cycle 2
    "F1", "F7", "F8", "F5", "VIS3_TL", "VIS3_BR",    # Cycle 3
]

def load_files(directory):

    dfs = []
    for filename in os.listdir(directory):
        suffix = os.path.splitext(filename)[1]
        filepath = os.path.join(directory, filename)
        if suffix != '.npy':
            print('Ignore', filename)
            continue    

        #tok = 
        data = numpy.load(filepath)
        #print(filename, data.shape)

        regex = r"(\w+)_(\d+)(\w+)_(\d+)(\w+)\.npy"
        match = re.findall(regex, filename)

        if not match:
            print('Ignored', filename)
            continue

        experiment, color_temp, _, lux, _ = match[0]

        avg = numpy.median(data, axis=1)
        assert len(avg) == 18

        # TODO: include all values, add measurement index
        # FIXME: add proper column names
        columns = ['ch_'+ch for ch in CHANNEL_MAP]
        df = pandas.DataFrame(data.T, columns=columns)
        df['datapoint'] = numpy.arange(len(df))

        df['filename'] = filename
        df['experiment'] = experiment
        df['lux'] = int(lux)
        df['colortemp'] = int(color_temp)

        #print(avg)
        #print(filename)

        dfs.append(df)

    out = pandas.concat(dfs)
    return out

def main():
    df = load_files('data/one')
    print('Raw')
    print(df.shape)
    print(df.head())

    g = seaborn.relplot(data=df, x='ch_FY', y='lux', col='colortemp')
    fig = g.figure
    plot_path = 'one_raw.png'
    fig.savefig(plot_path)
    print('Wrote', plot_path)

    # XXX: when using raw, there is no clear linear relationship with Lux

    index = ['filename']
    avg = df.groupby(index).agg('median', numeric_only=True)

    print('Averaged')
    print(avg.shape)
    print(avg.head())

    g = seaborn.relplot(data=avg, x='ch_FY', y='lux', col='colortemp')
    fig = g.figure
    plot_path = 'one_averaged.png'
    fig.savefig(plot_path)
    print('Wrote', plot_path)


    g = seaborn.relplot(data=df, x='datapoint', y='ch_FY', col='lux', col_wrap=5)
    fig = g.figure
    plot_path = 'one_datapoint.png'
    fig.savefig(plot_path)
    print('Wrote', plot_path)



if __name__ == '__main__':
    main()


