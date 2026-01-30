# Technical Documentation

## System Overview

This project implements an autonomous Guidance, Navigation, and Control (GNC) system for asteroid exploration missions, based on the Master's thesis chapters 4 and 5.

### Architecture

The system follows a modular architecture with clear separation of concerns:

```
GNC System
├── Functional Analysis Layer (Chapter 4)
│   ├── Mission Objectives Tree
│   ├── Requirements Database
│   └── Functional Decomposition
│
└── Physical Architecture Layer (Chapter 5)
    ├── Navigation Subsystem
    ├── Guidance Subsystem
    ├── Control Subsystem
    ├── Sensor Suite
    └── Actuator Suite
```

## Implementation Details

### 1. Functional Analysis (Chapter 4)

#### Mission Objectives Tree

The mission objectives are organized hierarchically following MBSE methodology:

- **OBJ-0**: Top-level mission (Sample Return)
  - **OBJ-1**: Rendezvous and Orbiting/Hovering
  - **OBJ-2**: Touch-And-Go Approach
  - **OBJ-3**: Earth Return
  - **OBJ-4**: Scientific Data Collection

Each objective is decomposed into functional requirements that drive the system design.

#### Requirements Management

Requirements follow ECSS-E-ST-60-30C standard and are categorized as:

- **Functional**: What the system shall do
- **Operational**: How the system shall operate
- **Performance**: Quantitative performance metrics
- **Interface**: Interactions between subsystems
- **Safety**: Critical safety constraints

Verification methods per ECSS-E-ST-10-02C:
- **Test**: Physical testing (preferred method)
- **Analysis**: Analytical verification
- **Review**: Design review
- **Inspection**: Direct examination

### 2. System Architecture (Chapter 5)

#### GNC Loop

The GNC system executes a closed-loop control cycle:

```python
while mission_active:
    # 1. Navigation: Estimate current state
    current_state = navigation.update(sensor_data)
    
    # 2. Guidance: Compute desired trajectory
    desired_state = guidance.plan(current_state, target)
    
    # 3. Control: Generate commands
    commands = control.compute(current_state, desired_state)
    
    # 4. Execute commands
    actuators.execute(commands)
```

#### Sensor Suite

Based on Chapter 5, Section 5.1:

1. **IMU (Inertial Measurement Unit)**
   - 3 accelerometers + 3 gyroscopes
   - Used for attitude propagation
   - Typical noise: 1e-4 m/s² (accel), 1e-6 rad/s (gyro)

2. **Star Tracker**
   - Absolute 3-axis attitude determination
   - Accuracy: ~0.001° (arcsec level)
   - Update rate: 5-10 Hz

3. **Sun Sensor**
   - Sun direction measurement
   - Used for safe mode and backup attitude
   - FOV: typically 120°

4. **Optical Camera**
   - Relative navigation via line-of-sight
   - Feature tracking for state estimation
   - Critical for proximity operations

5. **LIDAR/Altimeter**
   - Range measurement
   - Surface normal determination
   - Required for TAG landing

### 3. Mission Phases

#### Rendezvous Phase (RDV)

**Duration**: 24 days  
**Initial state**: [2500, 200, -50] km  
**Final state**: [20, 0, 0] km (Home Position)

**Requirements**:
- Position accuracy: ±2.4 km (3σ)
- Velocity accuracy: ±0.12 m/s (3σ)
- Remain within approach cone: 1° half-angle
- Total ΔV: ≤3.0 m/s

**Key Functions**:
- Autonomous trajectory control
- Multi-sensor state estimation
- Continuous asteroid tracking
- Maneuver planning and execution

#### Touch-And-Go Phase (TAG)

**Duration**: ~30 minutes (descent + surface + ascent)  
**Target accuracy**: 25 m (98.3% confidence)

**Requirements** (from Table 4.3):
- Landing accuracy: 25 m
- Attitude error: <10°
- Vertical velocity: 10±5 cm/s
- Horizontal velocity: <5 cm/s

**Key Functions**:
- Terrain mapping and feature detection
- Hazard avoidance
- Autonomous descent control
- Sample collection
- Safe ascent

### 4. Verification & Validation

Following the V-model from Chapter 1 and verification requirements from Chapter 6:

#### Verification Levels

1. **Unit Testing**
   - Individual function verification
   - Coverage: All critical functions

2. **Integration Testing**
   - Subsystem interfaces
   - GNC loop closure

3. **System Testing**
   - End-to-end mission scenarios
   - Requirements compliance

4. **Hardware-in-the-Loop (HIL)**
   - Real-time simulation with actual hardware
   - Reference: Hayabusa2 HIL setup (Figure 6.2)

#### Test Scenarios

Based on Hayabusa2 heritage:
- Nominal operations
- Off-nominal scenarios (sensor failures)
- Emergency abort procedures
- Multiple TAG attempts

### 5. Safety Architecture

Critical safety requirements (R-AUTO-03, R-GNC-48):

- **Hazard Detection**: Real-time obstacle avoidance
- **Abort Capability**: Autonomous abort at any time
- **Safe Trajectories**: Maintain escape options
- **Health Monitoring**: Continuous subsystem checks

Safety checks execute every control cycle:
```python
if not safety_check():
    execute_abort_maneuver()
    transition_to_safe_mode()
```

### 6. Performance Metrics

Tracked performance metrics:
- Position error (3σ)
- Velocity error (3σ)  
- Attitude error (3σ)
- Control effort (ΔV consumption)
- Computation time

Requirements compliance is verified continuously against:
- R-SYS-01: Attitude accuracy 0.1° (3σ)
- R-SYS-03: Position 25 m, Velocity 2.5 cm/s (3σ)
- R-GNC-51: State estimation accuracy during descent

## Usage Examples

### 1. Initialize GNC System

```python
from src.system_architecture import GNCSystem
from src.functional_analysis import GNCRequirements

# Load requirements
requirements = GNCRequirements()

# Initialize GNC
gnc = GNCSystem()
gnc.set_mode(GNCMode.APPROACH)
gnc.set_authority(ControlAuthority.AUTONOMOUS)
```

### 2. Run Mission Simulation

```python
# See examples/mission_simulation.py for complete example
python examples/mission_simulation.py
```

### 3. Verify Requirements

```python
requirements = GNCRequirements()

# Get all test requirements
test_reqs = requirements.get_by_verification(VerificationMethod.TEST)
print(f"Requirements requiring testing: {len(test_reqs)}")

# Check compliance
compliance = gnc.check_requirements_compliance()
for req_id, passed in compliance.items():
    print(f"{req_id}: {'PASS' if passed else 'FAIL'}")
```

## References

### Standards
- ECSS-E-ST-60-30C: GNC verification
- ECSS-E-ST-10-02C: System engineering requirements
- ECSS-E-ST-10-03: Testing
- ECSS-E-TM-10-21A: Simulation terminology

### Heritage Missions
- Hayabusa (2003-2010): First asteroid sample return
- Hayabusa2 (2014-2020): Enhanced GNC autonomy
- OSIRIS-REx (2016-2023): TAG maneuver validation

### Academic Source
Master's Thesis: "Lunar Missions Design with Electric Propulsion"
- Institution: Politecnico di Torino & Politecnico di Milano
- Chapters 4 & 5: Functional Analysis and System Architecture
- Focus: Autonomous GNC for small body exploration

## Future Work

Potential extensions:
1. Implement convex optimization for guidance (Chapter 3)
2. Add Monte Carlo simulation for robustness analysis
3. Implement fault detection and isolation
4. Add terrain relative navigation algorithms
5. Develop HIL testbed integration

## Contact

For questions about implementation:
- Review the code documentation
- Check examples/ directory for usage patterns
- Refer to thesis chapters 4 & 5 for theoretical background
