# Quality-Linked Predictive Maintenance for Display Lamination

**Author:** Hari Raghavendra  
**Assignment:** Module 20.1 — Initial Report and Exploratory Data Analysis

## Executive summary

This project explores whether lamination process readings and equipment-health signals can help flag an out-of-specification bondline thickness (BLT) on the next production cycle. The initial analysis includes data-quality checks, exploratory plots, feature engineering and a logistic-regression baseline.

The notebook uses **synthetic data generated for this project**, because measured factory telemetry was not provided. All results below describe that demonstration. They do not establish actual equipment performance, approved process limits or maintenance savings.

The model detected 24 of 67 next-cycle BLT excursions in the chronological test set, while generating 46 false alarms. The workflow runs successfully, but the model would need substantial improvement and validation before it could support production decisions.

## Rationale

Lamination equipment can continue running while its process performance gradually changes. If equipment-health signals can provide an early warning of quality loss, engineers may be able to investigate before more material is affected. This project tests an initial approach to that question using BLT compliance as the quality outcome.

Predicting a BLT excursion is a quality-risk task. Establishing that an excursion indicates equipment degradation, or that maintenance would prevent it, requires additional maintenance and production records.

## Research Question

**Can lamination-process and equipment-health measurements available at the end of cycle t predict whether the BLT on cycle t+1 will fall outside specification?**

The target, `next_blt_out_of_spec`, is 1 when the next cycle on the same tool is out of specification and 0 when it is within specification. This project does not predict equipment breakdown time or remaining useful life.

## Data Sources

The notebook generates 2,150 fictional cycles across five tools using a fixed random seed of 42. Each tool has 430 observations at 15-minute intervals, covering January 1–5, 2026. These timestamps and operating values are illustrative.

| Data category | Variables |
|---|---|
| Record identifiers | Timestamp, tool ID |
| Process readings | Roller force, roller speed, sheet tension, vacuum |
| Equipment-health indicators | Motor current, temperature, vibration, cycle time, cycles since preventive maintenance |
| Quality measurement | Current-cycle BLT, used to construct the next-cycle outcome |

The example BLT specification band is **95–105 µm**, inclusive. This is a fictional demonstration band, not an approved engineering specification. Relationships between drift, sensor readings and BLT are programmed into the generator.

The notebook can alternatively read `data/lamination_telemetry.csv`. Any real-data use requires a compatible schema, verified measurement timing and appropriate recipe-specific specifications.

## Methodology

1. **Audit and clean the data:** check required columns, convert timestamps and numerical fields, inspect missing values and remove records with missing identifiers or duplicate tool/timestamp keys.
2. **Review potential outliers:** flag measurements outside the 1.5×IQR bounds. Retain them for analysis because extreme readings may contain useful warning signals.
3. **Create the next-cycle target:** sort observations within each tool and shift the BLT compliance outcome forward one cycle. Exclude observations without a known next-cycle label.
4. **Explore the data:** compare outcomes by tool, plot roller-force distributions and vibration box plots, examine force versus motor current, and inspect rolling event frequency over time.
5. **Engineer features:** calculate force deviation from a reference, five-cycle rolling sensor averages and rolling force variability. These features use current and preceding observations only.
6. **Split chronologically:** use earlier observations for training and the most recent portion for testing. Purge training rows whose next-cycle label crosses the test boundary.
7. **Fit a baseline:** use logistic regression with balanced class weights, training-only median imputation and standardization, and one-hot encoding of tool ID. Evaluate predictions at a fixed 0.50 threshold.

Tools used: Python, NumPy, pandas, Seaborn, Matplotlib and scikit-learn.

## Results

### Data quality and exploratory findings

| Check | Synthetic-data result |
|---|---:|
| Generated observations | 2,150 |
| Missing raw values | 0 |
| Duplicate tool/timestamp records | 0 |
| Usable next-cycle labels | 2,145 |
| Next-cycle within-spec outcomes | 1,661 |
| Next-cycle out-of-spec outcomes | 484 — 22.6% |

The final observation from each of the five tools has no next-cycle outcome and is excluded. No raw records required removal for missing identifiers or duplicates. The imputation pipeline remains in place for missing predictor values, including the first rolling-standard-deviation value for each tool.

The outlier check flagged 20 roller-force readings, 19 roller-speed readings, 5 motor-current readings and 20 cycle-time readings; it flagged no vibration readings. These are counts per variable and may overlap across records. They are review flags, not confirmed sensor faults.

The simulated next-cycle excursion rate varies by tool:

| Fictional tool | Labeled cycles | Excursions | Excursion rate |
|---|---:|---:|---:|
| DEMO-LAM-01 | 429 | 77 | 17.9% |
| DEMO-LAM-02 | 429 | 79 | 18.4% |
| DEMO-LAM-03 | 429 | 89 | 20.7% |
| DEMO-LAM-04 | 429 | 104 | 24.2% |
| DEMO-LAM-05 | 429 | 135 | 31.5% |

The plots show lower force and higher vibration tending to precede excursions, with substantial overlap between the outcome groups. This overlap suggests that a single sensor threshold would not cleanly separate the groups. Tool differences and sensor associations reflect the generator's assumptions and need testing against measured data.

### Baseline model evaluation

The chronological split produces 1,710 training observations and 430 test observations, with 5 additional labeled observations purged at the boundary. The test period starts January 4, 2026 at 13:45. Event prevalence is 24.4% in training and 15.6% in testing, showing that the outcome mix changes over time even in this example.

| Test metric | Result |
|---|---:|
| Precision | 34.3% |
| Recall | 35.8% |
| F1 score | 35.0% |
| Balanced accuracy | 61.6% |
| Average precision | 34.6% |
| ROC-AUC | 72.7% |
| Accuracy | 79.3% |
| Test event prevalence | 15.6% |

Average precision summarizes the precision–recall curve using scikit-learn's `average_precision_score`; it is not a trapezoidal area calculation.

| Actual outcome | Predicted within spec | Predicted out of spec |
|---|---:|---:|
| Within spec | 317 | 46 |
| Out of spec | 43 | 24 |

**Interpretation:** Of 70 alerts, 24 corresponded to an excursion and 46 were false alarms. The model caught 35.8% of the 67 actual excursions and missed 64.2%.

Recall matters because missed excursions could allow additional quality loss. Precision matters because false alarms create investigation burden. F1 summarizes their balance, while average precision evaluates ranking across thresholds. Average precision exceeds the 15.6% event-prevalence reference, indicating useful ranking within this synthetic example.

Accuracy alone would be misleading: always predicting “within spec” achieves 84.4% accuracy on this test set but detects no excursions. The model's lower accuracy does not by itself settle whether its alerts are useful; that requires a measured trade-off between missed events and false alarms.

## Next steps

1. Confirm that synthetic demonstration data meets the assignment's data requirements.
2. Obtain suitable measured telemetry joined to BLT results by tool and cycle, with recipe, material lot and maintenance context.
3. Verify the prediction timeline and approved BLT limits before modeling real outcomes.
4. Remove the redundant pair of raw roller force and force deviation from the model feature list, then rerun the analysis. For a constant setpoint, these contain the same information and complicate coefficient interpretation.
5. Use a separate chronological validation period to compare models and tune the alert threshold without using the final test set for selection.
6. Compare against simple process-monitoring rules and assess performance across additional periods, tools and recipes.
7. Evaluate alerts in shadow mode and measure investigation burden, warning time and quality impact before recommending maintenance actions.

## Outline of project

- [Module 20 notebook: EDA and baseline model](Module20_Lamination_EDA_Baseline.ipynb)
- `README.md` — project summary and verified demonstration findings.
- `data/lamination_telemetry.csv` — optional input; not required to reproduce the synthetic run.

### Running the analysis

Save the notebook as `Module20_Lamination_EDA_Baseline.ipynb` beside this README so the relative link works. Install the dependencies:

```bash
python -m pip install numpy pandas seaborn matplotlib scikit-learn jupyter
```

Open the notebook in Jupyter and run all cells from top to bottom. If the optional CSV is absent, the notebook generates the synthetic dataset automatically. Results above correspond to that synthetic run at the 0.50 decision threshold; results must be updated if the data or model changes.

## Contact and Further Information

**Hari Raghavendra**  
Project repository: [rajgpln2/kraftwerk](https://github.com/rajgpln2/kraftwerk)

This report describes the verified notebook demonstration. It makes no claim of validated factory performance or demonstrated maintenance savings.
