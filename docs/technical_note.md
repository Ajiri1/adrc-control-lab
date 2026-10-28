# Technical Note: Active Disturbance Rejection Control

## 1. Purpose

Active Disturbance Rejection Control (ADRC) is a control strategy that estimates and compensates for the combined effect of model uncertainty and external disturbances. Instead of requiring a detailed model of every disturbance, ADRC augments the system state with a disturbance estimate.

## 2. Plant model

The demonstration uses a second-order system:

\[
\ddot{y}=bu+d(t)
\]

The unknown term \(d(t)\) represents external loading, unmodelled dynamics, and other effects that are grouped into a lumped disturbance. The simulation combines a sinusoidal disturbance with a step disturbance introduced partway through the run.

## 3. Extended State Observer

The observer estimates the output, output velocity, and lumped disturbance. With observer states \(z_1,z_2,z_3\), the estimation error is

\[
e_o=y-z_1
\]

and the observer is implemented as

\[
\dot{z}_1=z_2+\beta_1 e_o
\]

\[
\dot{z}_2=z_3+\beta_2 e_o
\]

\[
\dot{z}_3=\beta_3 e_o
\]

The observer gains use the bandwidth parameter \(\omega_o\):

\[
\beta_1=3\omega_o,\quad \beta_2=3\omega_o^2,\quad \beta_3=\omega_o^3
\]

A higher observer bandwidth generally improves estimation speed but can increase sensitivity to measurement noise and discretization.

## 4. Control law

The controller uses the estimated state to calculate a virtual control action:

\[
u=\frac{k_p(r-z_1)-k_dz_2-z_3}{b_0}
\]

where \(r\) is the reference, \(b_0\) is the nominal input gain, and the feedback gains are set using a controller bandwidth \(\omega_c\):

\[
k_p=\omega_c^2,\quad k_d=2\omega_c
\]

The input is saturated to represent actuator limits.

## 5. Simulation workflow

1. Generate a step reference.
2. Calculate the applied disturbance.
3. Read the simulated plant output as the observer measurement.
4. Update the ESO states.
5. Calculate and saturate the control signal.
6. Integrate the plant acceleration, velocity, and output.
7. Store the plant response, observer estimates, disturbance, and control input.
8. Plot reference tracking and disturbance estimation.

## 6. Evaluation

Useful evaluation measures include mean absolute tracking error, settling time, overshoot, peak control effort, and disturbance-estimation error. A rigorous comparison should run the same disturbance profile with a baseline controller and ADRC, using identical plant parameters and initial conditions.

## 7. Limitations and next steps

This implementation uses forward Euler integration and an ideal measurement by default. It is intended for learning and should not be treated as hardware-ready. Useful extensions include measurement noise, plant-gain mismatch, alternate disturbances, a PID baseline, a parameter sweep, and a comparison of discrete-time integration methods.
