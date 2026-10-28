import csv
import os
import matplotlib.pyplot as plt

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_PATH = os.path.join(ROOT, "data", "python_results.csv")
PNG_PATH = os.path.join(ROOT, "data", "python_results.png")


def load_rows(path):
    with open(path, newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def main():
    rows = load_rows(CSV_PATH)
    t = [float(row["time"]) for row in rows]
    reference = [float(row["reference"]) for row in rows]
    output = [float(row["output"]) for row in rows]
    control = [float(row["control"]) for row in rows]
    disturbance = [float(row["disturbance"]) for row in rows]
    estimated_disturbance = [float(row["estimated_disturbance"]) for row in rows]
    estimated_output = [float(row["estimated_output"]) for row in rows]

    figure, axes = plt.subplots(3, 1, figsize=(12, 9), sharex=True)
    axes[0].plot(t, reference, label="Reference")
    axes[0].plot(t, output, label="Plant output")
    axes[0].plot(t, estimated_output, linestyle="--", label="ESO output estimate")
    axes[0].set_ylabel("Output")
    axes[0].grid(True)
    axes[0].legend()

    axes[1].plot(t, disturbance, label="Applied disturbance")
    axes[1].plot(t, estimated_disturbance, linestyle="--", label="ESO disturbance estimate")
    axes[1].set_ylabel("Disturbance")
    axes[1].grid(True)
    axes[1].legend()

    axes[2].plot(t, control, label="Control input")
    axes[2].set_xlabel("Time (s)")
    axes[2].set_ylabel("Control")
    axes[2].grid(True)
    axes[2].legend()

    figure.suptitle("Active Disturbance Rejection Control")
    figure.tight_layout()
    figure.savefig(PNG_PATH, dpi=160)
    print(f"Plot written to: {PNG_PATH}")
    plt.show()


if __name__ == "__main__":
    main()
