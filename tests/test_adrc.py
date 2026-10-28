import os
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "python"))

from adrc import ADRCConfig, ADRCController, simulate


class ADRCTests(unittest.TestCase):
    def test_control_is_saturated(self):
        config = ADRCConfig(u_min=-2.0, u_max=2.0)
        controller = ADRCController(config)
        control = controller.update(100.0, 0.0, config.dt)
        self.assertGreaterEqual(control, config.u_min)
        self.assertLessEqual(control, config.u_max)

    def test_simulation_has_expected_columns(self):
        config = ADRCConfig(duration=0.1, dt=0.001)
        rows = simulate(config)
        self.assertGreater(len(rows), 1)
        self.assertIn("estimated_disturbance", rows[0])
        self.assertIn("tracking_error", rows[0])

    def test_output_remains_finite(self):
        config = ADRCConfig(duration=1.0, dt=0.001)
        rows = simulate(config)
        for row in rows:
            self.assertTrue(abs(row["output"]) < 1e6)


if __name__ == "__main__":
    unittest.main()
