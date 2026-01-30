# Quick Start Guide

Get started with the GNC Autonomous System in 5 minutes!

## Installation

```bash
# Clone the repository
git clone https://github.com/ginevracianci/gnc-autonomous-system.git
cd gnc-autonomous-system

# Install dependencies
pip install -r requirements.txt
```

## Run Your First Simulation

```bash
# Run the complete mission example
python examples/mission_simulation.py
```

This will demonstrate:
- Mission objectives initialization
- GNC requirements loading
- Sensor suite operation
- System mode transitions
- Requirements compliance checking

## Quick Examples

### 1. Explore Mission Objectives

```python
from src.functional_analysis.mission_objectives import MissionObjectivesTree, MissionPhase

# Initialize objectives tree
tree = MissionObjectivesTree()

# Show all objectives
tree.print_tree()

# Get objectives for a specific phase
rdv_objectives = tree.get_objectives_by_phase(MissionPhase.RENDEZVOUS)
for obj in rdv_objectives:
    print(f"{obj.id}: {obj.name}")
```

### 2. Work with Requirements

```python
from src.functional_analysis.requirements import GNCRequirements, VerificationMethod

# Load all requirements
reqs = GNCRequirements()

# Get specific requirement
tag_req = reqs.get_requirement("R-TAG-01")
print(f"{tag_req.text}")

# Find all requirements verified by testing
test_reqs = reqs.get_by_verification(VerificationMethod.TEST)
print(f"Requirements requiring testing: {len(test_reqs)}")

# Export requirements matrix
matrix = reqs.export_requirements_matrix()
print(matrix['verification_coverage'])
```

### 3. Initialize GNC System

```python
from src.system_architecture.gnc_system import GNCSystem, GNCMode, GNCState
import numpy as np

# Create GNC system with default config
gnc = GNCSystem()

# Set operational mode
gnc.set_mode(GNCMode.APPROACH)

# Set current state
gnc.current_state = GNCState(
    position=np.array([2500e3, 200e3, -50e3]),  # m
    velocity=np.array([-1.18, -1.97, 0.16])      # m/s
)

# Check safety
if gnc._safety_check():
    print("System is safe to proceed")
```

### 4. Use Sensor Suite

```python
from src.system_architecture.sensors import SensorSuite
import numpy as np

# Initialize all sensors
sensors = SensorSuite()

# Simulate spacecraft state
state = {
    'acceleration': np.array([0.01, 0.005, -0.002]),
    'angular_rate': np.array([0.001, -0.0005, 0.0002]),
    'attitude': np.array([1, 0, 0, 0]),
    'sun_direction': np.array([0.5, 0.3, 0.8]) / np.linalg.norm([0.5, 0.3, 0.8]),
    'target_position_body': np.array([100, 50, 200]),
    'target_distance': 223.6,
    'surface_normal': np.array([0, 0, 1])
}

# Get all measurements
measurements = sensors.get_all_measurements(state, timestamp=0.0)

# Access individual sensors
imu_data = measurements['imu'].data
print(f"IMU: acceleration={imu_data[:3]}, gyro={imu_data[3:]}")
```

## Understanding the Code Structure

```
src/
├── functional_analysis/       # Chapter 4: MBSE approach
│   ├── mission_objectives.py  # Mission objectives tree
│   └── requirements.py         # Requirements database
│
└── system_architecture/        # Chapter 5: GNC architecture
    ├── gnc_system.py          # Main GNC system
    └── sensors.py             # Sensor suite
```

## Key Concepts

### Mission Phases

1. **CRUISE**: Minimal operations, conserving resources
2. **APPROACH**: Active navigation towards asteroid
3. **PROXIMITY**: Precise control for close operations
4. **TAG_DESCENT**: Autonomous descent to surface
5. **TAG_SURFACE**: Surface operations and sampling
6. **TAG_ASCENT**: Safe departure from surface

### Requirements Types

- **Functional**: What the system does
- **Operational**: How the system operates
- **Performance**: Quantitative metrics
- **Interface**: System interactions
- **Safety**: Critical constraints

### Verification Methods (ECSS)

- **TEST**: Physical testing (preferred)
- **ANALYSIS**: Mathematical/simulation verification
- **REVIEW**: Design review
- **INSPECTION**: Direct examination

## Common Tasks

### Check Requirements Compliance

```python
# After running simulation
compliance = gnc.check_requirements_compliance()
for req_id, passed in compliance.items():
    status = "✓ PASS" if passed else "✗ FAIL"
    print(f"{status} {req_id}")
```

### Get Performance Summary

```python
summary = gnc.get_performance_summary()
print(f"Mean position error: {summary['mean_position_error']:.2f} m")
print(f"Mean velocity error: {summary['mean_velocity_error']:.4f} m/s")
```

### Export Requirements Matrix

```python
matrix = reqs.export_requirements_matrix()

# Save to file
import json
with open('requirements_matrix.json', 'w') as f:
    json.dump(matrix, f, indent=2)
```

## Next Steps

1. **Read the full documentation**: See `docs/TECHNICAL_DOC.md`
2. **Explore examples**: Check `examples/` directory
3. **Run tests**: `pytest tests/` (when implemented)
4. **Contribute**: See `CONTRIBUTING.md`

## Troubleshooting

### Import Errors

Make sure you're in the project root directory:
```bash
cd gnc-autonomous-system
python examples/mission_simulation.py
```

### Missing Dependencies

Install all required packages:
```bash
pip install -r requirements.txt
```

## Key Parameters from Thesis

### Rendezvous Phase (Table 4.1)
- Initial position: [2500, 200, -50] km
- Final position: [20, 0, 0] km  
- Position tolerance: ±2.4 km (3σ)
- Velocity tolerance: ±0.12 m/s (3σ)
- Duration: 24 days

### TAG Phase (Table 4.3 - OSIRIS-REx)
- Landing accuracy: 25 m
- Attitude error: <10°
- Vertical velocity: 10±5 cm/s
- Horizontal velocity: <5 cm/s

### Performance Requirements
- Attitude accuracy: 0.1° (3σ) - R-SYS-01
- Position accuracy: 25 m (3σ) - R-SYS-03
- Velocity accuracy: 2.5 cm/s (3σ) - R-SYS-03

## Resources

- **Thesis**: Chapters 4 & 5 provide theoretical background
- **Standards**: ECSS-E-ST-60-30C (GNC), ECSS-E-ST-10-02C (Systems)
- **Heritage**: Hayabusa2, OSIRIS-REx missions
- **Documentation**: `docs/` directory

## Support

For questions or issues:
1. Check documentation in `docs/`
2. Review examples in `examples/`
3. Open an issue on GitHub
4. Contact: ginevra.cianci@gmail.com

---

**Ready to start?** Run `python examples/mission_simulation.py` and explore!
