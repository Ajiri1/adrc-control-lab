import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "python"))

from adrc import ADRCConfig, simulate, write_csv


def main():
    config = ADRCConfig(
        dt=0.001,
        duration=10.0,
        b=1.0,
        b0=1.0,
        wc=5.0,
        wo=25.0,
        u_min=-10.0,
        u_max=10.0,
        disturbance_step_time=4.0,
        disturbance_step=2.0,
        disturbance_sine_amplitude=0.25,
        disturbance_sine_frequency=1.2,
        measurement_noise_std=0.0
    )
    rows = simulate(config)
    output_path = os.path.join(ROOT, "data", "python_results.csv")
    write_csv(rows, output_path)
    final_row = rows[-1]
    mean_abs_error = sum(abs(row["tracking_error"]) for row in rows) / len(rows)
    print(f"Samples: {len(rows)}")
    print(f"Final output: {final_row['output']:.4f}")
    print(f"Final reference: {final_row['reference']:.4f}")
    print(f"Mean absolute tracking error: {mean_abs_error:.4f}")
    print(f"Results written to: {output_path}")


if __name__ == "__main__":
    main()
