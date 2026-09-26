"""Append actual, manually observed rolling-test results; never commands hardware."""
import argparse
import csv
import math
from datetime import datetime, timezone
from pathlib import Path

FIELDS = ['run_id', 'recorded_utc', 'mass_g', 'course_distance_m', 'elapsed_s',
          'average_speed_m_s', 'equivalent_wheel_rpm', 'target_speed_m_s',
          'direction', 'start_mode', 'surface', 'outcome', 'bus_voltage_v',
          'bus_current_a', 'motor_start_temp_c', 'motor_end_temp_c', 'notes']


def number(value, name, positive=False):
    result = float(value)
    if not math.isfinite(result) or (positive and result <= 0):
        raise ValueError(f'{name} must be finite'+(' and greater than zero' if positive else ''))
    return result


def result_row(args):
    mass = number(args.mass_g, 'mass', True)
    distance = number(args.distance_m, 'distance', True)
    target = number(args.target_m_s, 'target speed', True)
    elapsed = '' if args.elapsed_s is None else number(args.elapsed_s, 'elapsed time', True)
    if args.outcome == 'completed' and elapsed == '':
        raise ValueError('A completed run needs the observed elapsed time')
    if not args.run_id.strip():
        raise ValueError('run ID cannot be empty')
    # A failed/aborted attempt never gets the speed for the full course distance.
    speed = distance / elapsed if args.outcome == 'completed' else ''
    rpm = speed * 60 / (math.pi * 0.060) if speed != '' else ''
    row = dict(zip(FIELDS, [args.run_id.strip(), datetime.now(timezone.utc).isoformat(),
        mass, distance, elapsed, speed, rpm, target, args.direction, args.start_mode,
        args.surface, args.outcome, '', '', '', '', args.notes]))
    for key in ('bus_voltage_v', 'bus_current_a', 'motor_start_temp_c', 'motor_end_temp_c'):
        value = getattr(args, key)
        if value is not None:
            row[key] = number(value, key, key == 'bus_voltage_v')
    return row


def append(path, row):
    path = Path(path)
    exists = path.exists() and path.stat().st_size > 0
    if exists:
        with path.open(newline='') as f:
            reader = csv.DictReader(f)
            if reader.fieldnames != FIELDS:
                raise ValueError('CSV schema differs; choose another file or migrate it explicitly')
            if any(r['run_id'] == row['run_id'] for r in reader):
                raise ValueError('Run ID already exists; existing measurements were not changed')
    with path.open('a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        if not exists:
            writer.writeheader()
        writer.writerow(row)


def parser():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--file', type=Path, default=Path(__file__).with_name('runs.csv'))
    for field in ('run-id', 'mass-g', 'distance-m', 'target-m-s', 'surface'):
        p.add_argument('--'+field, required=True)
    p.add_argument('--elapsed-s')
    p.add_argument('--direction', required=True, choices=['forward', 'reverse'])
    p.add_argument('--start-mode', required=True, choices=['standing_start', 'flying_start'])
    p.add_argument('--outcome', required=True, choices=['completed', 'failed', 'aborted'])
    for field in ('bus-voltage-v', 'bus-current-a', 'motor-start-temp-c', 'motor-end-temp-c'):
        p.add_argument('--'+field)
    p.add_argument('--notes', default='')
    return p


if __name__ == '__main__':
    p = parser()
    args = p.parse_args()
    try:
        row = result_row(args)
        append(args.file, row)
    except (ValueError, OSError) as exc:
        p.error(str(exc))
    speed = row['average_speed_m_s']
    print(f"Saved {row['run_id']}: {row['outcome']}" +
          (f', {speed:.4f} m/s observed average' if speed != '' else ', no completed-course speed'))
