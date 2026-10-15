# Data Mining Test 1 Study Guide

This guide covers Homework 1A/B, Homework 2A/B, and Lectures 01 through 04a (PCA). The test emphasizes concepts, theory, principles, and light interpretation of code. Use this document to understand the ideas first, then use the final checklist to compress the material into the one-page note sheet allowed during Part A.

## Test Format and Strategy

- Part A: 70 minutes, mostly multiple choice with some short answers and light code interpretation.
- Closed book except for one single-sided sheet of notes. A calculator, blank scratch paper, and writing tools are allowed.
- Prioritize definitions, assumptions, statistic choice, interpretation of output, and recognizing when a method changes the data representation.
- For any computed statistic, identify the two groups, the outcome, the subtraction order, and the units before interpreting its sign.
- For any p-value or confidence interval, state what was simulated and what population or null-model assumption makes the statement meaningful.

## 1. Data, Questions, and Reproducible Discovery

### Observational units and variables

- An **observational unit** is what one row represents: a penguin, shopping session, utility company, customer, or another recorded entity.
- A **population** is the broader set of units or process about which a claim might be made. The recorded dataset is a sample or observed collection, not automatically the whole population.
- A **group variable** assigns observations to categories such as male/female, new/returning, or Horeca/Retail.
- An **outcome** is the measurement being compared, such as body mass, purchase status, spending, or page duration.
- A **context variable** can explain structure that should be preserved, such as region or weekend status.
- A **point estimate** is one numerical summary computed from the observed data.

### A reproducible analysis workflow

1. State the question in words and identify the observational unit.
2. Identify group, outcome, and relevant context variables.
3. Inspect shape, column names, data types, missing values, and category labels.
4. Map coded values to readable labels when needed.
5. Decide on a statistic that matches the real decision or question.
6. Visualize or summarize each group before testing.
7. State the data limitations: sampling design, missingness, dependence, and generalizability.
8. Use a reproducible random seed for simulation-based results.
9. Interpret the result in the original units and in the context of the question.

### Description is not causation

An observed group difference describes the recorded units. It does not by itself prove that group membership caused the difference. Generalization requires that the recorded units reasonably represent the target population; causal claims require an appropriate design or additional assumptions. If the sampling design is undocumented or non-random, be cautious about extending the result beyond the data.

### Mean, median, rates, and quartiles

Different statistics answer different questions:

- **Mean difference:** compares average magnitude and uses every numerical value.
- **Median difference:** compares the middle of each group and is less affected by extreme values.
- **Exceedance-rate difference:** compares the proportions above a decision threshold.
- **Upper-quartile difference:** compares a high-but-not-maximum part of each distribution.

The statistic is part of the question. A warehouse capacity decision based on whether body mass exceeds 4,500 g calls for an exceedance rate, not merely a mean difference.

### Useful pandas and NumPy ideas

```python
group_values = records.loc[records["group"] == "A", "outcome"].to_numpy()
counts = records["group"].value_counts()
rate = (records["outcome"] > threshold).mean()
```

In NumPy, `True` behaves like 1 and `False` like 0 in a mean, so the mean of a Boolean condition is the proportion for which the condition is true. Always check missing values before grouping or calculating a rate.

## 2. Permutation Tests and Inference

### The core idea

A permutation test asks whether an observed association or group difference is surprising under a **no-association null model**. Under this model, outcomes are unrelated to group labels, so labels can be reassigned while preserving the relevant structure.

1. Choose a statistic $T$ that represents the question.
2. Calculate the observed statistic $T_{obs}$.
3. Define what must remain fixed: often group sizes, and sometimes counts within regions or other strata.
4. Randomly reassign labels or otherwise simulate data under the null model.
5. Recalculate $T$ for every reassignment to form the null distribution.
6. Count how often simulated results are at least as extreme as $T_{obs}$.

For a signed difference, for example,

$$T = \operatorname{median}(\text{Retail}) - \operatorname{median}(\text{Horeca}).$$

The sign is meaningful only after the subtraction order is declared. A two-sided test treats unusually positive and unusually negative results as extreme.

### P-values

A p-value is the proportion of null-model simulations that produce a statistic at least as extreme as the observed statistic. It is **not** the probability that the null hypothesis is true, and it is not the probability that the observed result happened by chance in an unrestricted sense.

For a simulation with an observed result included,

$$\hat p = \frac{\#\{\text{simulated statistics at least as extreme}\}+1}{n_{resamples}+1}.$$

The simulation-resolution floor is about $1/(n_{resamples}+1)$. A very small reported p-value may mean the result is at the smallest resolution the simulation can show, not that the probability is literally zero.

### Exchangeability and structure

Permutation is valid only for units that are exchangeable under the null model. If region affects the outcome and group composition differs by region, an unstratified permutation may destroy important structure. A region-stratified permutation reassigns labels within each region while preserving the number of each group in each region.

The key question is: **What relationships should remain fixed under the null model, and what relationship is being broken?**

### Interpretation template

> Under the no-association model represented by the permutation procedure, about [p-value] of reassignments produced a statistic at least as extreme as the observed [statistic]. This provides [weak/strong] evidence against no association for the recorded units, subject to the exchangeability and sampling assumptions.

### SciPy code interpretation

```python
result = permutation_test(
	(group_a, group_b),
	statistic=statistic_function,
	permutation_type="independent",
	alternative="two-sided",
	n_resamples=5000,
	random_state=7130,
)
```

- `result.statistic`: the observed statistic.
- `result.pvalue`: the simulated tail proportion.
- `result.null_distribution`: statistics from the simulated null worlds.
- `permutation_type="independent"`: appropriate when the two groups are independent samples, not paired observations.
- A seed makes the pseudorandom result reproducible; it does not remove sampling uncertainty.

## 3. HW1A: Design and Test a Statistic

### Penguin comparison

The outcome is `body_mass_g`, the group variable is `sex`, and the observational unit is a penguin. The mean-difference statistic used in the homework is

$$T_{mean} = \overline{x}_{male} - \overline{x}_{female}.$$

The test uses an independent, two-sided permutation procedure. Know how to explain why the subtraction order determines the sign and why the statistic must be chosen before looking for a favorable result.

### Equipment-limit question

For a 4,500 g equipment limit, define an indicator for each penguin:

$$I_i = \begin{cases}1 & \text{if } body\_mass\_g_i > 4500 \\ 0 & \text{otherwise.}\end{cases}$$

The exceedance rate in a group is

$$\hat p = \operatorname{mean}(body\_mass\_g > 4500),$$

and the homework statistic is

$$T_{rate} = \hat p_{male} - \hat p_{female}.$$

This statistic directly addresses the fraction of units that exceed capacity. It discards the exact magnitude of values within the below-threshold and above-threshold categories.

### Likely conceptual traps

- A rate difference is not a mean difference.
- A positive male-minus-female result means the male group has the larger estimated value or rate.
- The null distribution comes from reassigning group labels, not from resampling penguins with replacement.
- A statistically unusual difference does not establish that sex caused body mass differences.
- Missing required fields can change group sizes and invalidate a careless calculation.

## 4. Bootstrap and Sampling Variability

### The core idea

A bootstrap estimates how a statistic would vary across repeated samples by treating the observed data as an empirical approximation to the population. It resamples observed units **with replacement**, usually within each group, and recalculates the statistic.

For a purchase-rate comparison,

$$T_{rate} = \hat p_{new} - \hat p_{returning}.$$

One bootstrap replicate draws a same-sized sample from each original group with replacement and calculates $T_{rate}$ on those samples. Many replicates form the bootstrap distribution.

### Important terms

- **Point estimate:** the statistic from the original observed groups.
- **Bootstrap sample:** one resampled dataset, with replacement.
- **Bootstrap replicate:** the statistic calculated from one bootstrap sample.
- **Bootstrap distribution:** the collection of many replicates.
- **Standard error:** the spread of the bootstrap distribution; an estimate of sampling variability.
- **Percentile confidence interval:** selected quantiles of the bootstrap distribution.

For a 95% percentile interval, use the 2.5th and 97.5th percentiles:

$$[q_{0.025}, q_{0.975}].$$

### What a bootstrap interval means

In the course's empirical-distribution framing: if the recorded groups reasonably represent their target populations and the resampling assumptions are reasonable, the interval gives plausible values for the population difference under the method's long-run coverage interpretation. It is not the probability that a fixed parameter is random, and it does not repair biased or unrepresentative data.

### Ordinary versus structured bootstrap

For HW1B, the ordinary bootstrap resamples each visitor group independently. A weekend-preserving or structured bootstrap resamples within cells such as visitor type by weekend status, then recombines the cells. This keeps the observed composition fixed while estimating variability.

Use stratification when the structure is part of the sampling or data-generating design and should not be erased. Compare ordinary and structured results as a sensitivity check rather than assuming one is universally correct.

### Permutation versus bootstrap

| Question | Permutation test | Bootstrap |
|---|---|---|
| Main purpose | Test evidence against no association | Estimate sampling variability |
| Simulated world | Null model where labels and outcomes are unrelated | Repeated samples from the empirical distribution |
| Replacement | Usually reassigns labels; no replacement of values | Samples with replacement |
| Main output | Null distribution and p-value | Bootstrap distribution, SE, and CI |
| Key assumption | Exchangeability under the null | Observed units represent the target population sufficiently |

### Bootstrap code patterns

```python
rng = np.random.default_rng(7130)
sample_a = rng.choice(group_a, size=len(group_a), replace=True)
sample_b = rng.choice(group_b, size=len(group_b), replace=True)
replicate = statistic(sample_a, sample_b)

lower, upper = np.quantile(replicates, [0.025, 0.975])
```

Seeding once creates a reproducible random sequence. Re-seeding inside every loop iteration would repeatedly generate the same first draw and is incorrect. `replace=True` is essential: without it, the procedure is sampling without replacement, not a bootstrap.

## 5. Distance, Scaling, and Nearest Neighbors

### Representation comes first

Distance is calculated between feature vectors. The chosen features, their units, their scales, and their order all affect the result. A nearest neighbor is simply an observation ranked as close under a chosen metric; it is not automatically similar in every meaningful sense.

### Euclidean distance

For vectors $x$ and $y$ with $p$ features,

$$d_{Euclidean}(x,y) = \sqrt{\sum_{j=1}^{p}(x_j-y_j)^2}.$$

Large numerical ranges can dominate the squared gaps. In the utility example, a high-range feature such as Sales can overwhelm smaller-scale features. Inspect feature ranges and squared contribution shares before interpreting raw distances.

### Manhattan distance

$$d_{Manhattan}(x,y) = \sum_{j=1}^{p}|x_j-y_j|.$$

Manhattan distance adds absolute coordinate gaps rather than squaring them. It can therefore rank neighbors differently from Euclidean distance, especially when one feature has a very large discrepancy.

### Standardization

Standardization puts each feature on a comparable scale:

$$z_j = \frac{x_j-\bar{x}_j}{s_j}.$$

After standardization, each feature has mean approximately 0 and standard deviation approximately 1 under the selected convention. Recompute distances after scaling; do not assume raw nearest neighbors remain nearest.

Be precise about the standard deviation convention:

- HW2A distance scaling uses `std(ddof=0)`.
- HW2B PCA standardization uses `std(ddof=1)` to match sample covariance and the homework calculations.

Standardization is not automatically correct. It is useful when units or ranges should not determine importance, but it can remove meaningful domain scale.

### Distance workflow and code cues

1. Select and order the features explicitly.
2. Represent the anchor as a 2D row, for example `matrix.loc[[anchor]]`.
3. Calculate distances to all rows.
4. Remove the anchor's self-distance before ranking.
5. Sort ascending for distance and take the nearest $k$ rows.

```python
distances = cdist(matrix.loc[[anchor]], matrix, metric="euclidean").ravel()
ranking = pd.Series(distances, index=matrix.index).drop(anchor).sort_values().head(3)
```

Using double brackets preserves a two-dimensional shape for `cdist`. Forgetting to remove the anchor returns the trivial answer: the anchor itself at distance 0.

## 6. Cosine and Jaccard Similarity

The similarity measure encodes what “similar” means. Euclidean and Manhattan compare coordinate gaps; cosine compares direction; Jaccard compares binary set overlap.

### Cosine similarity

For quantity or duration vectors,

$$s_{cos}(x,y) = \frac{x^T y}{\lVert x \rVert_2\lVert y \rVert_2}, \qquad \lVert x \rVert_2 = \sqrt{\sum_j x_j^2}.$$

Cosine measures the angle between vectors. It focuses on proportions and ignores overall magnitude. Vectors with the same direction, even if one is 10 times larger, have cosine similarity 1. A zero vector has no defined direction, which is why all-zero sessions were excluded in the homework comparison.

SciPy's `cdist(..., metric="cosine")` returns cosine distance, so convert it to similarity with

$$similarity = 1 - distance.$$

### Jaccard similarity

Convert quantities to presence/absence sets first. If $A$ and $B$ are the products purchased by two customers,

$$J(A,B) = \frac{|A\cap B|}{|A\cup B|}.$$

Jaccard ignores quantities and shared absences. It is 1 for identical sets and 0 for no shared present items. The union matters: many shared items do not guarantee a large Jaccard value if the union is even larger.

### Metric comparison

| Metric | Representation | Sensitive to | Ignores or emphasizes |
|---|---|---|---|
| Euclidean | Numeric quantities | Scale and coordinate gaps | Nothing by default |
| Manhattan | Numeric quantities | Absolute coordinate gaps | Squaring/outlier amplification relative to Euclidean |
| Cosine | Numeric vector | Relative proportions/direction | Overall magnitude |
| Jaccard | Binary presence set | Shared presence relative to union | Quantities and shared absences |

For browsing sessions, raw durations, standardized durations, and binary page-presence data answer different questions. There is no universally best metric independent of the analysis goal.

## 7. PCA Foundations

### Why dimensionality reduction?

Dimensionality reduction represents observations with fewer coordinates while retaining useful information.

- **Feature selection:** keep a subset of original features; meanings remain directly recognizable.
- **Feature extraction:** construct new features from the originals; PCA does this through linear combinations.

PCA is most useful when several measurements contain correlated or redundant variation and a lower-dimensional summary is acceptable.

### Variance and covariance

For one feature,

$$s^2 = \frac{1}{n-1}\sum_{i=1}^{n}(x_i-\bar{x})^2.$$

For two features,

$$\operatorname{Cov}(x_1,x_2) = \frac{1}{n-1}\sum_{i=1}^{n}(x_{1i}-\bar{x}_1)(x_{2i}-\bar{x}_2).$$

The sample covariance matrix is

$$S = \begin{bmatrix}
\operatorname{Var}(x_1) & \operatorname{Cov}(x_1,x_2) \\
\operatorname{Cov}(x_1,x_2) & \operatorname{Var}(x_2)
\end{bmatrix}.$$

The diagonal contains variances; the off-diagonal entries contain covariances. Total variance is the sum of the feature variances, and equivalently the sum of the PCA eigenvalues.

### Principal components and eigenvectors

A direction vector $w$ has unit length. In two dimensions, if $w=(a,b)$, then $a^2+b^2=1$. The coordinate or score of a centered observation along that direction is

$$z = w^T x_c = ax_{1,c}+bx_{2,c}.$$

The first principal component is the direction with maximum projected variance. Each later component is perpendicular to the previous components and captures the greatest remaining variance. The eigenvalue equation is

$$S w = \lambda w.$$

- $w$ is an eigenvector and gives component direction/loadings.
- $\lambda$ is the variance captured by that component.
- Components are ordered from largest to smallest eigenvalue.
- The sign of an eigenvector is arbitrary: flipping every loading and score sign describes the same axis.

### Variance retention

For component $k$,

$$\text{explained fraction}_k = \frac{\lambda_k}{\sum_j\lambda_j}.$$

For the first $K$ components,

$$\text{cumulative retention}_K = \frac{\sum_{k=1}^{K}\lambda_k}{\sum_j\lambda_j}.$$

Choose the number of components based on the required information retention and the domain cost of losing detail. A 90% rule is a practical criterion, not a universal law.

### Standardization before PCA

If features have different units or scales, a large-unit feature can dominate variance. Standardize when each feature should contribute comparably. For HW2B, use the sample standard deviation (`ddof=1`) before PCA. PCA then operates on the standardized feature matrix.

### Loadings, scores, eigenvalues, and reconstruction

- **Loadings:** coefficients in `pca.components_`; component directions shared by all records.
- **Scores:** rows returned by `pca.transform(X)`; each record's coordinates in component space.
- **Eigenvalues:** `pca.explained_variance_`; variance across all records along each component.
- **Explained variance ratios:** `pca.explained_variance_ratio_`; fractions used for retention decisions.
- **Reconstruction:** `pca.inverse_transform(scores)` maps reduced coordinates back to the original standardized feature space. Undo standardization to return to original units.

Interpret a loading by its sign and magnitude relative to other loadings in the same component. A high positive PC1 score indicates an observation aligned with positive PC1 loadings; it does not mean the observation has a high value for every original feature.

### PCA code workflow

```python
means = features.mean()
scales = features.std(ddof=1)
standardized = (features - means) / scales

pca = PCA(n_components=4, svd_solver="full")
pca.fit(standardized)
scores = pca.transform(standardized)
rebuilt_standardized = pca.inverse_transform(scores)
```

`fit` learns the directions from the training data. `transform` projects observations using those already-learned directions. New observations must be standardized with the saved training means and scales before transformation.

### HW2B facts to know

- The penguin PCA uses four standardized measurements: bill length, bill depth, flipper length, and body mass.
- Three components retain 97.29% of the variance, so three are sufficient for a 90% target in the homework.
- PC1 has strong contributions from bill length, flipper length, and body mass, with an opposing bill-depth contribution in the course result.
- Eigenvalues describe variation across all penguins; scores describe one penguin's location.
- Fewer retained components generally increase reconstruction error. High total variance retention does not guarantee equally accurate reconstruction for every individual feature.

## 8. Homework Reference Sheet

### HW1A

- Data: 342 complete penguins; `sex` and `body_mass_g`.
- Statistic: male mean minus female mean; also male minus female rate above 4,500 g.
- Method: independent, two-sided permutation test; 5,000 resamples; seed 7130.
- Main reasoning: choose a statistic that matches the decision, preserve group sizes, and interpret p-values under label exchangeability.

### HW1B

- Data: online shopping sessions; new/returning visitor, purchase Boolean, weekend.
- Data size: 12,245 sessions before excluding 85 `Other` visitor labels.
- Statistic: new purchase rate minus returning purchase rate.
- Method: 10,000 bootstrap replicates, with replacement, percentile interval.
- Compare ordinary resampling with weekend-preserving resampling.

### HW2A

- Data: 11,610 usable shopping sessions after excluding all-zero rows for cosine comparisons.
- Anchor: session 58.
- Features: administrative, informational, and product-related page durations.
- Tasks: three nearest sessions using raw and standardized Euclidean, Manhattan, cosine, and Jaccard comparisons.
- Main reasoning: metric choice and scaling can change the neighbor ranking.

### HW2B

- Data: 342 complete penguins and four measurements.
- Tasks: hand-center data, form covariance matrix, verify $Sw=\lambda w$, calculate a PC score, fit PCA, interpret loadings and scores, select components, and compare reconstruction.
- Main result: three components retain 97.29% of standardized variance.

## 9. Common Code-Reading Questions

When shown code, ask these questions in order:

1. What are the rows and what does each selected column mean?
2. Is the code computing a statistic, generating a null distribution, generating a bootstrap distribution, or measuring distance?
3. Is sampling with or without replacement? Are labels being permuted or values being resampled?
4. What is the subtraction order and therefore the meaning of the sign?
5. Is the data numeric, standardized numeric, or Boolean presence/absence?
6. Does a library function return distance or similarity? Does it include the anchor itself?
7. Which degrees-of-freedom convention is used for standard deviation?
8. Does the output describe one observation, all observations, or a component?

High-value code details include `.mean()` on a Boolean condition, `replace=True`, `np.quantile`, `1 - cosine distance`, `.drop(anchor)`, `ddof=0` versus `ddof=1`, `fit` versus `transform`, and `components_` versus `transform()` output.

## 10. One-Sheet Notes Checklist

The allowed sheet may contain formulas and notes but no worked problems. Compress these items rather than copying long explanations:

- Observational unit, population versus sample, group/outcome/context, and description versus causation.
- Mean, median, exceedance-rate, and upper-quartile differences; write the subtraction order.
- Permutation: no association, exchangeability, preserved structure, null distribution, p-value, two-sided extremeness, simulation floor.
- Bootstrap: empirical distribution, with replacement, replicate versus distribution, standard error, percentile CI.
- The one-line permutation/bootstrap distinction.
- Euclidean, Manhattan, cosine, and Jaccard formulas plus what each ignores.
- Standardization formula and the course conventions: HW2A `ddof=0`; HW2B `ddof=1`.
- PCA: covariance matrix, $Sw=\lambda w$, score $w^Tx_c$, variance ratio, cumulative retention.
- PCA vocabulary: loading, score, eigenvalue, `fit`, `transform`, `inverse_transform`.
- Code traps: Boolean mean, `replace=True`, self-distance, `1 - distance`, zero vectors, and `components_` versus scores.
- Interpretation sentence starters for p-values, confidence intervals, distances, similarities, and loadings.

## Final Self-Test

Before the exam, be able to answer these without opening the notebooks:

1. Why can a mean difference and an exceedance-rate difference tell different stories?
2. What exactly is randomized in a permutation test, and what must be preserved?
3. Why is a bootstrap sample drawn with replacement?
4. What does a 95% percentile bootstrap interval summarize?
5. Why can standardization change nearest neighbors?
6. How do cosine similarity and Jaccard similarity treat magnitude and absence?
7. Why is the anchor removed before ranking nearest neighbors?
8. What do eigenvectors, eigenvalues, loadings, and scores each represent?
9. Why should PCA use saved means and scales when transforming new data?
10. Why can a component retain high total variance while reconstructing one feature poorly?
