
Related works

Bonsai

Rocket. Convolutions random projection
Feature learning with trees on time-series

Deep gradient booting for tabular data
Neural Oblivious Decision Ensembles for Deep Learning on Tabular Data
https://arxiv.org/abs/1909.06312
Oblivous trees
https://stats.stackexchange.com/questions/353172/what-is-oblivious-decision-tree-and-why

TabNet: Attentive Interpretable Tabular Learning
https://arxiv.org/abs/1908.07442
self-supervised tabular learning

https://pytorch-tabular.readthedocs.io/en/latest/models/


Feature learning packages


Motivation

Event Detection in time-series
Highly imbalanced classes
Normal class dominates. Should be quick to classify


Trees

Memoize pre-processing. So that (intermediate) results can be reused.

Challenge:
Many pre-processing functions have many parameters, often continious.
Huge space of possibilities to search through.
Solution: Using gradient boosting, differentiable pre-processing functions?

Not suitable for easy on-target learning anymore.
But could still be fast at inference time?

Gradient boosting evaluation tree-by-tree.
Can one do "early stopping" inference?
Convergence




