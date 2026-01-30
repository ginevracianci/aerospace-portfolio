# Autonomous GNC System for Small Body Exploration

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](./LICENSE)
[![MBSE](https://img.shields.io/badge/Methodology-MBSE-orange.svg)]()
[![ECSS](https://img.shields.io/badge/Standards-ECSS-red.svg)]()

A Python-based implementation of an autonomous Guidance, Navigation, and Control (GNC) system designed for small body (asteroid) exploration missions, following Model-Based Systems Engineering (MBSE) principles.

![Mission Overview](docs/images/mission_overview.png)

## 📋 Project Overview

This project implements the functional analysis and system architecture for an autonomous GNC system capable of performing:
- **Rendezvous and Hovering** with asteroids
- **Touch-And-Go (TAG)** sample collection maneuvers
- **Autonomous Navigation** in uncertain dynamical environments
- **Real-time Trajectory Control** with minimal ground intervention

The system design is based on heritage from successful missions including Hayabusa2 and OSIRIS-REx, and follows ECSS standards for space systems engineering.

## 📚 Academic Background

This project is based on research conducted for my Master's Thesis:

**Title**: Lunar Missions Design with Electric Propulsion: A Parametric Study 
on SEP Trajectories for Small Satellites

**Institution**: Politecnico di Torino & Politecnico di Milano

**Supervisors**: 
- Prof. Lorenzo Casalino (Politecnico di Torino)
- Prof. Camilla Colombo (Politecnico di Milano)

**Implementation**: Chapters 4 (Functional Analysis) & 5 (System Architecture)

[📄 View Thesis Abstract](https://drive.google.com/file/d/163-vJmio-P-rDc4Nkhl1ZB7KGaXkaF6G/view?usp=sharing)

## 🎯 Key Features

### Functional Architecture (Chapter 4)
- Complete functional decomposition following MBSE methodology
- SysML-inspired requirements management
- Hierarchical function tree for GNC operations
- Activity diagrams for mission phases (RDV, TAG, Ascent)

### System Architecture (Chapter 5)
- Modular GNC architecture with clear interfaces
- State estimation using Kalman filtering
- Trajectory optimization and guidance algorithms
- Closed-loop feedback control with PID schemes

### Technical Capabilities
- **Navigation**: Multi-sensor fusion (IMU, optical cameras, LIDAR)
- **Guidance**: Trajectory planning with obstacle avoidance
- **Control**: Attitude and orbit control with reaction wheels and thrusters
- **Autonomy**: On-board decision making for hazard detection and avoidance

## 🏗️ Project Structure

```
gnc-autonomous-system/
│
├── src/
│   ├── functional_analysis/      # Functional decomposition and requirements
│   │   ├── mission_objectives.py
│   │   ├── function_tree.py
│   │   └── requirements.py
│   │
│   ├── system_architecture/       # GNC system architecture
│   │   ├── gnc_system.py
│   │   ├── sensors.py
│   │   └── actuators.py
│   │
│   ├── navigation/                # State estimation algorithms
│   │   ├── kalman_filter.py
│   │   ├── relative_state_estimation.py
│   │   └── optical_navigation.py
│   │
│   ├── guidance/                  # Trajectory planning
│   │   ├── trajectory_optimizer.py
│   │   ├── approach_cone.py
│   │   └── tag_guidance.py
│   │
│   └── control/                   # Attitude and orbit control
│       ├── pid_controller.py
│       ├── attitude_control.py
│       └── thrust_management.py
│
├── tests/                         # Unit and integration tests
├── examples/                      # Example missions and scenarios
├── docs/                          # Documentation and technical notes
└── data/                         # Mission parameters and test data
```

## 🚀 Getting Started

### Prerequisites
```bash
python >= 3.8
numpy >= 1.20.0
scipy >= 1.7.0
matplotlib >= 3.4.0
```

### Installation
```bash
# Clone the repository
git clone https://github.com/ginevracianci/gnc-autonomous-system.git
cd gnc-autonomous-system

# Install dependencies
pip install -r requirements.txt

# Run tests
pytest tests/
```

### Quick Start Example
```python
from src.system_architecture import GNCSystem
from src.navigation import RelativeStateEstimator
from src.guidance import TrajectoryOptimizer
from src.control import AttitudeController

# Initialize GNC system
gnc = GNCSystem()

# Setup navigation
navigator = RelativeStateEstimator()

# Configure guidance
guidance = TrajectoryOptimizer(
    initial_position=[2500, 200, -50],  # km
    final_position=[20, 0, 0],          # km
    approach_cone_angle=1.0             # degrees
)

# Setup control
controller = AttitudeController(
    control_type='PID',
    gains={'kp': 0.5, 'ki': 0.1, 'kd': 0.2}
)

# Run simulation
results = gnc.simulate_mission(
    navigator=navigator,
    guidance=guidance,
    controller=controller,
    duration=24  # days
)
```

## 📊 Mission Phases

![Mission Phases](docs/images/mission_phases.png)

### 1. Rendezvous Phase
- Approach from ~2500 km to 20 km home position
- Maintain spacecraft within approach cone (1° half-angle)
- Position accuracy: ±2.4 km (3σ)
- Velocity accuracy: ±0.12 m/s (3σ)

### 2. Touch-And-Go (TAG) Phase
- Descent from home position to surface
- Landing accuracy: 25 m (per OSIRIS-REx requirements)
- Attitude error: <10°
- Vertical velocity: 10 cm/s
- Horizontal velocity: 5 cm/s
- Sample collection duration: 2-5 seconds

### 3. Ascent Phase
- Safe departure from asteroid surface
- Hazard avoidance during ascent
- Return to home position
- Trajectory validation

## 📖 Documentation

- **[Quick Start Guide](QUICKSTART.md)** - Get up and running in 5 minutes
- **[Technical Documentation](docs/TECHNICAL_DOC.md)** - Detailed system design and implementation
- **[Visual Guide](docs/VISUAL_GUIDE.md)** - Complete SysML diagrams and architecture visuals
- **[Contributing Guidelines](CONTRIBUTING.md)** - How to contribute to this project

### System Diagrams

The project includes complete SysML diagrams created with Cameo Systems Modeler:

| Diagram Type | Description | View |
|--------------|-------------|------|
| Mission Objectives Tree | Hierarchical decomposition of mission goals | [View](docs/images/objective_tree.png) |
| Requirements Diagrams | ECSS-compliant requirements with traceability | [View](docs/images/autonomous_requirements.png) |
| GNC Architecture | Complete system architecture and data flow | [View](docs/images/gnc_architecture.png) |
| Activity Diagrams | Operational sequences for RDV and TAG | [View](docs/images/rdv_activity.png) |

📊 **[See all diagrams in Visual Guide →](docs/VISUAL_GUIDE.md)**

## 🔬 Verification & Validation

The system follows ECSS-E-ST-10-02C verification approach with four methods:
1. **Testing**: Unit tests, integration tests, HIL simulation
2. **Analysis**: Performance analysis, Monte Carlo simulations
3. **Review-of-design**: Documentation review, peer review
4. **Inspection**: Code quality, interface verification

## 📖 Technical Documentation

### Key Requirements
- **R-GNC-01**: Autonomous trajectory control with <5% fuel margin
- **R-GNC-02**: Relative state estimation accuracy (position: 25m, velocity: 2.5cm/s)
- **R-GNC-03**: Real-time hazard detection and avoidance
- **R-GNC-04**: Robust control in uncertain gravitational fields

### Reference Standards
- ECSS-E-ST-60-30C: Spacecraft GNC verification
- ECSS-E-ST-10-02C: System engineering general requirements
- ECSS-E-ST-10-03: Testing
- ECSS-E-TM-10-21A: Simulation terminology

## 🎓 Academic Context

This implementation is based on the Master's thesis:
**"Lunar Missions Design with Electric Propulsion: A Parametric Study on SEP Trajectories for Small Satellites"**
- Institution: Politecnico di Torino & Politecnico di Milano
- Focus: Chapters 4 (Functional Analysis) & 5 (System Architecture Definition)
- Application: Asteroid exploration with autonomous GNC

## 🤝 Contributing

Contributions are welcome! Please read the contributing guidelines before submitting pull requests.

### Development Workflow
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Heritage Missions**: Hayabusa, Hayabusa2, OSIRIS-REx
- **Standards**: European Cooperation for Space Standardization (ECSS)
- **Methodology**: Model-Based Systems Engineering (MBSE) with SysML
- **Academic Supervision**: Prof. Lorenzo Casalino (PoliTO), Prof. Camilla Colombo (PoliMI)

## 📧 Contact

Ginevra Cianci - [LinkedIn](https://linkedin.com/in/ginevra-cianci) - ginevra.cianci@gmail.com

Project Link: [https://github.com/ginevracianci/gnc-autonomous-system](https://github.com/ginevracianci/gnc-autonomous-system)

---

## 🔗 Related Projects
- [Trajectory Optimization Tools](https://github.com/yourname/trajectory-optimization)
- [Spacecraft Dynamics Simulator](https://github.com/yourname/spacecraft-sim)
- [MBSE Tools for Space Systems](https://github.com/yourname/mbse-space)
