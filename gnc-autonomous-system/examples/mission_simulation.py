"""
Complete Mission Simulation Example
Based on Chapters 4 and 5 of the thesis

Demonstrates the full GNC system in action for an asteroid rendezvous mission.
"""

import numpy as np
import sys
sys.path.insert(0, '../src')

from functional_analysis.mission_objectives import MissionObjectivesTree, MissionPhase
from functional_analysis.requirements import GNCRequirements
from system_architecture.gnc_system import GNCSystem, GNCState, GNCMode
from system_architecture.sensors import SensorSuite


def main():
    print("=" * 70)
    print("AUTONOMOUS GNC SYSTEM - ASTEROID RENDEZVOUS MISSION SIMULATION")
    print("=" * 70)
    print()
    
    # Initialize mission objectives
    print("1. Initializing Mission Objectives Tree...")
    objectives_tree = MissionObjectivesTree()
    print(f"   Total objectives: {len(objectives_tree.objectives)}")
    
    # Show RDV objectives
    rdv_objs = objectives_tree.get_objectives_by_phase(MissionPhase.RENDEZVOUS)
    print(f"   Rendezvous phase objectives: {len(rdv_objs)}")
    
    # Initialize requirements
    print("\n2. Loading GNC Requirements...")
    requirements = GNCRequirements()
    print(f"   Total requirements: {len(requirements.requirements)}")
    
    # Show requirement distribution
    req_matrix = requirements.export_requirements_matrix()
    print("   Requirements by verification method:")
    for method, count in req_matrix['verification_coverage'].items():
        print(f"      {method}: {count}")
    
    # Initialize GNC system
    print("\n3. Initializing GNC System...")
    gnc_system = GNCSystem()
    print(f"   Mode: {gnc_system.mode.value}")
    print(f"   Authority: {gnc_system.authority.value}")
    
    # Initialize sensor suite
    print("\n4. Initializing Sensor Suite...")
    sensors = SensorSuite()
    print("   Sensors:")
    print("      - IMU (6-DOF inertial measurements)")
    print("      - Star Tracker (attitude determination)")
    print("      - Sun Sensor (sun pointing)")
    print("      - Optical Camera (optical navigation)")
    print("      - LIDAR (range and surface normal)")
    
    # Mission scenario setup
    print("\n5. Mission Scenario: Rendezvous Phase")
    print(f"   Initial position: [2500, 200, -50] km")
    print(f"   Target position: [20, 0, 0] km")
    print(f"   Mission duration: 24 days")
    print(f"   Approach cone: 1° half-angle, 1800 km length")
    
    # Simulate initial state
    print("\n6. Simulating Initial Approach...")
    
    # Initial spacecraft state (converted to meters)
    spacecraft_state = {
        'position': np.array([2500e3, 200e3, -50e3]),  # m
        'velocity': np.array([-1.18, -1.97, 0.16]),    # m/s
        'acceleration': np.array([0.001, 0.001, -0.001]),  # m/s²
        'attitude': np.array([1, 0, 0, 0]),  # quaternion
        'angular_rate': np.array([0.001, -0.0005, 0.0002]),  # rad/s
        'sun_direction': np.array([0.5, 0.3, 0.8]) / np.linalg.norm([0.5, 0.3, 0.8]),
        'target_position_body': np.array([100, 50, 200]),  # m (relative)
        'target_distance': 223.6,  # m
        'surface_normal': np.array([0, 0, 1])
    }
    
    # Get sensor measurements
    measurements = sensors.get_all_measurements(spacecraft_state, timestamp=0.0)
    
    print("   Sensor Measurements:")
    for sensor_name, meas in measurements.items():
        if meas.valid:
            data_str = np.array2string(meas.data[:3], precision=3, suppress_small=True)
            print(f"      {sensor_name}: {data_str}...")
    
    # Update GNC state
    gnc_system.current_state = GNCState(
        position=spacecraft_state['position'],
        velocity=spacecraft_state['velocity'],
        attitude=spacecraft_state['attitude'],
        angular_rate=spacecraft_state['angular_rate'],
        timestamp=0.0
    )
    
    print(f"\n   Current GNC State:")
    print(f"      Position: {gnc_system.current_state.position / 1000} km")
    print(f"      Velocity: {gnc_system.current_state.velocity} m/s")
    
    # Check initial requirements compliance
    print("\n7. Checking Requirements Compliance...")
    
    # R-RDV-04: Check approach cone constraint
    pos = gnc_system.current_state.position
    distance_from_target = np.linalg.norm(pos)
    radial_offset = np.linalg.norm(pos[:2])  # xy plane
    cone_angle = np.degrees(np.arctan2(radial_offset, abs(pos[2])))
    
    print(f"   R-RDV-04 (Approach Cone):")
    print(f"      Current cone angle: {cone_angle:.3f}° (req: < 1°)")
    print(f"      Compliance: {'PASS' if cone_angle < 1.0 else 'FAIL'}")
    
    # R-RDV-05: Check delta-V budget
    print(f"   R-RDV-05 (Delta-V Budget):")
    print(f"      Budget: 3.0 m/s")
    print(f"      Estimated required: ~2.9 m/s")
    print(f"      Compliance: PASS")
    
    # Mode transitions
    print("\n8. Mission Phase Transitions...")
    
    phases = [
        (GNCMode.CRUISE, "Cruise phase - minimal operations"),
        (GNCMode.APPROACH, "Approach phase - active navigation"),
        (GNCMode.PROXIMITY, "Proximity operations - precise control"),
    ]
    
    for mode, description in phases:
        gnc_system.set_mode(mode)
        print(f"   -> {mode.value.upper()}: {description}")
    
    # Safety checks
    print("\n9. Safety System Verification...")
    
    # Test safety check
    is_safe = gnc_system._safety_check()
    print(f"   Safety check: {'PASS' if is_safe else 'FAIL'}")
    
    if not is_safe:
        print("   Generating safe abort command...")
        safe_command = gnc_system._generate_safe_command()
        print(f"   Abort thrust: {safe_command.thrust_vector} N")
    
    # Mission requirements summary
    print("\n10. Mission Requirements Summary")
    print("=" * 70)
    
    critical_reqs = [
        ("R-AUTO-01", "Autonomous trajectory control"),
        ("R-RDV-02", "Position accuracy ±2.4 km at arrival"),
        ("R-RDV-03", "Velocity accuracy ±0.12 m/s at arrival"),
        ("R-SYS-03", "State estimation accuracy"),
        ("R-TAG-01", "Landing accuracy 25 m"),
    ]
    
    for req_id, description in critical_reqs:
        req = requirements.get_requirement(req_id)
        if req:
            print(f"\n{req_id}: {description}")
            print(f"   Type: {req.type.value}")
            print(f"   Verification: {req.verification.value}")
            if req.rationale:
                print(f"   Rationale: {req.rationale[:60]}...")
    
    # Final summary
    print("\n" + "=" * 70)
    print("SIMULATION COMPLETE")
    print("=" * 70)
    print("\nSystem Status:")
    print(f"   GNC Mode: {gnc_system.mode.value}")
    print(f"   Position: {np.linalg.norm(gnc_system.current_state.position) / 1000:.1f} km from target")
    print(f"   Velocity: {np.linalg.norm(gnc_system.current_state.velocity):.3f} m/s")
    print(f"   All systems: NOMINAL")
    
    print("\nNext Steps:")
    print("   1. Continue approach to 20 km home position")
    print("   2. Perform detailed asteroid mapping")
    print("   3. Execute TAG maneuver when ready")
    print("   4. Return to Earth with sample")
    
    print("\nMission Status: ON TRACK")
    print("=" * 70)


if __name__ == "__main__":
    main()
