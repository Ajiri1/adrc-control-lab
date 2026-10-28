#include <algorithm>
#include <cmath>
#include <filesystem>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <string>

struct Config {
    double dt = 0.001;
    double duration = 10.0;
    double b = 1.0;
    double b0 = 1.0;
    double wc = 5.0;
    double wo = 25.0;
    double u_min = -10.0;
    double u_max = 10.0;
    double disturbance_step_time = 4.0;
    double disturbance_step = 2.0;
    double disturbance_sine_amplitude = 0.25;
    double disturbance_sine_frequency = 1.2;
};

struct State {
    double y = 0.0;
    double velocity = 0.0;
    double z1 = 0.0;
    double z2 = 0.0;
    double z3 = 0.0;
    double previous_u = 0.0;
};

class ADRCController {
public:
    explicit ADRCController(const Config& config)
        : config_(config),
          kp_(config.wc * config.wc),
          kd_(2.0 * config.wc),
          beta1_(3.0 * config.wo),
          beta2_(3.0 * config.wo * config.wo),
          beta3_(config.wo * config.wo * config.wo) {}

    double update(double reference, double measurement) {
        const double error = measurement - z1_;
        const double dz1 = z2_ + beta1_ * error;
        const double dz2 = z3_ + beta2_ * error;
        const double dz3 = beta3_ * error;
        z1_ += config_.dt * dz1;
        z2_ += config_.dt * dz2;
        z3_ += config_.dt * dz3;
        const double raw = (kp_ * (reference - z1_) - kd_ * z2_ - z3_) / config_.b0;
        return std::clamp(raw, config_.u_min, config_.u_max);
    }

    double estimated_output() const { return z1_; }
    double estimated_velocity() const { return z2_; }
    double estimated_disturbance() const { return z3_; }

private:
    Config config_;
    double kp_;
    double kd_;
    double beta1_;
    double beta2_;
    double beta3_;
    double z1_ = 0.0;
    double z2_ = 0.0;
    double z3_ = 0.0;
};

double reference_signal(double t) {
    return t >= 0.5 ? 1.0 : 0.0;
}

double disturbance_signal(double t, const Config& config) {
    const double step = t >= config.disturbance_step_time ? config.disturbance_step : 0.0;
    const double sinusoid = config.disturbance_sine_amplitude *
        std::sin(2.0 * std::acos(-1.0) * config.disturbance_sine_frequency * t);
    return step + sinusoid;
}

int main() {
    const Config config;
    State state;
    ADRCController controller(config);
    const int count = static_cast<int>(config.duration / config.dt) + 1;
    std::filesystem::create_directories("data");
    std::ofstream output("data/cpp_results.csv");
    if (!output) {
        std::cerr << "Could not open data/cpp_results.csv\n";
        return 1;
    }

    output << "time,reference,output,velocity,control,disturbance,estimated_output,estimated_velocity,estimated_disturbance,tracking_error,control_rate\n";
    output << std::fixed << std::setprecision(8);

    double absolute_error_sum = 0.0;

    for (int index = 0; index < count; ++index) {
        const double t = index * config.dt;
        const double reference = reference_signal(t);
        const double disturbance = disturbance_signal(t, config);
        const double control = controller.update(reference, state.y);
        const double acceleration = config.b * control + disturbance;
        state.velocity += config.dt * acceleration;
        state.y += config.dt * state.velocity;
        const double tracking_error = reference - state.y;
        const double control_rate = index == 0 ? 0.0 : (control - state.previous_u) / config.dt;
        absolute_error_sum += std::abs(tracking_error);

        output << t << ','
               << reference << ','
               << state.y << ','
               << state.velocity << ','
               << control << ','
               << disturbance << ','
               << controller.estimated_output() << ','
               << controller.estimated_velocity() << ','
               << controller.estimated_disturbance() << ','
               << tracking_error << ','
               << control_rate << '\n';

        state.previous_u = control;
    }

    output.close();
    std::cout << "Samples: " << count << '\n';
    std::cout << "Final output: " << state.y << '\n';
    std::cout << "Mean absolute tracking error: " << absolute_error_sum / count << '\n';
    std::cout << "Results written to data/cpp_results.csv\n";
    return 0;
}
