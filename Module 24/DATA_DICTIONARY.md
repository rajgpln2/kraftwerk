# Data dictionary

All observations are synthetic. Blank numeric fields represent missing measurements. UTC timestamps use ISO 8601. All retained floats have six decimal places in CSV, with four-decimal metrology sites.

The model uses exactly the 20 pre-lot features identified below. Run signals and inspection outcomes are excluded from predictors. Known product design limits support label construction and EDA. IDs and audit timestamps support joins and timing checks.

## Files

| File | Rows | Grain |
|---|---|---|
| lamination_units.csv | 30,000 | One production unit with five metrology sites |
| lamination_lots.csv | 600 | One pre-lot decision with later lot outcome |
| maintenance_events.csv | 26 | One scheduled maintenance event |

## Fields

### lamination_lots.csv

| Field | Unit | Role | Meaning |
|---|---|---|---|
| `lot_id` | identifier | Audit or design metadata | Lot identifier. Fifty units share each lot |
| `tool_id` | category | Pre-lot predictor | Fictional lamination tool LAM-01 through LAM-06 |
| `product_type` | category | Pre-lot predictor | P150 or P175, indicating the nominal incoming adhesive thickness |
| `prediction_time_utc` | UTC timestamp | Audit or design metadata | Lot decision time immediately before production starts |
| `precheck_time_utc` | UTC timestamp | Audit or design metadata | Stabilization-check timestamp, five minutes before the lot decision |
| `metrology_available_at_utc` | UTC timestamp | Audit or design metadata | Inspection release timestamp, 170 minutes after lot decision |
| `days_since_start` | days | Pre-lot predictor | Elapsed integer simulation day, 0 through 99 |
| `n_units` | units | Audit or design metadata | Number of units in the lot, fixed at 50 |
| `incoming_oca_nominal_um` | µm | Audit or design metadata | Design nominal incoming optical clear adhesive film thickness |
| `incoming_oca_mean_um` | µm | Audit or design metadata | Incoming lot sample thickness estimate, available before production |
| `incoming_oca_delta_um` | µm | Pre-lot predictor | Measured incoming film thickness minus its product nominal |
| `incoming_oca_sd_um` | µm | Pre-lot predictor | Incoming material thickness standard deviation available from inspection |
| `glass_bow_um` | µm | Pre-lot predictor | Incoming glass peak bow measurement |
| `precheck_temperature_c` | °C | Pre-lot predictor | Pre-lot stabilization temperature with sensor noise |
| `precheck_pressure_mpa` | MPa | Pre-lot predictor | Pre-lot applied lamination pressure with sensor noise |
| `precheck_vacuum_pa_abs` | Pa absolute | Pre-lot predictor | Pre-lot chamber absolute pressure. Larger values mean poorer vacuum |
| `precheck_roller_force_n` | N | Pre-lot predictor | Pre-lot roller force with sensor noise. Correlated with applied pressure |
| `recipe_speed_mm_s` | mm/s | Pre-lot predictor | Planned roller motion speed known before production |
| `recipe_dwell_s` | seconds | Pre-lot predictor | Planned dwell duration known before production |
| `ambient_humidity_pct` | % RH | Pre-lot predictor | Pre-lot ambient relative humidity |
| `cycles_since_maintenance` | units | Pre-lot predictor | Completed production units since last scheduled maintenance |
| `tool_operating_hours` | hours | Pre-lot predictor | Cumulative tool cycle operating hours including fictional prehistory |
| `historical_mean_delta_um` | µm | Pre-lot predictor | Mean normalized thickness of at most three latest released same-tool lots |
| `historical_oos_rate` | fraction | Pre-lot predictor | Out-of-spec fraction among at most three latest released same-tool lots |
| `history_count` | lots | Pre-lot predictor | Number of available prior same-tool lots, 0 through 3 |
| `history_age_hours` | hours | Pre-lot predictor | Age of the latest historical inspection release at current decision time |
| `history_latest_available_at_utc` | UTC timestamp | Audit or design metadata | Latest inspection release used in the historical features |
| `target_bondline_um` | µm | Audit or design metadata | Product bondline design center. 142 for P150 and 167 for P175 |
| `spec_lower_um` | µm | Audit or design metadata | Lot-mean lower limit, design center minus 7.5 µm |
| `spec_upper_um` | µm | Audit or design metadata | Lot-mean upper limit, design center plus 7.5 µm |
| `lot_mean_bondline_um` | µm | Post-production inspection | Observed mean of fifty per-unit five-site thickness means |
| `lot_bondline_oos` | binary | Target | Primary target. 1 when measured lot mean is strictly outside product limits |
| `is_synthetic` | boolean | Audit or design metadata | Always true. Explicit record-level synthetic-data disclosure |

### lamination_units.csv

| Field | Unit | Role | Meaning |
|---|---|---|---|
| `unit_id` | identifier | Audit or design metadata | Unique unit identifier |
| `lot_id` | identifier | Audit or design metadata | Lot identifier. Fifty units share each lot |
| `tool_id` | category | Audit or design metadata | Fictional lamination tool LAM-01 through LAM-06 |
| `product_type` | category | Audit or design metadata | P150 or P175, indicating the nominal incoming adhesive thickness |
| `bondline_site_1_um` | µm | Post-production inspection | Measured bondline thickness at spatial site 1, including 0.32 µm SD measurement noise |
| `bondline_site_2_um` | µm | Post-production inspection | Measured bondline thickness at spatial site 2, including 0.32 µm SD measurement noise |
| `bondline_site_3_um` | µm | Post-production inspection | Measured bondline thickness at spatial site 3, including 0.32 µm SD measurement noise |
| `bondline_site_4_um` | µm | Post-production inspection | Measured bondline thickness at spatial site 4, including 0.32 µm SD measurement noise |
| `bondline_site_5_um` | µm | Post-production inspection | Measured bondline thickness at spatial site 5, including 0.32 µm SD measurement noise |
| `unit_mean_bondline_um` | µm | Post-production inspection | Mean of five measured thickness sites on a unit |
| `unit_uniformity_range_um` | µm | Post-production inspection | Maximum minus minimum of five measured thickness sites on a unit |
| `production_time_utc` | UTC timestamp | Audit or design metadata | Unit production timestamp, one through fifty minutes after decision |
| `run_temperature_c` | °C | During-production signal | During-production unit temperature. Unavailable at the pre-lot decision |
| `run_pressure_mpa` | MPa | During-production signal | During-production applied pressure. Unavailable at the pre-lot decision |
| `run_vacuum_pa_abs` | Pa absolute | During-production signal | During-production chamber absolute pressure |
| `run_roller_force_n` | N | During-production signal | During-production roller force |
| `run_cycle_time_s` | seconds | During-production signal | During-production cycle duration, dwell plus 180 mm path divided by speed plus noise |
| `bubble_count` | count | Post-production inspection | Downstream bubble inspection count. Excluded from predictors |
| `is_synthetic` | boolean | Audit or design metadata | Always true. Explicit record-level synthetic-data disclosure |
| `metrology_available_at_utc` | UTC timestamp | Audit or design metadata | Inspection release timestamp, 170 minutes after lot decision |

### maintenance_events.csv

| Field | Unit | Role | Meaning |
|---|---|---|---|
| `tool_id` | category | Audit or design metadata | Fictional lamination tool LAM-01 through LAM-06 |
| `maintenance_time_utc` | UTC timestamp | Audit or design metadata | Scheduled maintenance completion, two hours before the next lot |
| `maintenance_type` | category | Audit or design metadata | Scheduled cleaning and calibration |
| `cycles_before_maintenance` | units | Audit or design metadata | Completed units before the scheduled maintenance reset |

## Missingness and history semantics

Four pre-lot measurement fields have independent 1.2% dropout probabilities. Each tool starts with no released history, creating six expected blank history records. History is calculated from the latest three inspection releases strictly earlier than the prediction time, and persists across maintenance to mirror an available measurement log. The notebook independently reconstructs these histories.

## Primary label

`lot_bondline_oos = int(lot_mean_bondline_um < spec_lower_um or lot_mean_bondline_um > spec_upper_um)`

Equality to either limit passes. Uniformity and bubble observations do not enter the label. A passing lot mean does not establish conformance of every unit or metrology site.
