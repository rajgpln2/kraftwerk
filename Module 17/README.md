# Comparing Classifiers for Bank Telemarketing

**Hari Raghavendra | Practical Application III — Assignment 17.1**

[View the analysis notebook](Comparing_Classifiers.ipynb)

## The question

Can we help a bank decide which customers to call about a term deposit? I compared k-nearest neighbors, logistic regression, decision trees and support vector machines using the UCI Bank Marketing dataset.

## Data and approach

The dataset contains 41,188 records from a Portuguese bank. I removed 12 exact duplicates, kept `unknown` responses as a separate category, and accounted for customers who had never been contacted before. Call duration was excluded because it is only known after a call.

I first compared default models using seven customer-information fields, then added campaign history, economic indicators and planned contact details. All models used the same 80/20 train/test split. Tuning used three-fold cross-validation on a shared 12,000-row training subset, followed by refitting on the full training set.

Only 11.3% of test records resulted in a subscription. Since predicting “no” for everyone already gives 88.7% accuracy, I used **average precision (AP)** to choose the model. AP measures how well a model ranks likely subscribers across different cutoffs.

## Results

The tuned models with expanded features produced these test results:

| Model | Accuracy | Average precision | Subscriber recall |
|---|---:|---:|---:|
| Logistic regression | 89.9% | **0.451** | 21.2% |
| K-nearest neighbors | 90.0% | 0.437 | 23.7% |
| Decision tree | 90.0% | 0.444 | **27.6%** |
| Support vector machine | 90.0% | 0.399 | 20.9% |

**Logistic regression was the best choice based on cross-validation AP.** Its highest-ranked 20% of test records contained 64.2% of observed subscribers, suggesting that ranking could help focus a limited calling budget.

The decision tree found more subscribers at its default cutoff. Logistic regression identified 197 subscribers but missed 731, so its cutoff would need adjustment before using it to make call/no-call decisions. Customers with a successful previous campaign outcome also showed higher subscription rates in the exploratory analysis.

## Recommendations

- Test a ranked calling list against the bank’s current approach in a small pilot.
- Choose the cutoff based on call costs and the value of subscriptions, rather than accuracy alone.
- Check performance on newer campaigns before using these historical results operationally.

## Project files

- [Comparing_Classifiers.ipynb](Comparing_Classifiers.ipynb) — analysis, charts, model comparisons and findings.
- `data/` — dataset and field descriptions.
- `results/` — detailed scores, tuning results and coefficients.
- [CRISP-DM-BANK.pdf](CRISP-DM-BANK.pdf) — background paper supplied with the assignment.
- `requirements.txt` — Python dependencies.

## Source

[UCI Bank Marketing dataset](https://archive.ics.uci.edu/dataset/222/bank+marketing). Moro, S., Cortez, P., and Rita, P. (2014). *A Data-Driven Approach to Predict the Success of Bank Telemarketing*. [Article DOI](https://doi.org/10.1016/j.dss.2014.03.001).
