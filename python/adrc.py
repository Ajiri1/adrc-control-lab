from dataclasses import dataclass
import math


@dataclass
class ADRCConfig:
    dt: float = 0.001
    duration: float = 10.0
    b: float = 1.0
    b0: float = 1.0
    wc: float = 5.0
    wo: float = 25.0
    u_min: float = -10.0
    u_max: float = 10.0
    disturbance_step_time: float = 4.0
    disturbance_step: float = 2.0
    disturbance_sine_amplitude: float = 0.25
    disturbance_sine_frequency: float = 1.2
    measurement_noise_std: float = 0.0
    random_seed: int = 7


class ADRCController:
    def __init__(self, config):
        self.config = config
        self.z1 = 0.0
        self.z2 = 0.0
        self.z3 = 0.0
        self.kp = config.wc ** 2
        self.kd = 2.0 * config.wc
        self.beta1 = 3.0 * config.wo
        self.beta2 = 3.0 * config.wo ** 2
        self.beta3 = config.wo ** 3

    def update(self, reference, measurement, dt):
        error = measurement - self.z1
        dz1 = self.z2 + self.beta1 * error
        dz2 = self.z3 + self.beta2 * error
        dz3 = self.beta3 * error
        self.z1 += dt * dz1
        self.z2 += dt * dz2
        self.z3 += dt * dz3
        raw_u = (self.kp * (reference - self.z1) - self.kd * self.z2 - self.z3) / self.config.b0
        return min(self.config.u_max, max(self.config.u_min, raw_u))


def reference_signal(t):
    return 1.0 if t >= 0.5 else 0.0


def disturbance_signal(t, config):
    step = config.disturbance_step if t >= config.disturbance_step_time else 0.0
    sinusoid = config.disturbance_sine_amplitude * math.sin(2.0 * math.pi * config.disturbance_sine_frequency * t)
    return step + sinusoid


def simulate(config=None):
    import csv
    import os
    import random

    config = config or ADRCConfig()
    rng = random.Random(config.random_seed)
    controller = ADRCController(config)
    count = int(config.duration / config.dt) + 1
    y = 0.0
    velocity = 0.0
    rows = []
    previous_u = 0.0

    for index in range(count):
        t = index * config.dt
        reference = reference_signal(t)
        disturbance = disturbance_signal(t, config)
        measured = y + rng.gauss(0.0, config.measurement_noise_std)
        u = controller.update(reference, measured, config.dt)
        acceleration = config.b * u + disturbance
        velocity += config.dt * acceleration
        y += config.dt * velocity
        rows.append({
            "time": t,
            "reference": reference,
            "output": y,
            "velocity": velocity,
            "control": u,
            "disturbance": disturbance,
            "estimated_output": controller.z1,
            "estimated_velocity": controller.z2,
            "estimated_disturbance": controller.z3,
            "tracking_error": reference - y,
            "control_rate": (u - previous_u) / config.dt if index else 0.0
        })
        previous_u = u

    return rows


def write_csv(rows, path):
    import csv
    import os

    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
