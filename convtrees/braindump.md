
# Things to optimize for

- Inference efficiency. Inference time VS Performance.
Critical for embedded devices.
- Dataset efficiency. Dataset size VS Performance
Small datasets are the norm.
Labeled training data is expensive.
- Training time. 
Compute is cheap. Mostly relevant for online learning.
But if extensive hyper-parameter search is needed, importance grows. 
- Robustness to adverse examples
- Interpretability


# Questions

What kind of performance can one achieve with

- N random convolutional kernels of size K, at random locations
- N random convolutional kernels of size K, at uniform grid locations
- N random kernels from codebook of C well-known kernels
- N kernels from learned (SKM) codebook of C kernels
- N kernels from transfered codebook from kernels of pretrained models


Support pre-seeding a codebook of kernels
Allows semi-supervised extension, reusing existing codebook learning methods

Maybe a combination of well-known kernels and learned-from data kernels is best?

Could try to prefer existing kernels.
Only choose a new one if better by factor X.

One could try to learn shared kernels (from anywhere), as well as learn position-dependent kernels. 

CNNs follow the thesis that kernel (weights) are useful regardless of their location.
The antithesis is that the best kernels are position-dependent.
Might be more true on a spectrogram (along frequency axis) than in general image.
And less true if need to be translation invariant? But maybe it should just be learned via data augmentation anyway
But the two are not neccesarily in opposition.

Could try to favor learning spatially separable kernels?


ExtraTrees, also subsamples data randomly

# 

# Datasets

## MNIST
http://yann.lecun.com/exdb/mnist/

RandomForest(n_estimators=100)
```
CV results
   param_min_samples_leaf  mean_train_score  mean_test_score
0                  1e-07          1.000000         0.964883
1            1.58489e-06          1.000000         0.964550
2            2.51189e-05          0.999317         0.963000
3            0.000398107          0.966308         0.946567
4             0.00630957          0.892408         0.888417
5                    0.1          0.678076         0.675383
Accuracy:  0.9702
```
3% error out-of-box

SVM with RBF 1.4%
CNN LeNet-4 1.1%



# References

@incollection{coates2012learning,
  title={Learning feature representations with k-means},
  author={Coates, Adam and Ng, Andrew Y},
  booktitle={Neural networks: Tricks of the trade},
  pages={561--580},
  year={2012},
  publisher={Springer}
}

@inproceedings{burciu2017sensing,
  title={Sensing Forest for Pattern Recognition},
  author={Burciu, Irina and Martinetz, Thomas and Barth, Erhardt},
  booktitle={International Conference on Advanced Concepts for Intelligent Vision Systems},
  pages={126--137},
  year={2017},
  organization={Springer}
}

@inproceedings{kohonen1990improved,
  title={Improved versions of learning vector quantization},
  author={Kohonen, Teuvo},
  booktitle={1990 IJCNN International Joint Conference on Neural Networks},
  pages={545--550},
  year={1990},
  organization={IEEE}
}

## Improved versions of Learning Vector Quantization
@kohonen1990improved

Introduced 

## Sensing Forest for Pattern Recognition
[@burciu2017sensing]

Uses k-means++ for learning low dimensional representation of the data.
Applies Learning Vector Quantization (LVQ) to compress codebook.
LVQ1 and LVQ3 variants.

> The goal is to learn efficient features for classification.
> This problem is approached by learning different tree structures that involve an hierarchical partitioning of the dataset.
> The resulting partitioning is used to solve the sensing problem more efficiently,
> i.e., to use as few sensing values as possible in order to sense and classify an unknown scene or object

! only tested with up to 20 trees.

MNIST
RF baseline 94%. Theirs: 96%

COIL-100. 128x128. Originally color. Paper used grayscale.
RF baseline 89%. Theirs: 92%
 
! results does not account for added computational complexity

## CAN LEARNING VECTOR QUANTIZATION BE AN ALTERNATIVE TO SVM AND DEEP LEARNING?
- RECENT TRENDS AND ADVANCED VARIANTS OF LEARNING VECTOR QUANTIZATION FOR CLASSIFICATION LEARNING
JAISCR, 2017

> Although deep learning architectures and support vector classifiers frequently achieve comparable or even better results
> LVQ models are smart alternatives with low complexity and computational costs making them attractive
> for many industrial applications like intelligent sensor systems

LVQ
pre-determined complexity due to the fixed number of prototypes



