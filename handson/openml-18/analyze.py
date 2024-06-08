
import seaborn
import pandas

def plot_leaf_quantization(df, path):

    # TODO: also plot KDE and/or histogram
    # Isolate experiments that only change leaf quantization
    df = df[df.leaves_per_class.isna()]

    # Extract change in performance wrt no change
    def rel_perf(df, metric='test_roc_auc'):
        matches = df[df.leaf_bits.isna()]
        assert len(matches) == 1, matches
        ref = matches.iloc[0][metric]
        out = df[metric] - ref
        return out

    rel = df.groupby(
        ['dataset', 'split'], as_index=False
    ).apply(rel_perf, include_groups=False).reset_index().set_index('id')['test_roc_auc']
    df['perf_change'] = rel

    assert 'perf_change' in df.columns
    df = df.dropna(subset=['leaf_bits'])
    df['leaf_bits'] = df['leaf_bits'].astype('int').replace({0: '0 (majority vote)'})

    # Plot results
    g = seaborn.catplot(data=df, kind='strip',
        x='leaf_bits', y='perf_change',
        height=5, aspect=2.0,
    )
    g.refline(y=0.1)
    g.refline(y=-0.1)
    #g.set(xlim=(0.50, 1.0))

    if path is not None:
        g.figure.savefig(path)
        print('Wrote', path)

    return g


def plot_leaf_clustering(df, path):

    # isolate experiments that are only changing clustering
    df = df[df.leaf_bits.isna()]

    
    # Extract change in performance
    def rel_perf(df, metric='test_roc_auc'):
        matches = df[df.leaves_per_class.isna()]
        assert len(matches) == 1, matches
        ref = matches.iloc[0][metric]
        out = df[metric] - ref
        return out

    rel = df.groupby(
        ['dataset', 'split'], as_index=False
    ).apply(rel_perf, include_groups=False).reset_index().set_index('id')['test_roc_auc']
    df['perf_change'] = rel

    assert 'perf_change' in df.columns
    df = df.dropna(subset=['leaves_per_class'])

    # Plot results
    g = seaborn.catplot(data=df, kind='strip',
        x='leaves_per_class', y='perf_change',
        height=5, aspect=2.0,
    )
    g.refline(y=0.1)
    g.refline(y=-0.1)
    #g.set(xlim=(0.50, 1.0))

    if path is not None:
        g.figure.savefig(path)
        print('Wrote', path)

    return g



def enrich_results(df):

    # enrich results
    leaf_bytes_per_class = 1
    decision_node_bytes = 2

    decision_nodes = df['test_nodes'] - df['test_leaves']
    df['leaf_size'] = df['test_leasize'] * leaf_bytes_per_class * df['test_uniqueleaves']
    df['decision_size'] = decision_nodes * decision_node_bytes
    df['total_size'] = df['leaf_size'] + df['decision_size']

    df['test_roc_auc'] = 100.0 * df['test_roc_auc'] # scale up to avoid everything being in the decimals
    import uuid
    df['id'] = df.apply(lambda _: uuid.uuid4(), axis=1)
    df = df.set_index('id')

    return df

def main():

    # Load data
    df = pandas.read_parquet('out.parquet')

    print(df.shape)
    print(list(sorted(df.columns)))
    print(df.head(1))

    # Enrich
    df = enrich_results(df)


    print(df.experiment.value_counts())

    print(df.run.value_counts())



    print(df.leaves_per_class.unique())
    print(df.leaf_bits.unique())


    #plot_leaf_quantization(df, path='leaf-quantization.png')

    plot_leaf_clustering(df, path='leaf-clustering.png')


    # XXX
    return


    order = df.groupby('dataset').mean()['test_roc_auc'].sort_values().index
    g = seaborn.catplot(data=df, kind='box',
        x='test_roc_auc', y='dataset', hue='experiment',
        height=12, aspect=1.0, order=order,
    )
    g.set(xlim=(0.50, 1.0))

    g.figure.savefig('performance-grouped.png')



    mm = df.groupby(['experiment', 'dataset']).median()[['total_size', 'test_roc_auc']]
    print(mm)

    ref = mm.loc['rf10_none']

    mm['rel_size'] = mm['total_size'] / ref['total_size']
    mm['perf_change'] = mm['test_roc_auc'] - ref['test_roc_auc']

    seaborn.set_style("ticks",{'axes.grid' : True})
    g = seaborn.relplot(data=mm.reset_index(),
        x='rel_size', y='perf_change',
        hue='experiment',
        height=8,
        size=10.0,
        #col='dataset',
        #col_wrap=6,
    )
    g.figure.savefig('relperf.png')


    order = mm.groupby('experiment').min()['test_roc_auc'].sort_values().index
    print('\norder\n', order)

    order = [ 'rf10_float', 'rf10_16bit', 'rf10_8bit' ]

    order = [ 'rf10_leaf16bit', 'rf10_leaf8bit', 'rf10_leaf4bit', 'rf10_majority' ]

    seaborn.set_style("ticks",{'axes.grid' : True})
    g = seaborn.catplot(kind='box', data=mm.reset_index(),
        x='perf_change',
        y='experiment',
        order=order,
        #hue='dataset',
        height=8,
        aspect=2.0,
        #col='dataset',
        #col_wrap=6,
    )
    g.figure.savefig('stripplot.png')

    mm = mm.sort_values('perf_change', ascending=True)
    print(mm.head(10))
    #print(mm.head(10).reset_index().dataset.unique())

if __name__ == '__main__':
    main()
