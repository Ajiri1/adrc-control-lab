# ADRC Control Lab

A small, reproducible Active Disturbance Rejection Control (ADRC) project for a second-order plant. It includes a Python simulation, a C++ simulation, plotting utilities, basic tests, and a short technical note.

## Project objective

The project demonstrates how an Extended State Observer (ESO) estimates the plant output, its rate of change, and the combined disturbance. The controller uses those estimates to track a reference signal while rejecting a disturbance.

## Model

The simulated plant is

\[
\ddot{y} = b u + d(t)
\]

where `y` is the output, `u` is the control input, `b` is the nominal input gain, and `d(t)` is an unknown lumped disturbance. The ESO estimates:

- `z1`: output
- `z2`: output rate
- `z3`: lumped disturbance

The control law is

\[
u = \frac{k_p(r-z_1)-k_d z_2-z_3}{b_0}
\]

where `r` is the reference and `b0` is the nominal input gain used by the controller. The applied control is limited to a configurable range.

## Folder structure

```text
adrc_control_lab/
├── cpp/
│   ├── adrc_sim.cpp
│   └── CMakeLists.txt
├── python/
│   ├── adrc.py
│   ├── run_simulation.py
│   └── plot_results.py
├── tests/
│   └── test_adrc.py
├── docs/
│   └── technical_note.md
├── data/
├── requirements.txt
└── .gitignore
```

## Run the Python simulation

Python 3.10+ is recommended.

```bash
python -m venv .venv
```

On Windows:

```powershell
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python python/run_simulation.py
python python/plot_results.py
```

On macOS/Linux:

```bash
source .venv/bin/activate
pip install -r requirements.txt
python python/run_simulation.py
python python/plot_results.py
```

The simulation writes `data/python_results.csv`. The plotting script writes `data/python_results.png`.

## Build and run the C++ simulation

A C++17 compiler is required.

```bash
cmake -S cpp -B build
cmake --build build
```

Run the executable from the repository root:

```bash
./build/adrc_sim
```

On Windows, the executable will usually be `build/Debug/adrc_sim.exe` or `build/Release/adrc_sim.exe`, depending on the generator. The program writes `data/cpp_results.csv`.

## Run tests

```bash
python -m unittest discover -s tests -v
```

## What to investigate

1. Change the ESO bandwidth `wo` and observe the trade-off between disturbance-estimation speed and noise sensitivity.
2. Change `b0` to test sensitivity to input-gain mismatch.
3. Change the disturbance amplitude or timing.
4. Compare reference tracking with and without the disturbance.
5. Change the control saturation limits and observe how they affect recovery.

## Limitations

This is a simulation and learning project, not a validated controller for physical equipment. The simplified model assumes a known second-order structure, ideal sampling, and no sensor noise unless explicitly added. Before using ADRC on hardware, validate the model, sampling period, actuator limits, safety interlocks, and stability under the actual operating conditions.
