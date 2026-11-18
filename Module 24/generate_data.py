"""Reproducible fictional display-lamination process. No factory data are used."""
from pathlib import Path
import argparse
import hashlib
import json
import numpy as np
import pandas as pd

SEED = 20261106
N_DAYS = 100
TOOLS = [f'LAM-{i:02d}' for i in range(1, 7)]
UNITS_PER_LOT = 50
CATEGORICAL_FEATURES = ['tool_id', 'product_type']
NUMERIC_FEATURES = [
    'incoming_oca_delta_um', 'incoming_oca_sd_um', 'glass_bow_um',
    'precheck_temperature_c', 'precheck_pressure_mpa', 'precheck_vacuum_pa_abs',
    'precheck_roller_force_n', 'recipe_speed_mm_s', 'recipe_dwell_s',
    'ambient_humidity_pct', 'cycles_since_maintenance', 'tool_operating_hours',
    'historical_mean_delta_um', 'historical_oos_rate', 'history_count',
    'history_age_hours', 'days_since_start',
]
FEATURES = CATEGORICAL_FEATURES + NUMERIC_FEATURES
TARGET = 'lot_bondline_oos'


def generate(seed=SEED):
    rng = np.random.default_rng(seed)
    lot_rows, unit_frames, maintenance = [], [], []
    tool_bias = np.array([-1.8, 0.9, -0.6, 1.7, -1.0, 0.5])
    pressure_bias = rng.normal(0, 0.006, 6)
    drift = np.zeros(6)
    wear_days = np.zeros(6, dtype=int)
    operating_hours = 1200.0 + 180 * np.arange(6)
    start = pd.Timestamp('2026-01-05T06:00:00Z')
    for day in range(N_DAYS):
        for tool_index, tool in enumerate(TOOLS):
            decision = start + pd.Timedelta(days=day, minutes=90 * tool_index)
            lot_id = f'LOT-{day * 6 + tool_index + 1:04d}'
            # Fixed schedules and a small persistent drift remain after maintenance.
            interval = [19, 21, 20, 23, 18, 22][tool_index]
            if day > 0 and wear_days[tool_index] >= interval:
                maintenance.append(dict(tool_id=tool, maintenance_time_utc=decision-pd.Timedelta(hours=2),
                                        maintenance_type='scheduled_clean_and_calibrate',
                                        cycles_before_maintenance=int(wear_days[tool_index] * UNITS_PER_LOT)))
                wear_days[tool_index] = 0
                drift[tool_index] *= 0.2
            drift[tool_index] = 0.88 * drift[tool_index] + rng.normal(0, 0.35)
            wear = wear_days[tool_index] / interval
            product = rng.choice(['P150', 'P175'], p=[0.65, 0.35])
            nominal = 150.0 if product == 'P150' else 175.0
            target = nominal - 8.0
            material_shift = rng.normal(0, 3.0) + 1.8 * np.sin(day / 8)
            # Material supply change late in the run creates a distribution shift.
            material_shift += 1.7 if day >= 72 else 0.0
            incoming_actual = nominal + material_shift
            incoming_measured = incoming_actual + rng.normal(0, 0.45)
            incoming_sd = rng.uniform(0.6, 1.7)
            bow = np.clip(rng.normal(12, 4), 1, 28)
            temp = np.clip(30 + 1.8*np.sin(day/10) + rng.normal(0, 1.7) + 2*wear, 23, 42)
            pressure = np.clip(0.15 + pressure_bias[tool_index] - 0.014*wear + rng.normal(0, 0.012), 0.09, 0.22)
            vacuum = np.clip(20 + 32*wear + rng.lognormal(1.4, 0.5), 5, 100)
            force = np.clip(300 + 800*(pressure-0.15) + rng.normal(0, 16), 210, 390)
            speed = np.clip(rng.normal(14, 2.3), 8, 22)
            dwell = np.clip(12 + (14-speed)*0.35 + rng.normal(0, 1), 7, 18)
            humidity = np.clip(45 + 7*np.sin(day/12) + rng.normal(0, 3), 25, 65)
            # Nonlinear viscoelastic surrogate, in um. Coefficients are assumptions.
            delta = (0.88*material_shift - 125*(pressure-0.15) - 0.60*(temp-30)
                     - 0.018*(force-300) + 0.22*(speed-14) - 0.20*(dwell-12)
                     + 0.045*max(vacuum-35, 0) + 0.09*(bow-12)
                     + 4.7*wear**1.6 + tool_bias[tool_index] + drift[tool_index]
                     - 12*(pressure-0.15)*(temp-30) + rng.normal(0, 1.4))
            # Unobserved within-lot shocks keep prediction imperfect.
            shock = rng.normal(0, 3.0) if rng.random() < 0.04 else 0.0
            unit_mean = target + delta + shock + rng.normal(0, incoming_sd, UNITS_PER_LOT)
            position = np.arange(UNITS_PER_LOT)
            unit_mean += 0.7*(position / 49 - 0.5) * wear
            spatial_gradient = (bow/18 + max(vacuum-30, 0)*0.015) * np.array([-1, -0.5, 0, 0.5, 1])
            sites = unit_mean[:, None] + spatial_gradient + rng.normal(0, 0.32, (UNITS_PER_LOT, 5))
            site_cols = [f'bondline_site_{i}_um' for i in range(1, 6)]
            units = pd.DataFrame(np.round(sites, 4), columns=site_cols)
            units['unit_mean_bondline_um'] = units[site_cols].mean(axis=1).round(4)
            units['unit_uniformity_range_um'] = (units[site_cols].max(axis=1)-units[site_cols].min(axis=1)).round(4)
            units.insert(0, 'unit_id', [f'{lot_id}-U{i:02d}' for i in range(1, 51)])
            units.insert(1, 'lot_id', lot_id)
            units.insert(2, 'tool_id', tool)
            units.insert(3, 'product_type', product)
            units['production_time_utc'] = [decision+pd.Timedelta(minutes=int(i)+1) for i in position]
            units['run_temperature_c'] = np.round(temp + rng.normal(0, 0.35, 50), 4)
            units['run_pressure_mpa'] = np.round(pressure + rng.normal(0, 0.002, 50), 6)
            units['run_vacuum_pa_abs'] = np.round(np.maximum(1, vacuum+rng.normal(0, 2, 50)), 4)
            units['run_roller_force_n'] = np.round(force+rng.normal(0, 3, 50), 4)
            units['run_cycle_time_s'] = np.round(dwell + 180/speed + rng.normal(0, 0.4, 50), 4)
            units['bubble_count'] = rng.poisson(0.04 + 0.012*max(vacuum-30, 0), 50)
            units['is_synthetic'] = True
            measured_mean = float(units['unit_mean_bondline_um'].mean())
            release = decision + pd.Timedelta(minutes=170)
            units['metrology_available_at_utc'] = release
            lower, upper = target-7.5, target+7.5
            oos = int(measured_mean < lower or measured_mean > upper)
            # Released past lots only. Same-tool last-three normalized thickness history.
            past = [row for row in lot_rows if row['tool_id'] == tool and row['metrology_available_at_utc'] < decision][-3:]
            history_delta = np.mean([row['lot_mean_bondline_um']-row['target_bondline_um'] for row in past]) if past else np.nan
            history_oos = np.mean([row[TARGET] for row in past]) if past else np.nan
            row = dict(lot_id=lot_id, tool_id=tool, product_type=product,
                       prediction_time_utc=decision, precheck_time_utc=decision-pd.Timedelta(minutes=5),
                       metrology_available_at_utc=release, days_since_start=day,
                       n_units=50, incoming_oca_nominal_um=nominal,
                       incoming_oca_mean_um=incoming_measured,
                       incoming_oca_delta_um=incoming_measured-nominal,
                       incoming_oca_sd_um=incoming_sd, glass_bow_um=bow,
                       precheck_temperature_c=temp+rng.normal(0, 0.20),
                       precheck_pressure_mpa=pressure+rng.normal(0, 0.001),
                       precheck_vacuum_pa_abs=vacuum+rng.normal(0, 1),
                       precheck_roller_force_n=force+rng.normal(0, 2),
                       recipe_speed_mm_s=speed, recipe_dwell_s=dwell,
                       ambient_humidity_pct=humidity,
                       cycles_since_maintenance=int(wear_days[tool_index]*50),
                       tool_operating_hours=operating_hours[tool_index],
                       historical_mean_delta_um=history_delta, historical_oos_rate=history_oos,
                       history_count=len(past),
                       history_age_hours=(decision-past[-1]['metrology_available_at_utc']).total_seconds()/3600 if past else np.nan,
                       history_latest_available_at_utc=past[-1]['metrology_available_at_utc'] if past else pd.NaT,
                       target_bondline_um=target, spec_lower_um=lower, spec_upper_um=upper,
                       lot_mean_bondline_um=measured_mean, lot_bondline_oos=oos, is_synthetic=True)
            lot_rows.append(row)
            unit_frames.append(units)
            wear_days[tool_index] += 1
            operating_hours[tool_index] += units['run_cycle_time_s'].sum() / 3600
    lots = pd.DataFrame(lot_rows)
    # Random pre-decision sensor dropouts. Missingness does not depend on the target.
    for column in ['precheck_temperature_c', 'precheck_vacuum_pa_abs', 'precheck_roller_force_n', 'ambient_humidity_pct']:
        lots.loc[rng.random(len(lots)) < 0.012, column] = np.nan
    # Keep serialized and in-memory precision identical for reproducible label checks.
    lots = lots.round(6)
    return pd.concat(unit_frames, ignore_index=True), lots, pd.DataFrame(maintenance)


def write_dataset(output_dir, seed=SEED):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    units, lots, maintenance = generate(seed)
    frames = {'lamination_units.csv': units, 'lamination_lots.csv': lots,
              'maintenance_events.csv': maintenance}
    hashes = {}
    for name, frame in frames.items():
        path = output_dir / name
        frame.to_csv(path, index=False, float_format='%.6f', date_format='%Y-%m-%dT%H:%M:%SZ')
        hashes[name] = hashlib.sha256(path.read_bytes()).hexdigest()
    manifest = dict(seed=seed, unit_records=len(units), lots=len(lots), tools=len(TOOLS),
                    units_per_lot=UNITS_PER_LOT, days=N_DAYS,
                    synthetic=True, target=TARGET, prediction_features=FEATURES,
                    sha256=hashes)
    (output_dir/'manifest.json').write_text(json.dumps(manifest, indent=2)+'\n')
    return manifest


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir', type=Path, default=Path(__file__).resolve().parent/'data')
    parser.add_argument('--seed', type=int, default=SEED)
    args = parser.parse_args()
    print(json.dumps(write_dataset(args.output_dir, args.seed), indent=2))
