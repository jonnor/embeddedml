
import pandas

df = pandas.read_csv('out.csv', header=0, names=['time', 'level', 'fast'])

ax = df.plot(y=['level', 'fast'], x='time')

ax.figure.savefig('out.png')

