
## Challenge 1
Challenge 1.
Try different epsilon / min_pts.
How does the results change.

- Inter-distance
- Intra-distance
- Number of clusters
- Cluster size distribution. largest-smallest ?




Gridsearch.
Baysian optimization

How much of samples is classified as noise?
The average of 5 fooditems by weight are taken.
How does this influence clustering? Is it stable to permutations
Is there agreement within the foodcodes for the mean?
What if one would chose criteria to be different from by-weight
What if one would just cluster everything?

What would happen if performing PCA to reduce dimension?

Why is Z-score used instead of just regular standardization?

What is actually the purpose/interpretation of the clusters?

How many clusters is desired?

"Development of a Scalable Method for Creating Food Groups Using the NHANES Dataset and MapReduce"

Identifying food patterns.
Healthy Eating Index-2010.
Mediterranean Diet Score.
Identifying clusters of individuals with similar dietary intakes

Rely on pre-defined food groups.
Assumption: Food groups should consist of those highly similar in nutrient content.

National Health and Nutrition Examination Survey (NHANES) dataset


Claim: Our preprocessing ensures that our method
minimizes the introduction of subjectivity into the food grouping.

45 features mentioned. Tutorial uses 56??


Goal
identify high quality food groups
which have smaller diameter (more internally similar) and
larger cluster separation (more externally different) than
the standard, expert-informed, method of grouping food items

Proposed clustering has 8 groups
USDA 2 leading digit has 47 groups
USDA 3 leading digits has 118 groups

### Scalability

food entries 1,587,750
unique food items 7,494

Claim: our method is developed with scalability in mind.
Claim: The ever-increasing amount of collected data must be processed in parallel
in order to maintain the ability for time efficient analysis

? new food items not added very often ?

Is Spark DBSCAN faster than scikit-learn?
Does it hold if dataset size is increased?
What is the memory consumption?


How 

Challenge 2.


Challenge 3.
Preprocessed data
compare and contrast k-means and DBSCAN.
Maybe reducing to macro-nutriends.


Email solutions to

taufer@gmail.com
dylanchapp@gmail.com
