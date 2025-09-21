
## Data collection for Machine Learning
With an emphasis on applications to sensor data, physical phenomena.

Simplified system model. Input data -> model output.
Regression, classification or anomaly detection type tasks.

Can be TinyML / Edge AI cases, or desktop/mobile/cloud ML.

## Key aspects

- Need to define our objectives.
What is the purpose of our solution. Primary, secondary.
In which circumstances will it be used. What users, which environments
What are the most important "axes" of generalization? 

- Need to capture the entire space of data
In terms of inputs, and outcomes
Include benefit of correct and consequence-of-error for the various cases.


## Stages

- Planning
- Data collection execution
- Dataset validation
- Use for model
- 

## Context of this content

Aim to build better *data* literacy.
More focus on the data in Data Science and Machine Learning.
Compliment to the extremely model centric approach for most ML.

Data. In high quality, sufficient quantity is the key to ML.
Both to make-something-actually-work. And for competitive advantage, commercial value. 
Models are commodity.


## Want to cover

- Why dataset collection matters, especially with deep learning.
Fails out-of-distribution. Misleading metric values. Looks good, fails in practice.
- How to identify (potential) factors and observational variables, covariates.
Brainstorming. Multi-perspective. Causal graphs.
Literature review. Sensor, environment, subject-of-interest, other-subjects/actors.
- Setting up expectations.
How are each factor/variable expected to influence the data.
- Factors that are independent of the variable of interest. Class-invariance. Mostly/fully.
- How to capture factors and observational variables, structured way. Document. Carry metadata along data samples.
- How to reduce the factorial explosion. Fractionall factorical. Pairwise interactions.
- How to validate our dataset. For coverage, bias. Fairness. Sub-group analysis.
- How to identify out-of-distribution cases. In dataset, in production.
- Using factors and observed variables for error analysis
- How simple features can help dataset and model analysis
- Ways of handling variation in the data. Elimination, normalization, learned adaptation 
- How imbalances in your data affects. The typical gets the most priority. Both in the loss, and in aggregate metrics.
- Difficulty proxy metrics/variables. Good/borderline/bad. Ex: SNR in speech. Usage as FP guards.
- Confusor objects, things that are genuinely quite close to targets (by nature, in data space),
but are actually different. Risk analysis. Prevalence: Common vs rare. Consequence: high vs low.
- Comparing datasets. Ex: controlled collection vs production data.
- Picking data augmentation techniues and ranges, based on observed data.

Maybe

- Strategies for labeling data. 
- Average case vs worst-case error

Explore

- domain adaptation techniques?
- Smart fractional designs, like Resolution IV+ ?


## Pedagogical tools

Things that we would like to show intutively - visually

- Illustrate out-of-distribution, prediction problems. In 2d data space
- Illustrate how poor subgroup performance does not show in aggregate metrics. Ex 10%
- Illustrate how inbalanced data can lead to poor performance for other sub-groups
- ? show how incorrect splits lead to data leakage. Grouped vs non-grouped splitting


## Potential covariates

- User demographics
- Environmental conditions (e.g., temperature, humidity)
- Device metadata (e.g., phone model, sensor type)
- Time of day, day of week, etc.

! know your distributions. Consider balancing. Pre collection or post collection.


