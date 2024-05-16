
import seaborn
import pandas

df = pandas.read_parquet('out.parquet')
print(df)


g = seaborn.catplot(data=df, kind='box', y='test_score', x='dataset', hue='experiment')
g.set(ylim=(0.90, 1.0))

g.figure.savefig('analyze.png')
