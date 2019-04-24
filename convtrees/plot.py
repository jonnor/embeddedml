
import pandas
from matplotlib import pyplot as plt

df = pandas.read_csv('results.csv')

fig, (est_ax, leaf_ax) = plt.subplots(1, 2, figsize=(8, 6))
df.plot.scatter(ax=est_ax, y='mean_test_score', x='param_n_estimators')
df[df.param_n_estimators == 100].plot.scatter(ax=leaf_ax, y='mean_test_score', x='param_min_samples_leaf')
leaf_ax.set_xscale('log')
leaf_ax.set_xlim(1e-9, 1e-2) 
fig.savefig('res.png')
