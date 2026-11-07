### What the results say
- **Logistic regression** was selected by training cross-validation, with mean AP **0.461** on the shared tuning subset. Its full-training refit achieved holdout AP **0.451**, compared with prevalence **0.113**; the conditional bootstrap 95% interval is **0.421–0.485**.
- At its standard decision rule, precision is **66.1%** and recall is **21.2%**. It identifies **197** subscribers, misses **731**, and flags **101** non-subscribers. Ranking quality and a useful yes/no cutoff are different questions.
- The highest-ranked **1,648** records (20% of holdout) contain **596** subscribers: **36.2%** response concentration, **3.21×** the holdout prevalence, capturing **64.2%** of observed subscribers. This is a retrospective prioritization result, not a promised campaign conversion rate.
- Client-only default models have limited information. The expanded tuned comparison adds history, economic conditions and planned contact context; changes cannot be credited to hyperparameter tuning alone.
- Prior successful contact is associated with higher subscription rates in training data. This is a candidate for controlled testing, not proof that repeated calls cause subscriptions. Small groups and correlated predictors need cautious interpretation.

### Recommended next steps
1. Pilot a ranked contact list at a defined call budget and compare against the existing campaign policy using a randomized eligible-contact test.
2. Measure net deposit value, agent time, opt-outs and customer burden; choose the cutoff using those costs on validation data rather than optimizing accuracy alone.
3. Obtain timestamps and customer/campaign identifiers for temporal and group-separated validation. Reassess using recent data before deployment; these records are from 2008–2010.
4. Verify planned-contact inputs are available before scoring. Calibrate probabilities if operational decisions require probability estimates.
5. Check stability, subgroup performance, consent and contact-frequency limits before using customer attributes for targeting.

### Limits
No causal effect, profitability, future performance or deployment readiness is established. The fixed random split, historical data, potential repeat contacts, limited tuning grid and 12,000-row tuning subset constrain the comparison. Test-set differences alone do not establish statistical superiority.
