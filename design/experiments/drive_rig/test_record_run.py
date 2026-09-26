import csv
import math
import tempfile
import unittest
from pathlib import Path

from record_run import append, parser, result_row


class Measurements(unittest.TestCase):
    def args(self, **changes):
        a = parser().parse_args(['--run-id', 'synthetic-test-only', '--mass-g', '1000',
            '--distance-m', '2', '--target-m-s', '.2', '--surface', 'test',
            '--direction', 'forward', '--start-mode', 'standing_start',
            '--outcome', 'completed', '--elapsed-s', '10'])
        for key, value in changes.items():
            setattr(a, key, value)
        return a

    def test_units(self):
        row = result_row(self.args())
        self.assertAlmostEqual(row['average_speed_m_s'], 0.2)
        self.assertAlmostEqual(row['equivalent_wheel_rpm'], 200/math.pi)

    def test_failed_attempt_is_not_full_course_speed(self):
        for elapsed in (None, '5'):
            row = result_row(self.args(outcome='failed', elapsed_s=elapsed))
            self.assertEqual(row['average_speed_m_s'], '')

    def test_invalid_measurements(self):
        for key in ('mass_g', 'distance_m', 'target_m_s', 'elapsed_s'):
            for value in ('0', '-1', 'nan', 'inf'):
                with self.subTest(key=key, value=value), self.assertRaises(ValueError):
                    result_row(self.args(**{key: value}))
        with self.assertRaises(ValueError):
            result_row(self.args(elapsed_s=None))

    def test_preserves_records_and_quotes_notes(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d)/'runs.csv'
            row = result_row(self.args(notes='comma, newline\nand quote "'))
            append(path, row)
            with self.assertRaises(ValueError):
                append(path, row)
            with path.open(newline='') as f:
                records = list(csv.DictReader(f))
            self.assertEqual(len(records), 1)
            self.assertEqual(records[0]['notes'], row['notes'])

    def test_does_not_append_to_other_csv(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d)/'runs.csv'
            path.write_text('unrelated,value\na,b\n')
            with self.assertRaises(ValueError):
                append(path, result_row(self.args()))


if __name__ == '__main__':
    unittest.main()
