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

## 🚀 ESA Collaboration

This work was conducted at **ISAE-SUPAERO's Space Advanced Concepts Laboratory (SaCLaB)** in collaboration with ESA stakeholders for asteroid exploration GNC validation.

**Research Context:**
- **Institution**: ISAE-SUPAERO SaCLaB, Toulouse, France
- **Duration**: May 2023 - December 2023
- **Thesis Title**: "Systems Engineering for Asteroid Exploration GNC Validation Test"
- **Supervisors**: 
  - Prof. Nicole Viola (Politecnico di Torino)
  - Prof. Stéphanie Lizy-Destrez (ISAE-SUPAERO, SaCLaB Head)
  - Dr. Tomohiro Ishizuka (ISAE-SUPAERO SaCLaB)
  - Dr. Jasmine Rimani (Politecnico di Torino)
  - Eng. Jérôme Puech (ESA Collaboration Coordinator)

**Key Activities:**
- Autonomous GNC algorithm design for asteroid rendezvous and Touch-And-Go
- Model-Based Systems Engineering (MBSE) methodology with SysML
- Hardware-in-the-loop (HIL) simulation framework development
- Requirements verification and validation following ECSS standards

**Tools**: CATIA Cameo Systems Modeler (SysML), MATLAB/Simulink, Python

**[📄 Read more about ESA collaboration →](docs/ESA_COLLABORATION.md)**

## 🎯 Key Features

### Functional Architecture (Chapter 4)
- Complete functional decomposition following MBSE methodology
- SysML-inspired requirements management with full traceability
- Hierarchical function tree for GNC operations
- Activity diagrams for mission phases (RDV, TAG, Ascent)
- 50+ requirements aligned with ECSS standards

### System Architecture (Chapter 5)
- Modular GNC architecture with clear interfaces
- State estimation using Kalman filtering
- Trajectory optimization and guidance algorithms
- Closed-loop feedback control with PID schemes
- Sensor suite definition and actuator specifications

### Hardware-in-the-Loop (HIL) Testing (Chapter 6)
- Complete HIL testing methodology for GNC validation
- Test scenario definitions for Rendezvous and Touch-And-Go phases
- Verification matrix aligned with ECSS-E-ST-60-30C standards
- Heritage from Hayabusa2 and OSIRIS-REx HIL setups
- Compatible with ESA GRALS facility testing approach
- Fault injection and off-nominal scenario testing

**[📄 Read detailed HIL methodology →](docs/HIL_TESTING.md)**

### Technical Capabilities
- **Navigation**: Multi-sensor fusion (IMU, optical cameras, LIDAR, Star Tracker)
- **Guidance**: Trajectory planning with approach cone constraints and obstacle avoidance
- **Control**: Attitude and orbit control with reaction wheels and thrusters
- **Autonomy**: On-board decision making for hazard detection and collision avoidance
- **V&V**: Comprehensive verification strategy following ECSS testing standards

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
│   └── hil_simulation_example.py  # HIL test demonstration
├── docs/                          # Documentation and technical notes
│   ├── TECHNICAL_DOC.md
│   ├── VISUAL_GUIDE.md
│   ├── ESA_COLLABORATION.md
│   └── HIL_TESTING.md
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

### HIL Simulation Example
```python
from examples.hil_simulation_example import HILSimulator

# Initialize HIL simulator
hil = HILSimulator(dt=0.1)  # 10 Hz update rate

# Run rendezvous test scenario
hil.run_test_scenario(scenario='RDV', duration=100.0)

# Run touch-and-go test scenario
hil.run_test_scenario(scenario='TAG', duration=100.0)
```

## 📊 Mission Phases

![Mission Phases](docs/images/mission_phases.png)

### 1. Rendezvous Phase
- Approach from ~2500 km to 20 km home position
- Maintain spacecraft within approach cone (1° half-angle)
- Position accuracy: ±2.4 km (3σ)
- Velocity accuracy: ±0.12 m/s (3σ)
- ΔV budget: < 3.0 m/s

### 2. Touch-And-Go (TAG) Phase
- Descent from home position to surface
- Landing accuracy: 25 m (3σ, per OSIRIS-REx requirements)
- Attitude error: <10°
- Vertical velocity: 10 ± 5 cm/s
- Horizontal velocity: < 5 cm/s
- Sample collection duration: 2-5 seconds

### 3. Ascent Phase
- Safe departure from asteroid surface
- Hazard avoidance during ascent
- Return to home position
- Trajectory validation and fuel margin verification

## 📖 Documentation

| Document | Description | Link |
|----------|-------------|------|
| Quick Start Guide | Get up and running in 5 minutes | [View](QUICKSTART.md) |
| Technical Documentation | Detailed system design and implementation | [View](docs/TECHNICAL_DOC.md) |
| Visual Guide | Complete SysML diagrams and architecture visuals | [View](docs/VISUAL_GUIDE.md) |
| ESA Collaboration | Research context and academic background | [View](docs/ESA_COLLABORATION.md) |
| HIL Testing Strategy | Complete HIL methodology and test scenarios | [View](docs/HIL_TESTING.md) |
| Contributing Guidelines | How to contribute to this project | [View](CONTRIBUTING.md) |

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

1. **Testing**: Unit tests, integration tests, Hardware-in-the-Loop simulation
2. **Analysis**: Performance analysis, Monte Carlo simulations, sensitivity studies
3. **Review-of-design**: Documentation review, peer review, design walkthroughs
4. **Inspection**: Code quality checks, interface verification, standards compliance

### Verification Matrix

| Requirement | Test Method | HIL Scenario | Status |
|-------------|-------------|--------------|--------|
| R-GNC-01 | HIL Testing | RDV-HIL-001 | ✅ PASS |
| R-GNC-02 | HIL Testing | NAV-HIL-001 | ✅ PASS |
| R-GNC-48 | HIL Testing | TAG-HIL-001 | ✅ PASS |
| R-AUTO-03 | HIL Testing | ABORT-HIL-001 | ✅ PASS |

**[📄 See complete verification strategy →](docs/HIL_TESTING.md)**

## 📖 Technical Documentation

### Key Requirements
- **R-GNC-01**: Autonomous trajectory control with <5% fuel margin
- **R-GNC-02**: Relative state estimation accuracy (position: 25m, velocity: 2.5cm/s)
- **R-GNC-03**: Real-time hazard detection and avoidance
- **R-GNC-04**: Robust control in uncertain gravitational fields
- **R-GNC-48**: Touch-and-Go landing accuracy within 25m (3σ)
- **R-AUTO-03**: Autonomous abort capability with safe escape trajectory

### Reference Standards
- **ECSS-E-ST-60-30C**: Spacecraft GNC verification
- **ECSS-E-ST-10-02C**: System engineering general requirements
- **ECSS-E-ST-10-03C**: Testing standards
- **ECSS-E-TM-10-21A**: Simulation terminology
- **ISO 9001:2015**: Quality management systems

## 🎓 Academic Context

This implementation is based on Master's thesis research conducted at:
- **Politecnico di Torino** (Italy)
- **ISAE-SUPAERO Space Advanced Concepts Laboratory** (France)

**Thesis**: "Systems Engineering for Asteroid Exploration GNC Validation Test"

**Focus**: Complete systems engineering approach from functional analysis (Chapter 4) through system architecture (Chapter 5) to verification and validation (Chapter 6), with emphasis on MBSE methodology and ECSS standards compliance.

**Application Domain**: Autonomous asteroid exploration with sample return capability

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

- **ISAE-SUPAERO SaCLaB** for research facilities and technical support
- **Heritage Missions**: Hayabusa, Hayabusa2 (JAXA), OSIRIS-REx (NASA)
- **ESA GRALS Facility** for HIL testing methodology reference
- **Standards**: European Cooperation for Space Standardization (ECSS)
- **Methodology**: Model-Based Systems Engineering (MBSE) with SysML
- **Academic Supervision**: 
  - Prof. Nicole Viola (Politecnico di Torino)
  - Prof. Stéphanie Lizy-Destrez (ISAE-SUPAERO)
  - Dr. Tomohiro Ishizuka (ISAE-SUPAERO)
  - Dr. Jasmine Rimani (Politecnico di Torino)

## 📧 Contact

**Ginevra Cianci**
- LinkedIn: [linkedin.com/in/ginevracianci](https://linkedin.com/in/ginevracianci)
- GitHub: [github.com/ginevracianci](https://github.com/ginevracianci)
- Email: ginevra.cianci@polito.it

**Project Link**: [https://github.com/ginevracianci/gnc-autonomous-system](https://github.com/ginevracianci/gnc-autonomous-system)

---

## 🔗 Related Resources
- [ISAE-SUPAERO SaCLaB](https://www.isae-supaero.fr/en/research/saclab)
- [ESA ESTEC GNC Division](https://www.esa.int/About_Us/ESTEC)
- [ECSS Standards](https://ecss.nl/)
- [Hayabusa2 Mission](https://www.hayabusa2.jaxa.jp/en/)
- [OSIRIS-REx Mission](https://www.asteroidmission.org/)
