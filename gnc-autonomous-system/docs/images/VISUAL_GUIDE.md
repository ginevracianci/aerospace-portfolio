# Visual Guide - GNC System Architecture

This document presents the complete visual architecture of the autonomous GNC system, featuring diagrams created using Cameo Systems Modeler (SysML) as part of the thesis work.

## Table of Contents

1. [Mission Overview](#mission-overview)
2. [Mission Objectives Tree](#mission-objectives-tree)
3. [Requirements Diagrams](#requirements-diagrams)
4. [System Architecture](#system-architecture)
5. [Activity Diagrams](#activity-diagrams)
6. [Analysis Context](#analysis-context)

---

## Mission Overview

### Mission Phases
![Mission Phases](images/mission_phases.png)

The mission consists of three main phases:
1. **Approach & Rendezvous**: Long-range navigation and approach to 20 km home position
2. **Touch-And-Go (TAG)**: Descent, sample collection, and ascent
3. **Earth Return**: Departure trajectory and return to Earth

### Mission Context
![Mission Overview](images/mission_overview.png)

---

## Mission Objectives Tree

### Hierarchical Objectives Decomposition
![Objectives Tree](images/objective_tree.png)

The mission objectives tree follows MBSE methodology with:
- **Top Level (OBJ-0)**: Sample Return Mission
- **Level 1**: Primary mission phases (RDV, TAG, Return, Science)
- **Level 2+**: Functional decomposition into specific GNC operations

**Key Objectives**:
- OBJ-1: Rendezvous and Orbiting/Hovering
- OBJ-2: Touch-And-Go Approach
- OBJ-3: Departure and Earth Return
- OBJ-4: Scientific Data Collection

---

## Requirements Diagrams

### Requirements Overview
![Requirements Overview](images/requirements_overview.png)

Requirements are organized following ECSS-E-ST-60-30C standards:
- Functional Requirements
- Operational Requirements
- Performance Requirements
- Interface Requirements
- Safety Requirements

### Autonomous Requirements
![Autonomous Requirements](images/autonomous_requirements.png)

**Key Autonomous Requirements**:
- **R-AUTO-01**: Autonomous trajectory control with minimal fuel
- **R-AUTO-02**: Accurate state estimation for maneuver execution
- **R-AUTO-03**: Independent operation with safe escape plans
- **R-AUTO-04**: Resource management and constraint avoidance

**Rationale**: Ground intervention impossible due to communication delay (10+ minutes round trip)

### TAG Requirements
![TAG Requirements](images/tag_requirements.png)

**Touch-And-Go Requirements** (Based on OSIRIS-REx):
- **R-TAG-01**: Landing accuracy 25 m (98.3% confidence)
- **R-TAG-02**: Attitude alignment with local vertical (±10°)
- **R-TAG-03**: Vertical velocity 10±5 cm/s at touchdown
- **R-TAG-04**: Horizontal velocity <5 cm/s at touchdown
- **R-TAG-05**: Allow for 3 TAG attempts within propellant budget

**Verification**: Primarily through Hardware-in-the-Loop (HIL) testing

---

## System Architecture

### GNC Functional Architecture
![GNC Architecture](images/gnc_architecture.png)

The GNC system implements a modular architecture with three main subsystems:

#### 1. Navigation Subsystem
- **State Estimation**: Kalman filtering with multi-sensor fusion
- **Sensors**: IMU, Star Tracker, Sun Sensor, Optical Camera, LIDAR
- **Output**: Position, velocity, attitude, angular rates (LVLH frame)

#### 2. Guidance Subsystem
- **Trajectory Planning**: Optimal path generation
- **Approach Cone**: Maintain 1° half-angle constraint
- **Hazard Avoidance**: Real-time obstacle detection and avoidance
- **Output**: Desired state trajectory

#### 3. Control Subsystem
- **Attitude Control**: 3-axis stabilization using reaction wheels
- **Orbit Control**: Thrust vector control for translation
- **Control Law**: PID-based feedback control
- **Output**: Actuator commands (thrust, torque)

### Data Flow
```
Sensors → Navigation → State Estimate
                ↓
        Guidance ← Target State
                ↓
        Control → Commands → Actuators
```

### Mission Model
![Mission Model](images/mission_model.png)

The mission model shows the operational context including:
- Spacecraft blocks and subsystems
- Physical environment (asteroid gravitational field)
- External disturbances and perturbations
- Interface definitions

---

## Activity Diagrams

Activity diagrams show the operational flow for each mission phase, created using SysML.

### Rendezvous Activity Diagram
![Rendezvous Activity](images/rdv_activity.png)

**Rendezvous Sequence**:
1. **Orbit Estimation**: Determine relative position/velocity
2. **Target Acquisition**: Lock onto asteroid with optical sensors
3. **Approach Guidance**: Compute optimal approach trajectory
4. **Maneuver Execution**: Execute delta-V burns
5. **State Update**: Refine state estimate post-maneuver
6. **Arrival**: Reach 20 km home position

**Key Functions**:
- Continuous asteroid tracking
- Approach cone constraint satisfaction
- Fuel-optimal trajectory planning
- State estimation refinement

### TAG Activity Diagram
![TAG Activity](images/tag_activity.png)

**Touch-And-Go Sequence**:
1. **Descent Initialization**: Depart from home position
2. **Terrain Mapping**: Scan landing site with LIDAR/cameras
3. **Hazard Detection**: Identify obstacles and safe zones
4. **Descent Guidance**: Compute safe descent trajectory
5. **Terminal Approach**: Final guidance to touchdown point
6. **Touchdown**: Contact surface, collect sample (2-5 sec)
7. **Ascent**: Immediate departure from surface
8. **Return to HP**: Navigate back to home position

**Critical Functions**:
- Real-time hazard detection
- Surface normal computation
- Velocity control (vertical/horizontal)
- Abort capability at any time

---

## Analysis Context

### System Context Diagram
![Analysis Context](images/analysis_context.png)

The analysis context defines:

#### System Boundary
- **System of Interest**: GNC Subsystem
- **External Interfaces**: 
  - Physical Environment (asteroid gravity, solar pressure)
  - Ground Segment (commands, telemetry)
  - Other S/C Subsystems (power, thermal, communications)

#### Key Blocks
- **Spacecraft Block**: Contains all subsystems
- **GNC Subsystem**: System under analysis
- **Environment Block**: External disturbances
- **Sensor Suite**: Measurement devices
- **Actuator Suite**: Control devices

#### Interfaces
- **Sensor Data Flow**: Environment → Sensors → GNC
- **Command Flow**: GNC → Actuators → Environment
- **Telemetry Flow**: GNC → Ground Segment

---

## Implementation Notes

### Tools Used
- **Cameo Systems Modeler**: SysML modeling and diagram creation
- **MATLAB**: Initial trajectory analysis and optimization
- **Python**: Implementation of GNC algorithms

### Standards Compliance
- **ECSS-E-ST-60-30C**: GNC functional chain verification
- **ECSS-E-ST-10-02C**: System engineering general requirements
- **ISO/IEC/IEEE 15288:2015**: Systems and software engineering

### Verification Methods
Per ECSS-E-ST-10-02C:
1. **Test**: Physical testing (preferred for critical functions)
2. **Analysis**: Mathematical/simulation verification
3. **Review**: Design review and documentation
4. **Inspection**: Direct examination of implementation

---

## Mission Requirements Summary

### Performance Requirements

| Requirement | Phase | Value | 3σ |
|------------|-------|-------|-----|
| Position Accuracy | RDV Arrival | 20 km | ±2.4 km |
| Velocity Accuracy | RDV Arrival | 0 m/s | ±0.12 m/s |
| Landing Accuracy | TAG | Target site | 25 m |
| Attitude Error | TAG | Vertical aligned | <10° |
| Vertical Velocity | TAG Touchdown | 10 cm/s | ±5 cm/s |
| Horizontal Velocity | TAG Touchdown | 0 cm/s | <5 cm/s |

### Operational Constraints

| Constraint | Value | Rationale |
|-----------|-------|-----------|
| Approach Cone Angle | 1° half-angle | Solar illumination |
| Cone Length | 1800 km | Visibility constraint |
| RDV Duration | 24 days | Mission timeline |
| Total ΔV Budget | ≤3.0 m/s | Propellant limit |
| TAG Attempts | 3 max | Sample success probability |

---

## Heritage Missions

This work builds on lessons learned from:

### Hayabusa (2003-2010)
- First asteroid sample return
- Autonomous descent and ascent validated
- GNC challenges identified and addressed

### Hayabusa2 (2014-2020)
- Enhanced autonomous operations
- Multiple TAG attempts capability
- Improved terrain mapping and hazard detection

### OSIRIS-REx (2016-2023)
- High-precision TAG (25 m accuracy)
- Advanced optical navigation
- Natural Feature Tracking (NFT) implementation

---

## References

### Academic Source
**Master's Thesis**: "Lunar Missions Design with Electric Propulsion: A Parametric Study on SEP Trajectories for Small Satellites"
- **Institution**: Politecnico di Torino & Politecnico di Milano
- **Supervisors**: Prof. Lorenzo Casalino (PoliTO), Prof. Camilla Colombo (PoliMI)
- **Implementation**: Chapters 4 (Functional Analysis) & 5 (System Architecture)

### Standards
- ECSS-E-ST-60-30C: Spacecraft GNC verification
- ECSS-E-ST-10-02C: System engineering general requirements
- ECSS-E-ST-10-03: Testing
- ISO/IEC/IEEE 15288:2015: Systems engineering processes

---

## About This Documentation

These diagrams were created as part of the thesis work using:
- **Cameo Systems Modeler** (No Magic) for SysML modeling
- **MBSE Methodology** following ESA SysML Solution guidelines
- **ECSS Standards** for space systems engineering

The diagrams demonstrate:
- ✅ Requirements traceability
- ✅ Functional decomposition
- ✅ System architecture definition
- ✅ Verification planning
- ✅ Standards compliance

---

**For implementation details, see**: [Technical Documentation](TECHNICAL_DOC.md)  
**For code examples, see**: [Quick Start Guide](../QUICKSTART.md)  
**For full project overview, see**: [Main README](../README.md)
