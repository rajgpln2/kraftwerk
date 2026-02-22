# What Drives the Price of a Used Car? (CRISP-DM Report)

## 1) Business Understanding (Goal + Success Criteria)

**Client:** Used car dealership
**Business question:** *Which vehicle attributes are most strongly associated with higher/lower used-car prices, and how should inventory strategy change based on those signals?*

**Data-mining goal:** Predict (log) vehicle price using vehicle attributes (year, mileage, drivetrain, fuel, title status, condition, etc.) and interpret the drivers to produce actionable recommendations. 

**Success criteria:**

* A model with reasonable generalization performance (holdout test set).
* Clear, interpretable takeaways for non-technical stakeholders (dealers).
* Transparent data cleaning decisions and known limitations. 

-----------------------------------------------------------------------------------------------------

## 2) Data Understanding (Dataset + Data Quality)

**Source:** The Kaggle used-car listings file sample -> (426,880 rows; 18 columns).
Key columns include: `price`, `year`, `odometer`, `manufacturer`, `condition`, `fuel`, `drive`, `type`, `title_status`, `transmission`, `state`, etc.

### Data quality notes (important)

Several columns have substantial missing information:

* `size` ~72% missing
* `cylinders` ~42% missing
* `condition` ~41% missing
* `drive` and `paint_color` ~31% missing
* `type` ~22% missing

`price` also contains **extreme outliers** (including zeros and unrealistic values), so filtering is required before modeling.

(These checks align with CRISP-DM’s “Verify Data Quality” expectation.) 

-----------------------------------------------------------------------------------------------------

## 3) Data Preparation (Cleaning + Feature Choices)

### Cleaning rules (to improve realism + stability)

To reduce noise/outliers and reflect typical dealership pricing:

* Kept rows with **$500 ≤ price ≤ $200,000**
* Kept rows with **1990 ≤ year ≤ 2022**
* Kept rows with **0 ≤ odometer ≤ 500,000** (or missing)

### Modeling target transformation

* Modeled **log(price + 1)** to reduce skew and stabilize variance.

### Features used

Dropped very high-cardinality or non-informative identifiers:

* Dropped: `id`, `VIN`, `region`, `model`
* Used: `year`, `odometer`, `manufacturer`, `condition`, `cylinders`, `fuel`, `title_status`, `transmission`, `drive`, `size`, `type`, `paint_color`, `state`

Missing values were imputed (median for numeric; most-frequent for categorical) and categoricals were one-hot encoded.

(These steps correspond to CRISP-DM “Clean Data / Construct Data / Format Data.”) 

-----------------------------------------------------------------------------------------------------

## 4) Exploratory Findings (Dealer-Relevant Patterns)

Below are **median price** patterns from the cleaned dataset (directionally useful; not causal):

### Strong “value” signals

* **Newer vehicles command materially higher prices.**
  Median price by age bucket (approx):

  * 0–1 years: ~$35.6k
  * 2–3 years: ~$34.0k
  * 4–5 years: ~$28.0k
  * 6–8 years: ~$19.0k
  * 9–12 years: ~$12.0k

* **Lower mileage matters:** prices drop steadily as mileage increases.

* **Drive type:**
  Median price ranks roughly **4WD > RWD > FWD** (4WD has a meaningful premium).

* **Fuel type:**
  Median price ranks roughly **diesel > electric > gas/hybrid** in this dataset (diesel is notably higher).

* **Vehicle type:**
  Median price ranks roughly **pickup/truck > coupe > SUV > sedan/hatchback**.

These patterns motivated the modeling approach and interpretation. 

-----------------------------------------------------------------------------------------------------

## 5) Modeling (Multiple Regression Models + Tuning)

CRISP-DM recommends trying multiple techniques and calibrating parameters where relevant. 

### Train/test design

* Random 80/20 split (holdout test set).
* Primary metric on holdout: **RMSE on log(price)** (also tracked MAE and R²).

### Model A — OLS Linear Regression (One-hot encoded features)

**Holdout performance:**

* RMSE (log): **0.569**
* MAE (log): **0.366**
* R²: **0.602**

This was the best-performing model in this run and is also interpretable.

### Model B — Ridge Regression (L2 regularization) + small grid search

Performed a small **grid search over alpha** on a sampled training subset (to keep runtime manageable on a large dataset), then refit the best alpha on the full training set.

**Selected alpha:** 10.0
**Holdout performance:**

* RMSE (log): **0.755**
* MAE (log): **0.549**
* R²: **0.299**

Ridge underperformed OLS here, suggesting the OLS fit benefited from the wide feature set without needing strong shrinkage (given our preprocessing and the dataset scale).

-----------------------------------------------------------------------------------------------------

## 6) Model Interpretation (What Drives Price?)

Because the target is **log(price)**, coefficients can be interpreted approximately as % changes:

* Approx % change ≈ exp(coef) − 1

### Biggest interpretable drivers (directional)

From the OLS model:

**(A) Continuous drivers**

* **Year:** +0.072 per year ⇒ about **+7.5% price per 1 model-year newer** (all else equal).
* **Odometer:** −3.53e−6 per mile ⇒ about **−3.5% per +10,000 miles** (all else equal).

**(B) Categorical drivers (examples)**
Positive associations (higher price), relative to the baseline category:

* **Diesel fuel:** ~**+29%** vs baseline fuel category
* **Clean title:** ~**+6.6%**
* **RWD / 4WD:** meaningful premiums vs FWD
* **Pickups / trucks:** premiums vs sedans and smaller body types
* **“Excellent” condition:** premium vs lower-condition categories

Negative associations (lower price):

* **Sedans:** ~**−20.6%** vs baseline type category
* **FWD:** ~**−17.8%** vs baseline drivetrain
* **4-cylinder:** negative vs higher-cylinder categories (directionally consistent with lower-performing trims)

> Note: Coefficients are *conditional on other variables* and depend on the dataset’s category baselines. They should be used as guidance for inventory strategy, not as absolute pricing rules.

(Interpreting and documenting model meaning aligns with CRISP-DM “Model Descriptions / Assess Model.”) 

-----------------------------------------------------------------------------------------------------

## 7) Evaluation (Business & Limitations)

### What this means for a dealership

The analysis supports a practical pricing and sourcing narrative:

1. **Age and mileage dominate value.**
   Newer inventory with controlled mileage will move the dealership’s average selling price materially.

2. **Inventory with drivetrain capability carries a premium.**
   4WD and (to a lesser extent) RWD listings tend to price higher than FWD, even after controlling for other attributes.

3. **Body type mix matters.**
   Trucks/pickups command a strong premium; sedans lag, holding other factors constant.

4. **Title status and condition are “table stakes.”**
   Clean-title and higher-condition vehicles predictably price higher.

### Known limitations / risks

* Many fields have missing values (e.g., size, cylinders, condition), which can bias interpretation.
* Data is listings-based; it may reflect regional mix, listing behavior, or selection bias.
* Extremely high-end brands (e.g., Ferrari) can skew “manufacturer” medians; treat as niche segments.
* This is associative modeling, not causal inference.

(Reviewing business fit and risks is a CRISP-DM expectation in Evaluation.) 

-----------------------------------------------------------------------------------------------------

## 8) Recommendations + Next Steps

CRISP-DM notes that deployment may be as simple as a report, but should include recommendations and how results will be used/monitored. 

### Actionable recommendations for the dealership

**Inventory sourcing**

* Prioritize **0–5 year old** vehicles where possible; the price drop after ~6–8 years is substantial.
* Target **lower mileage** units (especially under common financing thresholds), because mileage has a consistent penalty.
* Maintain a healthy mix of **4WD / truck / pickup** inventory where local demand supports it.

**Pricing & merchandising**

* Use a pricing playbook that explicitly adjusts for:

  * model year (strong positive lift)
  * mileage (consistent negative lift)
  * drivetrain (4WD premium)
  * title status and condition (clean/excellent premium)
* Emphasize “value drivers” in listings: clean title, condition grade, drivetrain, and service history.

**Next steps**

* Add richer features if available (trim, engine size, accident history, options/packages).
* Build a regional model per state/market to reduce geographic confounding.
* Track model performance over time and refresh periodically as market conditions shift. 

-----------------------------------------------------------------------------------------------------

