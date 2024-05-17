
import seaborn
import pandas

df = pandas.read_parquet('out.parquet')
print(df)

# enrich results
leaf_bytes_per_class = 1
decision_node_bytes = 2

decision_nodes = df['test_nodes'] - df['test_leaves']
df['leaf_size'] = df['test_leasize'] * leaf_bytes_per_class * df['test_uniqueleaves']
df['decision_size'] = decision_nodes * decision_node_bytes
df['total_size'] = df['leaf_size'] + df['decision_size']

print(df.experiment.value_counts())

print(df.run.value_counts())


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

mm = mm.sort_values('perf_change', ascending=True)
print(mm.head(50))
print(mm.head(50).reset_index().dataset.unique())

