
import seaborn
import pandas

import uuid
import math

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

def name_strategies(df):

    mm = df.copy()
    mm['strategy'] = 'other'
    mm.loc[mm.leaves_per_class.isna() & mm.leaf_bits.isna(), 'strategy'] = 'original'
    mm.loc[mm.leaves_per_class.isna() & (mm.leaf_bits.notna()), 'strategy'] = 'quantize'
    mm.loc[mm.leaves_per_class.notna() & (mm.leaf_bits.isna()), 'strategy'] = 'cluster'
    mm.loc[mm.leaves_per_class.notna() & (mm.leaf_bits.notna()), 'strategy'] = 'joint'
    mm.loc[mm.leaves_per_class.isna() & (mm.leaf_bits == 0.0), 'strategy'] = 'majority'

    return mm

def plot_perf_vs_size(df, path):

    # Drop data
    df = df[df.leaf_bits != 4]    

    # Extract change in performance
    def subtract_ref(df, metric='test_roc_auc'):
        matches = df[df.leaves_per_class.isna() & df.leaf_bits.isna()]
        assert len(matches) == 1, matches
        ref = matches.iloc[0][metric]
        out = df[metric] - ref
        return out

    def divide_ref(df, metric='test_roc_auc'):
        matches = df[df.leaves_per_class.isna() & df.leaf_bits.isna()]
        assert len(matches) == 1, matches
        ref = matches.iloc[0][metric]
        out = df[metric] / ref
        return out

    grouped = df.groupby(['dataset', 'split'], as_index=False)
    df['perf_change'] = grouped.apply(subtract_ref, include_groups=False).reset_index().set_index('id')['test_roc_auc']
    df['size_change'] = grouped.apply(divide_ref, metric='total_size', include_groups=False).reset_index().set_index('id')['total_size']

    mm = df.groupby(['leaf_bits', 'leaves_per_class'], dropna=False).median(numeric_only = True).reset_index()
    mm = name_strategies(mm)

    #assert 'perf_change' in df.columns
    #df = df.dropna(subset=['leaves_per_class'])

    # Plot results
    g = seaborn.relplot(data=mm, kind='scatter',
        x='size_change', y='perf_change', hue='strategy',
        height=5, aspect=2.0,
    )
    g.refline(y=0.0)
    #g.set(xlim=(0.50, 1.0))

    if path is not None:
        g.figure.savefig(path)
        print('Wrote', path)

    return g



def plot_size_improvement(df, path):

    # Filter data
    pass

    # Extract change in performance
    def subtract_ref(df, metric='test_roc_auc'):
        matches = df[df.leaves_per_class.isna() & df.leaf_bits.isna()]
        assert len(matches) == 1, matches
        ref = matches.iloc[0][metric]
        out = df[metric] - ref
        return out

    def divide_ref(df, metric='test_roc_auc'):
        matches = df[df.leaves_per_class.isna() & df.leaf_bits.isna()]
        assert len(matches) == 1, matches
        ref = matches.iloc[0][metric]
        out = df[metric] / ref
        return out

    grouped = df.groupby(['dataset', 'split'], as_index=False)
    df['perf_change'] = grouped.apply(subtract_ref, include_groups=False).reset_index().set_index('id')['test_roc_auc']
    df['size_change'] = grouped.apply(divide_ref, metric='total_size', include_groups=False).reset_index().set_index('id')['total_size']

    df = name_strategies(df)


    df = df[df.strategy == 'joint']
    df = df[df.leaf_bits == 8]
    df = df[df.perf_change >= -1.0]

    #df.groupby(['dataset', ''])

    # make categorical
    df['leaves_per_class'] = df['leaves_per_class'].astype('Int64').astype(str)

    best = df.groupby(['dataset', 'leaves_per_class'], dropna=False).median(numeric_only=True).reset_index()

    def find_best(df):
        s = df.sort_values('size_change', ascending=True)
        b = s.iloc[0]
        return b


    best = best.groupby(['dataset']).apply(find_best)

    # Plot results
    g = seaborn.relplot(data=best, kind='scatter',
        x='size_change', y='perf_change', hue='leaves_per_class',
        height=6, aspect=2.0, #s=5.0,
    )
    g.refline(y=0.0)
    g.set(xlim=(0, 1.0))

    if path is not None:
        g.figure.savefig(path)
        print('Wrote', path)

    return g



def enrich_results(df):

    # compute storage size
    leaf_bytes_per_class = df['leaf_bits'] / 8
    leaf_bytes_per_class = leaf_bytes_per_class.fillna(value=4).astype(int)

    # FIXME: take the feature precision into account
    decision_node_bytes = 2

    df = df.rename(columns={'test_leasize': 'test_leafsize'}) # Fixup typo

    decision_nodes = df['test_nodes'] - df['test_leaves']
    df['leaf_size'] = df['test_leafsize'] * leaf_bytes_per_class * df['test_uniqueleaves']
    df['decision_size'] = decision_nodes * decision_node_bytes
    df['total_size'] = df['leaf_size'] + df['decision_size']

    df['test_roc_auc'] = 100.0 * df['test_roc_auc'] # scale up to avoid everything being in the decimals

    # Add identifier per row, for ease of merging data
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


    plot_size_improvement(df, path='size-improvement.png')

    #plot_perf_vs_size(df, path='size-change.png')

    #plot_leaf_quantization(df, path='leaf-quantization.png')

    #plot_leaf_clustering(df, path='leaf-clustering.png')




if __name__ == '__main__':
    main()
