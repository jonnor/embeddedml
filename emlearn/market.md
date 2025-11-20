
Most practitioners do not want an ML inference library.
They want a working ML-powered application,
with *as little effort and risk as possible*.

1. Make it work
2. Make it good
3. Make it efficient

Technology choice is often made at 1)
- if the proof-of-concept works, and no new blockers come up, they stick with that.

Hardware trends

- FLASH and RAM has become much cheaper. 1MB+ now quite usual
- Floating point FPU standard on majority of application MCUs
- SIMD available for many. ARM NEON in Cortex M4F+
- NPUs now available in high-end MCUs


Software trends

- Deep-learning replaced/reduced need for feature engineering. Esp for 1) PoC/make it work stage.
- Neural networks as the go-to-solution for practically any problem
- Gradient boosted trees (XGBoost/LightGBM) etc as go-to for high-perf on tabular style data
- General-purpose models for entire domains. Pre-trained, embedding models, or fine-tuned
- End-to-end training of differentiable programs, generalization of deep neural networks
- Sharing repositories of pre-trained models. HuggingFace etc
- End-to-end service for train & deploy of custom models. Ex Edge Impulse
- AutoML. Automated tuning of hyperparameters and networks
- PyTorch as a favored tool for researchers over Tensorflow
- JAX as up-and-coming potential alternative to PyTorch
- Talk of "foundational model" for tiny systems. Big challenges in efficiency still


ExecuTorch - deploy PyTorch

https://docs.pytorch.org/executorch/stable/platforms-embedded.html#microcontrollers

arm-baremetal - Build for bare-metal ARM targets.
zephyr - Build for Zephyr RTOS.

## Areas of active research

Researchers often have other priorities.

Application-oriented researchers. Working on PoC/make-it-work level. Similar mindsent as ML application developers.


- Robustness. Performance in all cases. Guaranteed perforance. Resistance to adverserial attacks.
- Adaptability. Few shot learning.
- Efficiency. How to squeeze out extra NN%. Or how to potentially improve efficiency by N times.
- Explainability/interpretability. How to have on-edge models that are explainable & interpretable
- Hardware-software co-design. How can one design even more integrated solutions, even closer to sensor edge

## Ideas

- Compare neural networks vs Random Forest vs Gradient boosted trees in TinyML settings. Which is most efficient? Assuming pre-created features
- Tutorial/docs on explainable and interpretable models for sensor data. ? in which applications is this most relevant
- How to deal with out-of-distribution data

